import cv2
import sys
import pytesseract
import csv

def clean_it_up(str, organic, week):
    '''
    (string from image, 0/1, week_1) --> (dict)
    {'date': 'week_1', product name': 'chicken', 'unit_promo_price': '$2.5',
    'uom': 'lb','least_unit_for_promo': 1,'save_per_unit': '$1.75',
    'discount': 0.58,'organic': 0}
    '''
    foods = []
    with open('product_dictionary.csv', newline='') as f:     
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            if not 1:
                foods.append(row)
    d = {}
    d['date'] = week
    for item in foods:
        maybe = str.find(item)
        for maybe not -1:
            name = str[maybe:len(item)]
            d['product name'] = name



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