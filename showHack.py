#用于可视化某场比赛的hack情况
from DataGet import getHackData,strToDict
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.axes
import networkx as nx

plt.rcParams['font.sans-serif'] = 'kaiti'

path = "./NormalData/hackdata"
#getHackData(566)

def _showHackOfContest(id:int,ax1:matplotlib.axes._axes.Axes,ax2:matplotlib.axes._axes.Axes,ax3:matplotlib.axes._axes.Axes):
    data = pd.read_csv(path+str(id)+".csv") #读入数据

    #ax1用饼状图展示整体Hack情况，以及状态
    hack_dict = {
        "成功hack":0,
        "不成功hack":0,
        "输入有误":0,
        "其他":0
    }
    hack_dict["成功hack"]=data[data['verdict']=="HACK_SUCCESSFUL"].shape[0]
    hack_dict['不成功hack']=data[data['verdict']=="HACK_UNSUCCESSFUL"].shape[0]
    hack_dict['输入有误']=data[data['verdict']=="INVALID_INPUT"].shape[0]
    hack_dict['其他']=data.shape[0]-hack_dict['成功hack']-hack_dict['不成功hack']-hack_dict['输入有误']

    explode = [0.08,0.06,0.04,0.02]
    colors = ['pink','lightgreen','skyblue','orange']
    ax1.pie(hack_dict.values(),labels=hack_dict.keys(),colors=colors,explode=explode,autopct='%1.1f%%')
    ax1.set_title("Hack行为结果",fontsize=13)

    #ax2可以用柱状图表示不同问题的hack情况
    tot_h = dict()
    succ_h = dict()
    for i in range(data.shape[0]):
        string = data.loc[i]['problem']
        string = strToDict(string)
        index = string['index']
        if index in tot_h.keys():
            tot_h[index]+=1
        else:
            tot_h[index]=1
        if data.loc[i]["verdict"]=="HACK_SUCCESSFUL":
            if index in succ_h.keys():
                succ_h[index]+=1
            else:
                succ_h[index]=1
        else:
            if index not in succ_h.keys():
                succ_h[index]=0
    pg=ax2.bar([x-0.2 for x in range(1,len(tot_h.values())+1)],tot_h.values(),width=0.4,color='skyblue',label='尝试hack数')
    ax2.bar_label(pg,label_type='edge')
    pg=ax2.bar([x+0.2 for x in range(1,len(tot_h.values())+1)],succ_h.values(),width=0.4,color='pink',label='成功hack数')
    ax2.bar_label(pg,label_type='edge')
    ax2.legend()
    ax2.set_xticks([x for x in range(1,len(tot_h.values())+1)],labels=tot_h.keys())
    ax2.set_ylabel("数目",fontsize=13)
    ax2.set_title("hack数量统计",fontsize=13)
    ax2.set_xlabel("问题序号")
    
    #ax3用柱状图展示不同用户Hack他人的情况
    tot_h=dict()
    succ_h=dict()
    for i in range(data.shape[0]):
        string = data.loc[i]['hacker']
        string = strToDict(string)['members'][0]['handle']
        if string not in tot_h.keys():
            tot_h[string]=0
        if string not in succ_h.keys():
            succ_h[string]=0
        tot_h[string]+=1
        if data.loc[i]['verdict']=="HACK_SUCCESSFUL":
            succ_h[string]+=1
    succ_h = dict(sorted(succ_h.items(),key=lambda kv:kv[1],reverse=True))
    new_succ=dict();cnt=0
    new_tot = dict()
    for x in succ_h.items():
        cnt+=1
        if cnt>30:
            break
        new_succ[x[0]]=x[1]
        new_tot[x[0]]=tot_h[x[0]]
    pg=ax3.bar([x-0.2 for x in range(1,len(new_tot.values())+1)],new_tot.values(),width=0.4,color='skyblue',label='尝试hack数')
    ax3.bar_label(pg,label_type='edge')
    pg=ax3.bar([x+0.2 for x in range(1,len(new_succ.values())+1)],new_succ.values(),width=0.4,color='pink',label='成功hack数')
    ax3.bar_label(pg,label_type='edge')
    ax3.legend()
    ax3.set_title("成功hack前30名数据",fontsize=13)
    ax3.set_ylabel("数目",fontsize=13)
    ax3.set_xlabel("Hacker",fontsize=13)
    ax3.set_xticks([x for x in range(1,len(new_succ.values())+1)],new_succ.keys(),rotation='vertical')
    
def showHackOfContest(id:int):
    getHackData(id)
    fig = plt.figure(figsize=(10,10))
    plt.title("Contest {} Hack数据统计".format(str(id)),fontsize=22)
    plt.axis('off')
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(212)
    _showHackOfContest(id,ax1,ax2,ax3)
    plt.tight_layout()
    plt.show()

def showHackData(id:int):#展示成功Hack数据
    getHackData(id)
    data = pd.read_csv(path+str(id)+".csv")
    data = data[data['verdict']=='HACK_SUCCESSFUL']
    data = data[['hacker','defender']]
    data = data.reset_index(drop=True)
    ret = dict()
    for i in range(data.shape[0]):
        str1 = strToDict(data.loc[i]['hacker'])
        str2 = strToDict(data.loc[i]['defender'])
        if str1['members'][0]['handle'] not in ret.keys():
            ret[str1['members'][0]['handle']]=list()
        ret[str1['members'][0]['handle']].append(str2['members'][0]['handle'])
    ret = dict(sorted(ret.items(),key=lambda kv:len(kv[1]),reverse=True))
    return ret
    
    

#showHackOfContest(985)
#print(showHackData(566))