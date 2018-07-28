#!/usr/bin/env
# coding: utf-8
#utf-8です。

import os
from lxml import etree
from xml.etree import ElementTree

#PICT_DIR="../img"
LABEL_DIR="../annotation"
LABEL_OUT_DIR="../yolo_dataset"

execdir = os.path.dirname(os.path.abspath(__file__))

#label_files = 
def convert2yolo(xml_fp):
    txt = ""

    parser = etree.XMLParser()
    xmltree = ElementTree.parse(xml_fp, parser=parser).getroot()
    #filename = xmltree.find('filename').text
    try:
        verified = xmltree.attrib['verified']
        if verified == 'yes':
            verified = True
    except KeyError:
        verified = False

    size = xmltree.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
        
    for object_iter in xmltree.findall('object'):
        bndbox = object_iter.find("bndbox")
        label = object_iter.find('name').text
        # Add chris
        difficult = False
        if object_iter.find('difficult') is not None:
            difficult = bool(int(object_iter.find('difficult').text))
        truncated = False
        if object_iter.find('truncated') is not None:
            truncated = bool(int(object_iter.find('truncated').text))
        jingai = False
        if object_iter.find('jingai') is not None:
            jingai = bool(int(object_iter.find('jingai').text))
        blur = False
        if object_iter.find('blur') is not None:
            blur = bool(int(object_iter.find('blur').text))
        atypical_pose = False
        if object_iter.find('pose') is not None:
            atypical_pose = bool(int(object_iter.find('pose').text))
        occlusion = 0
        if object_iter.find('occlusion') is not None:
            occlusion = int(object_iter.find('occlusion').text)
        #filter here
        if jingai:
            continue
        if difficult:
            continue
        #convert to yolo format        
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)
        
        x_center_ratio = (xmin+xmax)/width
        y_center_ratio = (ymin+ymax)/height
        w_ratio = (xmax-xmin)/width
        h_ratio = (ymax-ymin)/height

        txt += "0 {} {} {} {}\n".format(x_center_ratio, y_center_ratio, w_ratio, h_ratio)
    return txt
            
for root, dirs, files in os.walk(os.path.join(execdir, LABEL_DIR)):
    for fn in files:
        id, ext = os.path.splitext(fn)
        if ext != ".xml": continue
        fpath = os.path.join(root, fn)
        yolo_txt = convert2yolo(fpath)
        if yolo_txt:
            os.makedirs(os.path.join(execdir, LABEL_OUT_DIR), exist_ok=True)
            with open(os.path.join(execdir, LABEL_OUT_DIR, id+".txt"), "w") as w:
                w.write(yolo_txt)

            
