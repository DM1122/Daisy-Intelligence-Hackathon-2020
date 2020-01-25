import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

debug = False

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


def getEmptyPath(file_name, file_ext, output_path='output'):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    i = 0

    while os.path.exists(output_path + '/' + file_name + str(i) + file_ext):
        print
        i += 1
    
    empty_path = output_path + '/' + file_name + str(i) + file_ext


    return empty_path



if __name__ == '__main__':
    
    result = searchImage(img_path='data/sample/sample_block_2.png',
                         template_path='data/labels/organic.png')

    print('Result:',result)