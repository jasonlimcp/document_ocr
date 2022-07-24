# OCR on documents using OpenCV and PyTesseract
_Last Update: Mar 2021_

### <ins>About</ins>
This project simulates a common use case in modern organizations - digitizing large volumes of documents, specifically ID documents such as PDFs of passports or drivers' licenses.
For images of reasonable image quality and resolution, Tesseract's OCR engine can parse segments of the document into a tabular output.

The example use case in this repo, for a Passport image, is elaborated on in [this Medium article](https://medium.com/p/edc10b5ecb62).

### <ins>Package Requirements</ins>
pytesseract <br>
opencv-python

PyTesseract runs on the Tesseract-OCR engine, which is required to be installed on the host system or server for the package to function. Documentation and downloads for the Tesseract-OCR project can be found [here](https://tesseract-ocr.github.io/tessdoc/Downloads.html).