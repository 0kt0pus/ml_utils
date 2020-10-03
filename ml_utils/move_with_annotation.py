##This is an improved version of the move selected
import xml.etree.ElementTree as ET
from .utils import function_utils as fu
import os
from tqdm import tqdm

class MoveWithAnnotations():
    def __init__(self, include_xml: bool=True) -> None:
        self.include_xml = include_xml

    def move_using_annotation(self, img_dir: str, req_classes: list, dst_dir: str) -> None:
        ## get the image files
        img_file_list = fu.get_img_paths(img_dir)
        ## the img file name ls
        img_file_name_list = [os.path.splitext(f.split('/')[-1])[0] for f in img_file_list]
        #print(img_file_name_list)
        ## dict to hold file-class assositation
        xfile_class_dict = dict()
        ## iterate, open and get the object class
        if self.include_xml:
            ## get the xmls
            xml_file_list = fu.get_xml_paths(img_dir)
            assert xml_file_list != [], "error: no xml files found"
            print("\nReading annotations\n")
            for xfile in tqdm(xml_file_list):
                xml_keys = ET.parse(xfile)
                root = xml_keys.getroot()
                ## get the objects
                class_list = list()
                for obj in root.findall('object'):
                    name = obj.find('name')
                    class_list.append(name.text)
                ## update the file-class dict
                xfile_class_dict[xfile] = class_list
            ## now we have the file-class association, so iterate over it
            ## and filter out the files that does not have req_classes
            req_file_list = list()
            for k, v in xfile_class_dict.items():
                #print(k, v)
                if list(map(lambda x: x in req_classes, v))[0] == True:
                    req_file_list.append(k)
            ## get the file names of required
            req_file_name_list = [os.path.splitext(f.split('/')[-1])[0] for f in req_file_list]
            ## map the req files
            req_img_bool_list = list(map(lambda x: x in req_file_name_list, img_file_name_list))
            ## filter the false and keep the True so we have the req img file (only true idxs)
            req_img_list = [img_file_list[i] for i, j in enumerate(req_img_bool_list) if j == True]
            #print(len(req_img_list))
            #print(len(req_file_list))
            assert len(req_img_list) == len(req_file_list), "error: number of annotations are not equal to the number of images"
        else:
            req_img_list = img_file_list
        #print(req_file_list)
        #for f in req_file_list:
        #      print(f)
        if not self.include_xml:
            print("\nMoving Images\n")
            fu.mover(req_img_list, dst_dir)
            #return req_img_list
        else:
            print("\nMoving Images\n")
            fu.mover(req_img_list, dst_dir)
            print("\nMoving Annotations\n")
            fu.mover(req_file_list, dst_dir)
        #return (req_img_list, req_file_list)

