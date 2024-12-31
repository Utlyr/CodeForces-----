#对用户的提交数据进行可视化
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.axes
import time
import numpy as np
import matplotlib.image as mpimg
plt.rcParams['font.sans-serif'] = 'kaiti'

username = "FXLY_awa"
photoOfUserPath = "./UserPhoto/"

img = mpimg.imread(photoOfUserPath+username+".jpg")
#print(img)
plt.imshow(img,cmap="prism",alpha=1)
plt.show()
'''

# 读取图像文件
img = mpimg.imread('UserPhoto/FXLY_awa.jpg')

# 显示图像
plt.imshow(img)
plt.axis('off')  # 关闭坐标轴
plt.show()
'''