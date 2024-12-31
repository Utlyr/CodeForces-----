#用于可视化用户比赛及rating数据
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import pandas as pd
import matplotlib.axes
import numpy as np
from DataGet import getUserRatingData
# 防止中文乱码
plt.rcParams['font.sans-serif'] = 'kaiti'

username = 'Jiangnan111'



def showRatingChange(ax:matplotlib.axes._axes.Axes,user_name:str):#这里要输入子画布,这里data来自userrating.csv
    getUserRatingData(user_name)
    data = pd.read_csv("./NormalData/userrating.csv")
    data['ratingUpdateTimeSeconds'] = pd.to_datetime(data['ratingUpdateTimeSeconds'],unit='s')
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y-%m-%d"))
    myticks=np.arange(0,4000,200)
    ax.set_yticks(myticks)
    ax.grid(True)
    ax.plot(data['ratingUpdateTimeSeconds'],data['newRating'],color='blue',marker='o')
    #plt.xticks(data['ratingUpdateTimeSeconds'],rotation=45) #显示x轴所有刻度，但太挤了，故不用
    ax.set_title("rating-时间图({})".format(user_name))
    ax.set_xlabel("时间（Y-M-D）")
    ax.set_ylabel("Rating",color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    ax2=ax.twinx()
    ax2.plot(data['ratingUpdateTimeSeconds'],data['rank'],color='r',marker='x')
    ax2.set_ylabel("Rank",color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    

'''fig = plt.figure(figsize=(10,5))
ax = plt.subplot(111)

showRatingChange(ax,username)
plt.show()
'''