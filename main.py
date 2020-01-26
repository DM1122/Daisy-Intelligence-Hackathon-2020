import csv
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import progress.bar
import pytesseract

import workspacelib



database = 'data/flyers/'
debug = False

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Block:
    def __init__(self, ref):
        self.ref = ref          # the path of the block image
        self.text = self.blockToText().lower()

        self.flyer_name = os.path.dirname(self.ref)
        self.product_name = self.findProductName()
        self.unit_promo_price = self.findUnitPromoPrice()
        self.uom = self.findUOM()
        self.least_unit_for_promo = self.findLeastUnitForPromo()
        self.save_per_unit = self.findSavePerUnit()
        self.discount = None
        self.organic = self.searchLabel('data/labels/organic.png')

    def blockToText(self):
        img = PIL.Image.open(self.ref)
        text = pytesseract.image_to_string(img)
        return text

    def findProductName(self):
        #product name 
        foods = []
        with open('data/product_dictionary.csv', newline='') as f:     
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                if not 1:
                    foods.append(row)
        
        name = None
        for item in foods:
            maybe = self.text.find(item)
            if maybe != -1:
                name = self.text[maybe:len(item)]
        
        return name
    
    def findUnitPromoPrice(self):
        #need to divide by least
        unit = 0
        if ('half' and 'off' in self.text == True) or ('buy' and 'one' and 'get' and 'free' in self.text == True):
            unit = self.save_per_unit
        else: 
            start = self.text.find('$')
            nums = ['0','1','2','3','4','5','6','7','8','9','.']
            if start == -1:
                return unit
            i = start
            while self.text[i]  in nums:
                print(self.text)
                i += 1
            
            unit = self.text[start:i]           # always returns zero
        return unit

    def findUOM(self):
        #units 
        units = ['ib']
        with open('data/units_dictionary.csv', newline='') as s:     
            reader1 = csv.reader(s, delimiter=' ')
            for row in reader1:
                if not 1:
                    units.append(row)

        name1 = None
        another = ''
        for item1 in units:
            maybe1 = self.text.find(item1)
            if maybe1 != -1:
                name1 = self.text[maybe1:len(item1)]
                name2 = self.text[:maybe1]
                new = name2[::-1]
                for i, c in enumerate(new):
                    if c.isdigit():
                        another = c
                        break
        na = str(another) + " " + str(name1)
        
        return na

    def findLeastUnitForPromo(self):
        least = 1
        result = self.text.find('save')
        if result != -1:
            str2 = self.text[result:]
            if 'on' in str2 == True: 
                som = str2.find('$')
                str3 = str2[som:]
                idk = str3.find(' ')
                jk = str3[idk:]
                for i, c in enumerate(jk):
                    if c.isdigit():
                        least = c
                        break
        
        return least

    def findSavePerUnit(self):
        result = self.text.find('save')
        other = self.text.find('off')
        num = None
        if other != -1:
            str_s = self.text[:other]
            s = str_s.find('$')
            fin = str_s[s:]
            for i, c in enumerate(fin):
                    if c.isdigit():
                        num = c
                        break
        
        elif result != -1 and ('/' in self.text == False):
            str2 = self.text[result:]
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
        
        return num
   
    def findDiscount(self):
        #Discount (ex. 2/$5, Save $6.98 on 2, output value = $6.98/$11.98 = 0.58)
        result = self.text.find('save')
        if result != -1:
            str2 = self.text[result:]
            for i, c in enumerate(str2):
                if c.isdigit():
                    save_price = float(c)
                    break
        
        yeah = float(self.unit_promo_price)*float(self.least_unit_for_promo)
        discount = save_price/(yeah + save_price)
        return  discount

    def searchLabel(self, template_path):
        '''
        Returns True or False if template is found in image.
        '''
        threshold = 0.9


        img = cv.imread(self.ref, 0)           # load in grayscale
        template = cv.imread(template_path,0)
        print('IMAGE:',img)
        print('TEMPLATE:',template)

        try:
            res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        except:
            res = np.zeros(1)
        
        loc = np.where(res >= threshold)

        if loc[0].shape[0] != 0:
            flag = True
        else:
            flag = False


        if debug:

            for point in zip(*loc[::-1]):
                cv2.imwrite(getEmptyPath('res','.png'), img)
                cv2.rectangle(img, point, (point[0]+template.shape[1], point[1]+template.shape[0]), (0,0,255), 2)

            plt.subplot(1,2,1)
            plt.title('Convolution')
            plt.imshow(res, cmap = 'gray')
            
            plt.subplot(1,2,2)
            plt.title('Detection')
            plt.imshow(img, cmap = 'gray')
            
            plt.show()


        return flag

    def toList(self):
        return [self.flyer_name, self.product_name, self.unit_promo_price, self.uom, self.least_unit_for_promo, self.save_per_unit, self.discount, self.organic]


def segmentFlyer(image_path):
    '''
    Segements flyer into its consituent blocks.
    '''

    img = cv.imread(image_path,0)

    # edges
    edged = cv.Canny(img, 100, 200)

    # dilation
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(50,50))
    dilated = cv.dilate(edged, kernel, iterations=1)

    # contours
    contours, hierarchy = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contoured = img.copy()
    cv.drawContours(contoured, contours, -1, (0,255,0), 3)

    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        block = img[y:y+h, x:x+w]

        if not block.shape[0] < 256:            # filter out garbage
            image_name = os.path.basename(image_path)
            save_path = workspacelib.getAvailablePath('block','.png', output_path='temp/blocks/'+image_name+'/')
            cv.imwrite(save_path, block)
            

    if debug:
        plt.subplot(1,4,1)
        plt.imshow(img, cmap='gray')
        plt.title('Image')

        plt.subplot(1,4,2)
        plt.imshow(edged, cmap='gray')
        plt.title('Edges')

        plt.subplot(1,4,3)
        plt.imshow(dilated, cmap='gray')
        plt.title('Dilation')


        plt.subplot(1,4,4)
        plt.imshow(contoured, cmap='gray')
        plt.title('Contoured')

        plt.show()




if __name__ == '__main__':
    workspacelib.clear()
    workspacelib.setup()
    

    #region Segmentation
    file_paths = os.listdir(database)
    bar = progress.bar.Bar('Segmenting Flyers', max=len(file_paths))
    for file_path in file_paths:
        image_path = database+file_path
        segmentFlyer(image_path)

        bar.next()
    bar.finish()
    #endregion

    #region OCR
    blocks = []

    file_dirs = os.listdir('temp/blocks')
    bar = progress.bar.Bar('Instantiating blocks', max=len(file_dirs))
    for file_dir in file_dirs:
        block_paths = os.listdir('temp/blocks/'+file_dir)
        for block_path in block_paths:
            blocks.append(Block(ref='temp/blocks/'+file_dir+'/'+block_path))
        bar.next()
    bar.finish()
    #endregion

    #region Output
    data = []
    for block in blocks:
        data.append(block.toList())
    
    with open('temp/output/output.csv', mode='w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)
    #endregion

