#用于展示单个用户的有用信息
from UserRatingDisplay import showRatingChange
import matplotlib.pyplot as plt
import matplotlib.axes
import pandas as pd
from DataGet import strToDict,getUserPhoto,getUserInfo
import matplotlib.image as mpimg
from UserSubmissionInfo import rankcolors,photoOfUserPath
from UserSubmissionInfo import getSubInfo
import time
import numpy as np

user_name = "FXLY_awa"

def showUserInfo(username:str,ax1:matplotlib.axes._axes.Axes,
                      ax2:matplotlib.axes._axes.Axes,ax3:matplotlib.axes._axes.Axes):#展示用户基本信息
    userdata = pd.read_csv("./NormalData/usersubmission.csv")
    prodata = pd.read_csv("./NormalData/problemdata.csv")

    getUserInfo(username)
    userinfo = pd.read_csv("./NormalData/userinfo{}.csv".format(username))
    if 'city' not in userinfo.columns:
        userinfo['city']=np.nan
    if 'country' not in userinfo.columns:
        userinfo['country']= np.nan
    if "organization" not in userinfo.columns:
        userinfo['organization']=np.nan
    #print(userinfo)
    #print(userinfo['titlePhoto'][0])
    getUserPhoto(userinfo['titlePhoto'][0],photoOfUserPath+username+".jpg")

    #ax1展示用户在这段时间内，解决问题的个数，maxrating，avegrating
    acceptdata = userdata[userdata['verdict']=='OK']
    #print(acceptdata)
    accedict = dict() #注意此处rating为0的问题表示还未确定rating，后面算平均值需要删除
    for x in acceptdata['problem']:#这里所有题目均算，但是vp题目rating记为0,同时不计入平均值
        prodict = strToDict(x) #将这个转为字典对象
        #print(prodict)
        accedict[prodict['name']]=0
        nd = prodata[prodata['name']==prodict['name']]
        nd=nd.reset_index(drop=True)
        #print(nd)
        #print(nd)
        if nd.empty or pd.isna(nd['rating'][0]):
            continue
        else:
            #print(nd)
            accedict[nd['name'][0]] = nd['rating'][0]
    #print(accedict)
    ratedpro = list()#有rating的数据（只存入rating）
    for i in accedict.values():
        if i != 0:
            ratedpro.append(i)
    if len(ratedpro)==0:#防止后面出现问题（0/0）
        ratedpro.append(0)
    ax1.set_facecolor("skyblue")
    ax1.set_xlim(0,1000)
    ax1.set_ylim(0,1000)
    #这里文字大小后面微调
    ax1.text(50,850,"用户：\n{}".format(username),bbox=dict(boxstyle="round,pad=0.3,rounding_size=0.2",fc="w", ec="black", lw=3),color=rankcolors[userinfo['rank'][0]],fontsize=13)
    ax1.text(50,250,"解决问题平均rating:{:.2f}".format(sum(ratedpro)/len(ratedpro)),color='blue',fontsize=13)
    ax1.text(50,150,"解决问题最大rating:{:.2f}".format(max(ratedpro)),color='red',fontsize=13)
    ax1.text(50,50,"AC/提交数：{}/{}".format(len(accedict.keys()),userdata.shape[0]),color='g',fontsize=13)
    ax1.text(50,600,"Rank:",fontsize=13,color='black')
    ax1.text(50,550,"{}".format(userinfo['rank'][0]),fontsize=13,color=rankcolors[userinfo['rank'][0]])
    ax1.text(50,650,"Rating:{}".format(userinfo['rating'][0]),fontsize=13)
    ax1.text(50,725,"Max Rating:{}".format(userinfo['maxRating'][0],fontsize=13))
    city = userinfo['city'][0]
    country = userinfo['country'][0]
    if pd.isna(city):
        city=''
    if pd.isna(country):
        country=''
    og = userinfo['organization'][0]
    if pd.isna(og):
        og=''
    ax1.text(50,330,"Organization:\n{}".format(og),fontsize=13,color='black')
    ax1.text(50,450,"From:{} {}".format(country,city),fontsize=13,color='black')
    img = mpimg.imread(photoOfUserPath+username+".jpg")
    #print(img)
    #ax1.imshow(img,cmap="prism")
    #ax1.figure.figimage(img, 420, 1095, zorder=1,alpha=1)#这种方法在ipynb不能输出
    k=img.shape
    #print(550+450*k[0]/max(k[0],k[1]))
    #ax1.imshow(img,extent=(550,800,550,800))
    ax1.imshow(img,extent=(550,550+int(450*k[1]/max(k[0],k[1])),550,int(550+450*k[0]/max(k[0],k[1]))))
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title("用户基本数据",fontsize=13)

    #展示用户不同类型题目的提交/AC数
    allsuboftags = dict()
    accsuboftags = dict()
    for x in userdata['problem']:
        prodict=strToDict(x)
        for y in prodict['tags']:
            if y in allsuboftags.keys():
                allsuboftags[y]+=1
            else:
                allsuboftags[y]=1
    for x in acceptdata['problem']:
        prodict=strToDict(x)
        for y in prodict['tags']:
            if y in accsuboftags.keys():
                accsuboftags[y]+=1
            else:
                accsuboftags[y]=1
    for x in allsuboftags.keys():
        if x not in accsuboftags.keys():
            accsuboftags[x]=0
    accsuboftags = dict(sorted(accsuboftags.items(),key=lambda kv:kv[1],reverse=True))
    sdict = dict();cnt=0
    for x in accsuboftags.items():
        sdict[x[0]]=x[1]
        cnt+=1
        if cnt==5:
            break
    subcolors = ['lightgreen','pink','orange','skyblue','gray']
    explode = [0.08,0.08,0.06,0.04,0.02]
    ax2.pie(sdict.values(),labels=sdict.keys(),explode=explode,colors=subcolors,autopct='%1.1f%%')
    ax2.set_title("用户提交最多5类题目",fontsize=13)

    showRatingChange(ax3,username)
    ax3.set_title("用户Rating变化情况",fontsize=13)

def ShowInfo(username:str):
    getSubInfo(username)
    time.sleep(2)
    fig = plt.figure(figsize=(10,10))
    plt.title("用户数据展示",fontsize=22)
    plt.axis('off')
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,1,2)
    showUserInfo(username,ax1,ax2,ax3)
    plt.tight_layout()
    plt.show()
    fig.savefig("./OutPut/User_{}_Info.svg".format(username))

#print(time.time())
#ShowInfo("Jiangnan111")