# coding: utf-8
import sys
import os
import cv2
import numpy as np
import pretreatment

from keras import models
from mlearn_for_image import preprocess_input

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def get_text(img, offset=0):
    text = pretreatment.get_text(img, offset)
    text = cv2.cvtColor(text, cv2.COLOR_BGR2GRAY)
    text = text / 255.0
    h, w = text.shape
    text.shape = (1, h, w, 1)
    return text


def main(fn):
    # 读取并预处理验证码
    img = cv2.imread(fn)
    text = get_text(img)
    imgs = np.array(list(pretreatment._get_imgs(img)))
    imgs = preprocess_input(imgs)

    # 识别文字
    model = models.load_model(os.getcwd()+'/pytool/model.h5')
    label = model.predict(text)
    label = label.argmax()
    wordStr = ''
    fp = open(os.getcwd()+'/pytool/texts.txt', encoding='utf-8')
    texts = [text.rstrip('\n') for text in fp]
    text = texts[label]
    wordStr += text
    #print("word-"+text)
    # 获取下一个词
    # 根据第一个词的长度来定位第二个词的位置
    if len(text) == 1:
        offset = 27
    elif len(text) == 2:
        offset = 47
    else:
        offset = 60
    text = get_text(img, offset=offset)
    if text.mean() < 0.95:
        label = model.predict(text)
        label = label.argmax()
        text = texts[label]
        wordStr += ","+text
        #print("word-"+text)

    # 加载图片分类器
    model = models.load_model(os.getcwd()+'/pytool/12306.image.model.h5')
    labels = model.predict(imgs)
    labels = labels.argmax(axis=1)
    arr = []
    posStr = ''
    for pos, label in enumerate(labels):
        posStr += (str)(pos // 4)+(str)(pos % 4)+","+texts[label]+" "

    result = wordStr+";"+posStr
    print(result)

if __name__ == '__main__':
    #main('test.png')
    main(sys.argv[1])
