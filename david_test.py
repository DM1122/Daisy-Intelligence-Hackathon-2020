import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

debug = True

def searchImage(img_path, template_path):
    '''
    Returns True or False if template is found in image.
    '''

    img = cv2.imread(img_path, 0)           # load in grayscale
    template = cv2.imread(template_path,0)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    bound_tl = max_loc
    bound_br = (max_loc[0]+template.shape[1], max_loc[1] + template.shape[0])

    cv2.rectangle(img, bound_tl, bound_br, 255, 2)

    if debug:
        plt.subplot(1,2,1)
        plt.imshow(res, cmap = 'gray')
        plt.title('Matching Result')
        plt.subplot(1,2,2),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point')

    plt.show()


    return flag



if __name__ == '__main__':
    
    result = searchImage(img_path='data/sample/sample_block.png',
                         template_path='data/labels/organic.png')

    print('Result:',result)






    # template = cv2.imread('mario_coin.png')
    # w, h = template.shape[:-1]

    # res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    # threshold = .8
    # loc = np.where(res >= threshold)
    # for pt in zip(*loc[::-1]):  # Switch collumns and rows
    #     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    # cv2.imwrite('result.png', img_rgb)