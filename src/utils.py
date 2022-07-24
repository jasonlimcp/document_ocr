import os
import requests
import math
import numpy as np
import cv2
import pytesseract

def read_image(img_src):
    img_data = requests.get(img_src).content
    with open('src/storage/temp_img.png', 'wb') as handler:
        handler.write(img_data)

    img = cv2.imread('src/storage/temp_img.png',0)
    (height, width) = img.shape

    os.remove("src/storage/temp_img.png")

    return img, height, width

def image_preprocess(img):
    img_canny = cv2.Canny(img, 50, 100, apertureSize = 3)
    img_hough = cv2.HoughLinesP(img_canny, 1, math.pi / 180, 100, minLineLength = 100, maxLineGap = 10)

    (x, y, w, h) = (np.amin(img_hough, axis = 0)[0,0], np.amin(img_hough, axis = 0)[0,1],
    np.amax(img_hough, axis = 0)[0,0] - np.amin(img_hough, axis = 0)[0,0],
    np.amax(img_hough, axis = 0)[0,1] - np.amin(img_hough, axis = 0)[0,1])

    img_roi = img[y:y+h,x:x+w]

    return img_roi

def mrz_selection(img_roi):
    (height, width) = img_roi.shape
    dim_mrz = (1, round(height*0.9), width-3, round(height-(height*0.9)))
    
    return dim_mrz

def mrz_postprocess(mrz):
    mrz = [line for line in mrz.split('\n') if len(line)>10]
    if mrz[0][0:2] == 'P<':
        lastname = mrz[0].split('<')[1][3:]
    else:
        lastname = mrz[0].split('<')[0][5:]
    
    firstname = [i for i in mrz[0].split('<') if (i).isspace() == 0 and len(i) > 0][1]
    pp_no = mrz[1][:9]

    return lastname, firstname, pp_no

def ocr_on_selection(dim, img_roi, config, lang = None):
    
    (x, y, w, h) = dim
    img_roi = cv2.rectangle(img_roi, (x, y), (x + w ,y + h),(0,0,0))
    img_select = img_roi[y:y+h, x:x+w]

    # Display Selected Region
    #cv2.imshow("test", img_select)
    #cv2.waitKey(0)

    img_select =cv2.GaussianBlur(img_select, (3,3), 0)
    ret, img_select = cv2.threshold(img_select,127,255,cv2.THRESH_TOZERO)

    output_str = pytesseract.image_to_string(img_select, lang, config)

    return output_str