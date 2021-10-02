import xml.etree.ElementTree as ET
import pickle
import os
from collections import OrderedDict
from os import listdir, getcwd
from os.path import join
'''
fire-detect:
    VOC2020 to yolo format code
'''
sets = [('2020', 'train')]
classes = ['reflective_clothes', 'other_clothes']

# VOC2020 folder root
#data_root = r'/home/fire_data/'

# voc的训练txt 验证txt 必须在VOC*** 以及目录下  不能在Main目录下面；它是在统计目录下
def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(year, image_id):    # 输入图片名
    global data_root
    # in_file,即'Annotations/'目录中存入每张图片的VOC格式的标签文件
    in_file = open('Annotations/%s.xml'%(image_id), encoding='utf-8')
    # out_file，即'labels/'目录中即将存入每张图片转换格式后的标签文件
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes: # or int(difficult)==1 不关心difficult
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

# wd = getcwd()

for year, image_set in sets:
    # if not os.path.exists(data_root + 'VOC%s/labels/'%(year)):
    #     os.makedirs(data_root + 'VOC%s/labels/'%(year))
    # read()方法用于从文件读取指定的字节数，如果未给定或为负则读取所有。得到一个字符串
    # strip() 方法用于移除字符串头尾指定的字符（默认为空格）或字符序列。
    # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。    
    # split() 通过指定分隔符对字符串进行切片。
    # str--分隔符，默认为所有的空字符，num--分割次数。默认为 -1, 即分隔所有。
    # 先读取文件中的所有字符，组成一个字符串，strip()处理前后空格后，然后使用split()将其分割
    """
    # 得到所有图片的名称，组成的列表image_ids
    """
    image_ids = open('ImageSets/Main/%s.txt'%(image_set)).read().strip().split() 
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:   # 获取单张图片名称imade_id
        print(image_id)
        # 由图片名image_id 得到该图片的地址 
        # 将该图片的地址加入到"2020_train.txt"文件中, 而且之后的图片地址也同样存入该同一个文件中
        list_file.write('JPEGImages/%s.jpg\n'%(image_id))
        convert_annotation(year, image_id)
    list_file.close()

'''
fire-detect：
    train.txt
    test.txt
'''
root = r'./JPEGImages/'   #存储图片的目录
f = open(r'./2020_train.txt', 'w')    # 打开存储图片地址的文件夹
names = os.listdir(root)   # 得到所有图片的名称
for name in names:
    print(name)
    f.write(os.path.join(root, name)+'\n')
f.close()

# 6：4 -> train.txt test.txt