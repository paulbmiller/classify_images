"""
Can be used to classify images from a folder. Standard routine can be
started using the function classify_folder(path, list of classes).
"""
import os
import cv2
import pandas as pd

TEST_FOLDER = 'test_folder'
TEST_CLASSES = ['Class1', 'Class2', 'Class3']
CSV_FILENAME = 'Classification.csv'


def classify_folder(path_to_classify, classes, prev_class={}, gray=False):
    """
    Classify images in a folder.
    
    Classify the image shown by pressing the keys from 1 to 9, with the
    option to go back using backspace. It can also deal with grayscale images
    (by setting the argument gray to True) and can avoid reclassifying already
    classified images (by passing in a dictionary from loading the CSV file
    using the load_csv function).

    Parameters
    ----------
    path_to_classify : str
        Path to the folder.
    classes : list
        List of class names.
    prev_class : dict
        Previously created dictionary (loaded from file).
    gray : bool
        Whether the images are grayscale or not.

    Returns
    -------
    classified : dict
        Dictionary of {filename : class_name} pairs.

    """
    classified = dict()
    filenames0 = os.listdir(path_to_classify)
    filenames = []
    
    for fn in filenames0:
        if fn not in prev_class.keys():
            filenames.append(fn)

    i = 0
    while i < len(filenames):
        back = False
        if not gray:
            cv2.imshow(
                'Classify', cv2.imread(path_to_classify + '/' + filenames[i]))
        else:
            cv2.imshow(
                'Classify',
                cv2.imread(path_to_classify + '/' + filenames[i], 0))
        while True:
            k = cv2.waitKey(20)
            
            if k >= ord('1') and k <= ord('9') and k < ord('1') + len(classes):
                classified[filenames[i]] = classes[k - 49]
                print('Classified as {}'.format(classes[k - 49]))
                break
            
            elif k == 8 and i > 0:
                i -= 1
                back = True
                break
            
            elif k == 27:
                classified = prev_class
                i = len(filenames)
                break
            
            elif k == 115:
                save_to_csv(classified)
                i = len(filenames)
                break
            
            else:
                continue
        
        if not back:
            i += 1
    
    cv2.destroyAllWindows()
    
    return classified


def save_to_csv(class_dict):
    """
    Save a dictionary to a CSV file.

    Parameters
    ----------
    class_dict : dict
        Dictionary of {filename : class_name} pairs.

    Returns
    -------
    None.

    """
    if os.path.exists(TEST_FOLDER + '/' + CSV_FILENAME):
        for fn, cl in pd.read_csv(
                TEST_FOLDER + '/' + CSV_FILENAME, header=None).to_numpy():
            if fn not in class_dict:
                class_dict[fn] = cl
    
    with open(TEST_FOLDER + '/' + CSV_FILENAME, 'w') as f:
        for key in class_dict.keys():
            f.write('{},{}\n'.format(key, class_dict[key]))


def load_csv():
    """
    Load a dictionary from the CSV file.

    Returns
    -------
    class_dict : dict
        Dictionary of {filename : class_name} pairs.

    """
    class_dict = dict()
    if os.path.exists(TEST_FOLDER + '/' + CSV_FILENAME):
        for fn, cl in pd.read_csv(
                TEST_FOLDER + '/' + CSV_FILENAME, header=None).to_numpy():
            if fn not in class_dict:
                class_dict[fn] = cl

    return class_dict


if __name__ == '__main__':
    class_dict = load_csv()
    
    class_dict = classify_folder(TEST_FOLDER,
                                 TEST_CLASSES,
                                 class_dict)
    
    save_to_csv(class_dict)
