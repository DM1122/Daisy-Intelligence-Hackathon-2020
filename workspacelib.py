
import os
import shutil


workspace = ['temp/', 'temp/blocks/', 'temp/output/']

verbose = True


def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts
    

def setup():
    '''
    Setup workspace folders.
    '''

    for folder in workspace:
        if not os.path.exists(folder):
            print('[workspacelib]: Creating folder "{}"'.format(folder)) if verbose else False
            os.mkdir(folder)
            

def clear():
    '''
    Clears workspace folders.
    '''

    print('[workspacelib]: Clearing workspace') if verbose else False
    
    for folder in workspace:       
        try:
            shutil.rmtree(folder)
        except:
            pass


def getAvailablePath(file_name, file_ext, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    i = 0
    while os.path.exists(output_path + '/' + file_name + '_' + str(i) + file_ext):
        i += 1
    
    empty_path = output_path + '/' + file_name + '_' + str(i) + file_ext


    return empty_path



if __name__ == '__main__':
    clear()