import cv2
import sys
import pytesseract

def clean_it_up(str, organic, week):
    '''
    (string from image, 0/1, week_1) --> (dict)
    {'product name': 'chicken', 'price': 1.99, 'savings': 0.5, 'organic': 0}
    '''


if __name__ == '__main__':
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # Read image path from command line
        imPath = 'data/sample/sample_block.png'
 
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