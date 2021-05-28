# !/usr/bin/python
# -*- coding:utf-8 -*-

import os
import xml.etree.ElementTree as ET

classes = [
    "C15204005005", "C15104005005", "C15331005010", "C15206040005", "C22301125010",
    "C22301070005",
    "C22338005020", "C22345105005", "C22345170045", "C22359040060", "C22342015010",
    "C22342015005",
    "C22342135005", "C21701825005", "C21701065030", "C21701080005", "C21701445005",
    "C21701095005",
    "C21701065010", "C21701130015", "C21109005005", "C15204035010", "C15204020005",
    "C15408115005",
    "C15408150000", "C15408140005", "C15408105005", "C15409015010", "C15410010005",
    "C15428005005",
    "C15105015045", "C15105005005", "C15102015005", "C15418003005", "C15106005010",
    "C15206070025",
    "C15401135015", "C15401030015", "C15403040010", "C15401135010", "C22355005010",
    "C22355005005",
    "C22302060030", "C22302035005", "C22331010005", "C22331375010", "C22331145005",
    "C22301090015",
    "C22338005025", "C22345075010", "C22345005005", "C22345055005", "C22345170050",
    "C22345120015",
    "C22348075005", "C22348090020", "C22348100020", "C22348030040", "C22358060010",
    "C22359040005",
    "C22359040025", "C22359040055", "C22359010005", "C22359050005", "C22359040045",
    "C22359020015",
    "C22330030010", "C22320010005", "C22360210010", "C22360190005", "C22360095010",
    "C22360185010",
    "C22360010005", "C22336025040", "C22326080040", "C22326060005", "C22327100015",
    "C22327065005",
    "C22341055010", "C22341090005", "C22341150010", "C22341185030", "C22341025005",
    "C22341200015",
    "C22341165010", "C22346420005", "C22346290005", "C22346715005", "C22346870005",
    "C22346725010",
    "C22342285005", "C22342010005", "C21102055005", "C21102020020", "C21301095005",
    "C21108045005",
    "C21701690005", "C21701080010", "C21703280010"
]


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(__image_id):
    in_file = open('Annotations/%s.xml' % __image_id)  # （改！）自己的图像标签xml文件的路径
    out_file = open('labels/%s.txt' % __image_id, 'w')  # （改！）自己的图像标签txt文件要保存的路径
    tree = ET.parse(in_file)  # 直接解析xml文件
    root = tree.getroot()  # 获取xml文件的根节点
    size = root.find('size')  # 获取指定节点“图像尺寸”
    w = int(size.find('width').text)  # 获取图像宽
    h = int(size.find('height').text)  # 图像高

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text  # xml里的difficult参数
        cls = obj.find('name').text  # 要检测的类别名称name
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


# 用VOC数据集的话，是将VOCdevkit/VOC2007/ImageSets/Main/文件夹下的所有txt都循环读入了
# 这里我只读入所有待训练图像的路径list.txt
image_paths = os.listdir('images')
for image_path in image_paths:
    image_path = os.path.abspath(os.path.join('images', image_path))
    # list_file.write('/root/darknet-master/data/obj/%s.jpg\n'%(image_id))
    image_id = os.path.split(image_path)[1]  # image_id内容类似'0001.jpg'
    image_id2 = os.path.splitext(image_id)[0]  # image_id2内容类似'0001'
    convert_annotation(image_id2)
