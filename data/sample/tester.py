import cv2
import sys
import pytesseract

if __name__ == '__main__':
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # Read image path from command line
        imPath = 'data/sample/sample_block_crop.png'
 
        # Define config parameters.
        # '-l eng'  for using the English language
        # '--oem 1' for using LSTM OCR Engine
        config = ('-l eng --oem 1 --psm 3')
 
        # Read image from disk
        im = cv2.imread(imPath, 0)
        # Run tesseract OCR on image
        text = pytesseract.image_to_string(im, config=config)
 
        # Print recognized text
        print(text)