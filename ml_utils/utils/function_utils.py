import pathlib
import os
import numpy as np
import shutil
from tqdm import tqdm

def get_version() -> str:
    return "VERSION: 0.1"

def get_xml_paths(img_dir: str) -> list:
    def filter_imgs(elem):
        if elem.split('/')[-1].split('.')[-1] == 'xml':
            return True
        else:
            return False

    xml_list = list()
    for root, subdir, files in os.walk(img_dir):
        for name in files:
            file_path = pathlib.PurePath(root, name)
            xml_list.append(file_path.as_posix())
    xml_file_list = list(filter(filter_imgs, xml_list))

    return xml_file_list

def get_img_paths(img_dir: str) -> list:
    def filter_xmls(elem):
        if elem.split('/')[-1].split('.')[-1] == 'xml' or \
           elem.split('/')[-1].split('.')[-1] == 'py' or \
            elem.split('/')[-1].split('.')[-1] == 'json':
            return False
        else:
            return True
    ## get all xmls
    #img_dir='../data/Cards_Balanced_Dataset_v2'
    #print(img_dir)
    ## get all paths
    file_list = list()
    for root, subdir, files in os.walk(img_dir):
        for name in files:
            file_path = pathlib.PurePath(root, name)
            file_list.append(file_path.as_posix())
    img_file_list = list(filter(filter_xmls, file_list))

    return img_file_list

def get_all_paths(img_dir: str) -> list:
    file_list = list()
    for root, subdir, files in os.walk(img_dir):
        for name in files:
            file_path = pathlib.PurePath(root, name)
            file_list.append(file_path.as_posix())

    return file_list

def annotate_name(input_path: list, annotation: str):
    input_path = get_img_paths(input_path)
    for f in input_path:
        ext_img = f.split('.')[-1]
        os.rename(f, 
                    '.'.join([
                        '_'.join([
                            ''.join(os.path.splitext(f)[0]), 
                            annotation
                            ]), 
                        ext_img
                        ]))
        os.rename(
            '.'.join([
                    ''.join(os.path.splitext(f)[0]), 
                'xml'
                ]), 
                                                    '.'.join([
                                                            '_'.join([''.join(os.path.splitext(f)[0]), 
                                                            annotation
                                                            ]), 
                                                        'xml'
                                                        ]))

def filter_list(full_list: list, to_keep: list) -> list:
    class_name = [
            '_'.join(os.path.splitext(name.split('/')[-1])[0].split('_')[:3])
                for name in full_list]
    #print(class_name)
    filtered_list = list(map(lambda x: x in to_keep, class_name))
    return filtered_list
'''
def make_file_class_dict(file_dir):
    ## get xml files
    xml_list = get_xml_paths(file_dir)
    ## iterate and make a dict of file-class
    for xml_file in xml_list:
        ## open xml
'''
def rot2square(cxcywha_list: list) -> list:
    cx, cy, w, h, a = cxcywha_list
    deg_a = int(np.degrees(a))
    ## if angle is orthogonal to the axes, only shift w, h for 90 and 270
    #cxcywha = list()
    '''
    if deg_a in [90, 270]:
        w, h = h, w
        return [cx, cy, w, h]
    if deg_a in [0, 180]:
        return [cx, cy, w, h]
    elif (deg_a > 0 and deg_a < 90):
    '''
    ## get the four lengths of the box
    s = np.abs(np.sin(a))
    c = np.abs(np.cos(a))
    new_h = w * s + h * c
    new_w = h * s + w * c
    return [cx, cy, new_w, new_h]

def tlbr(cxcywh_list: list) -> list:
    cx, cy, w, h = cxcywh_list
    tl_x = cx - (w / 2)
    tl_y = cy - (h / 2)
    br_x = tl_x + (w)
    br_y = tl_y + (h)

    return [tl_x, tl_y, br_x, br_y]

def write_label_map_v1(objname_list):
    with open('./annotations/label_map_single_quadrat.pbtxt', 'a') as the_file:
        for idx, objname in enumerate(objname_list):
            #print(idx)
            the_file.writelines('item\n')
            the_file.writelines('{\n')
            the_file.writelines('\tid: {}'.format(idx+1))
            the_file.writelines('\n')
            the_file.writelines("\tname: '{0}'".format(str(objname)))
            the_file.writelines('\n')
            the_file.writelines('}\n')
            the_file.writelines('\n')

def mover(src_path: list, dst_dir: str):
    #dst_path = [pathlib.PurePath(dst_dir, f.split('/')[-1]) for f in src_path]
    for p in tqdm(src_path):
        dst_file = pathlib.PurePath(dst_dir, p.split('/')[-1]).as_posix()
        shutil.copyfile(p, dst_file)


def get_file_name(file_path: str) -> str:
    return os.path.splitext(file_path)[0].split('/')[-1]