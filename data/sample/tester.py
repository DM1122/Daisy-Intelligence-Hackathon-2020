import cv2
import sys
import pytesseract
import csv

def clean_it_up(str1, organic, week):
    str = str1.lower()
    d = {}
    d['date'] = week
    #d['least_unit_for_promo'] = least
    d['organic'] = organic

    #Unit promo price:
    #if 'half off' or 'buy one, get one free' == True:
        #unit = num
    #...
    d['unit_promo_price'] = unit

    #Discount
    #2/$5, Save $6.98 on 2, output value = $6.98/$11.98 = 0.58
    #discount = save_price/(discount_price + save_price)

    result = word.find('save')
    #other = word.find('off')
    num = None
    if save != -1 #and there is not a slash: 
        #if the word 'on' comes after
            #num = ___ / ____
        #else: (i.e. nothing)
            #num = ___
        d['save_per_unit'] = num
    
    foods = []
    with open('product_dictionary.csv', newline='') as f:     
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            if not 1:
                foods.append(row)
    
    name = None
    for item in foods:
        maybe = str.find(item)
        if maybe != -1:
            name = str[maybe:len(item)]
            d['product name'] = name

    units = []
    with open('units_dictionary.csv', newline='') as s:     
        reader1 = csv.reader(s, delimiter=' ')
        for row in reader1:
            if not 1:
                units.append(row)

    name1 = None
    for item1 in units:
        maybe1 = str.find(item)
        if maybe1 != -1:
            name1 = str[maybe1:len(item1)]
            #add numbers before unit (see example output)
            d['uom'] = name1

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