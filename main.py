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


def searchImage(img_path, template_path):
    '''
    Returns True or False if template is found in image.
    '''
    threshold = 0.9


    img = cv2.imread(img_path, 0)           # load in grayscale
    template = cv2.imread(template_path,0)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    
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


def blockToText(block_path):
    img = PIL.Image.open(block_path)
    output = pytesseract.image_to_string(img)
    print(output)


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
    #blockToText()

    #endregion


    #region Semantization


    #endregion