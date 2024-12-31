#对用户的提交数据进行可视化
import requests
from DataGet import changeJsonToCsv,writeJsonToFile,strToDict,getUserPhoto,getUserInfo #不用文件后缀
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.axes
import time
import numpy as np
import matplotlib.image as mpimg
plt.rcParams['font.sans-serif'] = 'kaiti'

user_name = "Jiangnan111"
photoOfUserPath = "./UserPhoto/"

rankcolors = {
    "newbie":"gray",
    "pupil":"blue",
    "specialist":"cyan",
    "expert":"blue",
    "candidate master":"purple",
    "master":"orange",
    "international master":"red",
    "legendary grandmaster":"red",
    "tourist":"red"
}

def getSubmissionUrl(username:str):
    return "https://codeforces.com/api/user.status?handle={}".format(username)

def getSubInfo(username:str):
    res = requests.get(getSubmissionUrl(username))
    writeJsonToFile("./NormalData/usersubmission",res.text)
    changeJsonToCsv("./NormalData/usersubmission")
    print("用户{}提交数据获取成功".format(username))

#最好保证ax1:5x5,ax2:5x5,ax3:10x5
def showUserSubRecent(username:str,daysbefore:int,ax1:matplotlib.axes._axes.Axes,
                      ax2:matplotlib.axes._axes.Axes,ax3:matplotlib.axes._axes.Axes):#输入天数表示从当前时间往前daysbefore开始
    #把平均难度打印出来
    userdata = pd.read_csv("./NormalData/usersubmission.csv")
    prodata = pd.read_csv("./NormalData/problemdata.csv")
    locatime = time.time()-daysbefore*24*60*60 #计算得到前面的时间
    userdata = userdata[userdata['creationTimeSeconds']>=locatime] #筛选数据

    #此处第一次可视化该用户时取消注释
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
    #print(userinfo)

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
    ax1.set_title("近{}天提交数据".format(daysbefore),fontsize=13)
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
    ax1.text(50,700,"Rating:{}".format(userinfo['rating'][0]),fontsize=13)
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
    


    #展示用户提交结果判定（Accepted,Wrong,TLE,RE,other）
    substate = {'Accepted':0,
                'Wrong Answer':0,
                'TLE':0,
                "RunTimeError":0,
                "other":0}
    substate['Accepted']=userdata[userdata['verdict']=='OK'].shape[0]
    substate['Wrong Answer']=userdata[userdata['verdict']=='WRONG_ANSWER'].shape[0]
    substate['TLE']=userdata[userdata['verdict']=='TIME_LIMIT_EXCEEDED'].shape[0]
    substate['RunTimeError']=userdata[userdata['verdict']=='RUNTIME_ERROR'].shape[0]
    substate['other']=userdata.shape[0]-substate['Accepted']-substate['RunTimeError']-substate['TLE']-substate['Wrong Answer']

    subcolors = ['lightgreen','pink','orange','skyblue','gray']
    explode = [0.08,0.08,0.06,0.04,0.02]
    ax2.pie(substate.values(),labels=substate.keys(),colors=subcolors,explode=explode,autopct='%1.1f%%')
    #ax2.pie(substate.values(),labels=substate.keys(),colors=subcolors,autopct='%1.1f%%')
    ax2.set_title("提交结果",fontsize=13)
    
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
    for x in allsuboftags.keys():
        if x not in accsuboftags.keys():
            accsuboftags[x]=0
    for x in acceptdata['problem']:
        prodict=strToDict(x)
        for y in prodict['tags']:
            accsuboftags[y]+=1
    x_axis = np.arange(0,len(allsuboftags.values()))
    #x_axis1 = np.arange(0,len(accsuboftags.values()))
    ax3.set_title("用户不同类型题目提交/AC数量",fontsize=13)
    ax3.set_xlabel("题目类型",fontsize=13)
    ax3.set_ylabel("数量",fontsize=13)
    pg=ax3.bar(x_axis-0.125,allsuboftags.values(),width=0.25,color='skyblue',label='提交量')
    ax3.bar_label(pg,label_type='edge')
    pg=ax3.bar(x_axis+0.125,accsuboftags.values(),width=0.25,color='pink',label='AC量')
    ax3.bar_label(pg,label_type='edge')
    ax3.set_xticks(range(len(allsuboftags.keys())),labels=allsuboftags.keys(),rotation='vertical')
    ax3.legend()

def ShowSubmission(username:str,days:int):
    getSubInfo(username)
    time.sleep(2)
    fig = plt.figure(figsize=(10,10))
    plt.title("用户近{}天提交情况".format(days),fontsize=22)
    plt.axis('off')
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,1,2)
    showUserSubRecent(username,days,ax1,ax2,ax3)
    plt.tight_layout()
    plt.show()

#print(time.time())
ShowSubmission(user_name,30)