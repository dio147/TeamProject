import datetime
import requests
import json
import matplotlib.pyplot as plt
import numpy as np

def uploadpng():
    files={'img':('IMG_1808.JPG',open('IMG_1808.JPG','rb'),'image/png')}
    url = 'http://127.0.0.1:8000/testpost/'
    req = requests.post(url,files=files)
    print(json.loads(req.text))

def plt_line_image(tl, x_data, y_data):
    plt.clf()
    plt.title(tl)
    plt.grid(linestyle=":")
    plt.plot(x_data, y_data)
    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    plt.tight_layout()

def plt_bar_img(tl):
    plt.clf()
    plt.title(tl)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.size'] = 13
    # 设置图大小
    x = ['1','2','3','4','5','6','7']
    y1 = [2,3,4,5,6,7,8]
    y2 = [8,7,6,5,4,3,2]
    templist = []
    for i in range(7):
        templist.append(y1[i]+y2[i])
    y3 = [1,2,1,2,1,2,1]
    plt.figure(figsize=(10,8))
    plt.bar(x,y1,label ='抬头时长',width=0.5,bottom=0,linewidth=2)
    plt.bar(x,y2,label ='低头时长',bottom=y1,width=0.5,linewidth=2)
    plt.bar(x,y3,label = '趴下时长',bottom=np.sum([y1,y2],axis=0),width=0.5,linewidth=2)
    plt.legend(loc=1)


def generateGraphicss():
    title = 'title'
    x = np.linspace(0,100,101)
    y = np.linspace(0,100,101)
    plt_line_image(title,x,y)
    plt.savefig('tempImg/save.jpg')

if __name__ == '__main__':
    alist  = [1]
    if alist:
        print('haha')