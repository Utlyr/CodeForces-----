#可视化多用户rating变化线
import requests
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import pandas as pd
import matplotlib.axes
# 防止中文乱码
plt.rcParams['font.sans-serif'] = 'kaiti'
from DataGet import getUserRatingUrl,writeJsonToFile,changeJsonToCsv

userNameArray = ['Jiangnan111','FXLY_awa','k1nsom']
filepath = r'.\MulUserRatingData\userrating' #基础文件名，后面使用时加编号

def GetAllUserRating(userarr:list):
    for i in range(len(userarr)):
        res = requests.get(getUserRatingUrl(userarr[i]))
        writeJsonToFile(filepath+str(i),res.text)
        changeJsonToCsv(filepath+str(i))
        print("用户 {} Rating数据获取完成".format(userarr[i]))
        time.sleep(2) #暂停两秒（因为codeforce的API不能两秒内连续访问）

#GetAllUserRating(userNameArray)
def _showAllUserRating(userarr:list,ax:matplotlib.axes._axes.Axes):
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%Y-%m-%d"))
    ax.grid(True)
    ax.set_xlabel("时间(Y-M-D)")
    ax.set_ylabel("Rating")
    ax.set_title("用户Rating变化对比")
    for i in range(len(userarr)):
        data = pd.read_csv(filepath+str(i)+".csv")
        data['ratingUpdateTimeSeconds'] = pd.to_datetime(data['ratingUpdateTimeSeconds'],unit='s')#转换时间
        ax.plot(data['ratingUpdateTimeSeconds'],data['newRating'],marker='o',label=str(userarr[i]))
def showAllUserRating(usernamearr:list):
    fig = plt.figure(figsize=(10,5))
    ax = plt.subplot(111) 
    GetAllUserRating(usernamearr)
    _showAllUserRating(usernamearr,ax)
    plt.legend()
    plt.show()