import pytesseract
import pandas as pd
from src.utils import read_image, image_preprocess, mrz_selection, mrz_postprocess, ocr_on_selection

# Tesseract-OCR installation location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

img_src = 'https://upload.wikimedia.org/wikipedia/commons/a/a6/People%27s_Republic_of_China_Passport_%2897-2_version_for_Single_Exit_and_Entry%29.png'
img, height, width = read_image(img_src)

img_roi = image_preprocess(img)

img_mrz = mrz_selection(img_roi)

dim_mrz = mrz_selection(img_roi)

mrz = ocr_on_selection(dim_mrz, img_roi, '--psm 12')
lastname, firstname, pp_no = mrz_postprocess(mrz)

dim_lastname_chi = (140, 305, 45, 25)
dim_firstname_chi = (140, 335, 45, 25)

lastname_chi = ocr_on_selection(dim_lastname_chi, img_roi, '--psm 7', lang = 'chi_sim')
lastname_chi = lastname_chi.split('\n')[0]

firstname_chi = ocr_on_selection(dim_firstname_chi, img_roi, '--psm 7', lang = 'chi_sim')
firstname_chi = firstname_chi.split('\n')[0]

passport_dict = {'Passport No.': pp_no,
                 'First Name': firstname,
                 'Last Name': lastname,
                 'First Name (汉字)': firstname_chi,
                 'Last Name (汉字)': lastname_chi}

output = pd.DataFrame(columns = ['Passport No.','First Name','Last Name','First Name (汉字)','Last Name (汉字)'])
output = output.append(passport_dict, ignore_index = True)
print(output)