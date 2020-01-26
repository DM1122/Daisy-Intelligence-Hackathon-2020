import cv2
import sys
import pytesseract
import csv

def clean_it_up(str1, organic, week):
    stri = str1.lower()
    d = {}
    d['date'] = week
    d['organic'] = organic

    #least_unit_for_promo
    least = 1
    result = stri.find('save')
    if result != -1:
        str2 = stri[result:]
        if 'on' in str2 == True: 
            som = str2.find('$')
            str3 = str2[som:]
            idk = str3.find(' ')
            final = float(str3[1:idk])
            jk = str3[idk:]
            for i, c in enumerate(jk):
                if c.isdigit():
                    least = c
                    break
    d['least_unit_for_promo'] = least

    #Discount (ex. 2/$5, Save $6.98 on 2, output value = $6.98/$11.98 = 0.58)
    result = stri.find('save')
    if result != -1:
        str2 = stri[result:]
        for i, c in enumerate(str2):
            if c.isdigit():
                times = c
                break
    save_price = times
    discount_price = #same as Unit promo price, so get from there
    discount = save_price/(discount_price + save_price)
    d['discount'] = discount
    
    #save_per_unit (ex. save $3.5 on 2, output value – $1.75)
    result = stri.find('save')
    other = stri.find('off')
    num = None
    if other != -1:
        str_s = stri[:other]
        s = str_s.find('$')
        fin = str_s[s:]
        for i, c in enumerate(fin):
                if c.isdigit():
                    times = c
                    break
        num = times
    
    elif result != -1 and ('/' in stri == False):
        str2 = stri[result:]
        if 'on' in str2 == True: 
            som = str2.find('$')
            str3 = str2[som:]
            idk = str3.find(' ')
            final = float(str3[1:idk])
            jk = str3[idk:]
            for i, c in enumerate(jk):
                if c.isdigit():
                    times = c
                    break
            num = final / times

        else: 
            som1 = str2.find('$')
            str3_1 = str2[som1:]
            idk1 = str3_1.find(' ')
            final1 = float(str3_1[1:idk1])
            num = final1
    d['save_per_unit'] = num
   
    #product name 
    foods = []
    with open('product_dictionary.csv', newline='') as f:     
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            if not 1:
                foods.append(row)
    
    name = None
    for item in foods:
        maybe = stri.find(item)
        if maybe != -1:
            name = stri[maybe:len(item)]
            d['product name'] = name
    
    #units 
    units = []
    with open('units_dictionary.csv', newline='') as s:     
        reader1 = csv.reader(s, delimiter=' ')
        for row in reader1:
            if not 1:
                units.append(row)

    name1 = None
    for item1 in units:
        maybe1 = stri.find(item)
        if maybe1 != -1:
            name1 = stri[maybe1:len(item1)]
            name2 = stri[:maybe1]
            new = name2[::-1]
            for i, c in enumerate(new):
                if c.isdigit():
                    another = c
                    break
            d['uom'] = str(another + " " + name1)
    
    #Unit promo price - will need to import variable 'num' from save_per_unit
    if ('half' and 'off' in stri == True) or ('buy' and 'one' and 'get' and 'free' in stri == True):
        unit = num
    else: 
        #this is the one that gives us random letters and shit sooooooo
    d['unit_promo_price'] = unit

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