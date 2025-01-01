#这里对所有Codeforces用户的一些特征进行可视化
import requests
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.axes
from DataGet import writeJsonToFile,changeJsonToCsv
import seaborn as sns

plt.rcParams['font.sans-serif'] = 'kaiti'

alluserinfourl = "https://codeforces.com/api/user.ratedList?activeOnly=False&includeRetired=false"

def getAllUserInfo():#获得codeforces全部用户数据
    res = requests.get(alluserinfourl)
    writeJsonToFile("./NormalData/alluserinfo",res.text)
    changeJsonToCsv("./NormalData/alluserinfo")
    print("所有用户数据获取成功")

#getAllUserInfo()

def showAllUserCountry(ax:matplotlib.axes._axes.Axes):#展示用户所处国家情况
    data = pd.read_csv("./NormalData/alluserinfo.csv")
    country_nums = dict()
    sum = 0
    for x in data['country']:
        if pd.isna(x):#舍弃空值
            continue
        sum+=1
        if x in country_nums.keys():
            country_nums[x]+=1
        else:
            country_nums[x]=1
    #只显示前十个，其他几位others
    arr = list(country_nums.items())
    #print(arr)
    arr=sorted(arr,key=lambda kv:(kv[1],kv[0]),reverse=True)
    new_cn = dict()
    for i in range(25):
        new_cn[arr[i][0]]=arr[i][1]
        sum-=arr[i][1]
    new_cn['Others']=sum
    pg=ax.bar(range(len(new_cn.keys())),new_cn.values(),color='skyblue')
    ax.bar_label(pg,label_type='edge')
    ax.set_xticks(range(len(new_cn.keys())),new_cn.keys(),rotation='vertical')
    ax.set_title("Codeforces主要用户分布",fontsize=20)
    ax.set_ylabel("人数",fontsize=15)
    ax.set_xlabel("国家",fontsize=15)
    plt.savefig("./OutPut/PeoCountry.svg")

def showTop20MostFriend(ax:matplotlib.axes._axes.Axes):
    data = pd.read_csv("./NormalData/alluserinfo.csv")
    friends = dict()
    for i in range(len(data.iloc[0])):
        friends[data.loc[i]['handle']]=data.loc[i]['friendOfCount']
    
    arr = list(friends.items())
    arr=sorted(arr,key=lambda kv:(kv[1],kv[0]),reverse=True)
    arr=arr[:20]
    arr.reverse()
    new_cn = dict()
    for x in arr:
        new_cn[x[0]]=x[1]
    pg=ax.barh(range(len(new_cn.keys())),new_cn.values(),color='pink')
    ax.bar_label(pg,label_type='edge')
    ax.set_yticks(range(len(new_cn.keys())),new_cn.keys())
    ax.set_ylabel("用户昵称",fontsize=15)
    ax.set_title("Codeforces用户朋友最多TOP20",fontsize=20)
    ax.set_xlabel("朋友数目",fontsize=15)

def showTop20HighRating(ax:matplotlib.axes._axes.Axes):
    data = pd.read_csv("./NormalData/alluserinfo.csv")
    friends = dict()
    for i in range(len(data.iloc[0])):
        friends[data.loc[i]['handle']]=data.loc[i]['rating']
    
    arr = list(friends.items())
    arr=sorted(arr,key=lambda kv:(kv[1],kv[0]),reverse=True)
    arr=arr[:20]
    new_cn = dict()
    for x in arr:
        new_cn[x[0]]=x[1]
    pg=ax.bar(range(len(new_cn.keys())),new_cn.values(),color='lightblue')
    ax.bar_label(pg,label_type='edge')
    ax.set_xticks(range(len(new_cn.keys())),new_cn.keys(),rotation='vertical')
    ax.set_ylabel("Rating",fontsize=15)
    ax.set_title("Codeforces Rating最高TOP20",fontsize=20)
    ax.set_xlabel("用户昵称",fontsize=15)

def showAllUserRatingDist(ax:matplotlib.axes._axes.Axes):#可视化全球Rating分布
    data = pd.read_csv("./NormalData/alluserinfo.csv")
    data = data['rating']
    
    ax.hist(data,bins=100,color='skyblue',edgecolor='black',density=True,label="直方图")
    ax.set_title("Codeforces全球用户Rating分布",fontsize=15)
    ax.set_xlabel("Rating",fontsize=15)
    ax.set_ylabel("Rating分布直方图",fontsize=15)
    ax1=ax.twinx()
    ax1.ecdf(data,color='orange',label='密度累积曲线')
    ax1.legend()
    ax.legend(borderaxespad=2.5)
    plt.savefig("./OutPut/UserRatingDis.svg")

    

'''fig = plt.figure(figsize=(8,5))
ax=plt.subplot(111)
showAllUserCountry(ax)
plt.show()'''
#getAllUserInfo()