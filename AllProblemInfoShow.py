#用于获取问题集信息以及进行可视化
import requests
from DataGet import changeJsonToCsv,strToDict,writeJsonToFile,strToList
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes
import numpy as np
plt.rcParams['font.sans-serif']='kaiti'

problemUrl = "https://codeforces.com/api/problemset.problems"
filename1 = './NormalData/problemdata'
filename2 = './NormalData/problemStatisticsdata'

def getProData():#获取问题集信息
    res = requests.get(problemUrl)
    writeJsonToFile("./NormalData/problemdata",res.text)
    with open(filename1+".json",'r',encoding='utf-8') as f:
        data = json.load(f)
    data = data['result'] #取出结果
    if len(data) == 0:
        print("数据为空")
        return
    columns = list(data['problems'][0].keys())
    if 'rating' not in columns:
        columns.append('rating')
    with open(filename1+".csv",'w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for items in data['problems']:
            dataarr = list()
            for x in columns:
                if x in items.keys():
                    dataarr.append(items[x])
                else:
                    dataarr.append(None)
            #writer.writerow(list(items.values()))
            writer.writerow(dataarr)
    columns = list(data['problemStatistics'][0].keys())
    with open(filename2+".csv",'w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for items in data['problemStatistics']:
            dataarr = list()
            for x in columns:
                if x in items.keys():
                    dataarr.append(items[x])
                else:
                    dataarr.append(None)
            #writer.writerow(list(items.values()))
            writer.writerow(dataarr)
    print("问题集数据获取成功")

#给一个10x5的画布
def showAllProblemRatingDis(ax:matplotlib.axes._axes.Axes):#可视化codeforces的问题难度分布
    data = pd.read_csv("./NormalData/problemdata.csv")
    ax.hist(data['rating'],bins=100,color='skyblue',density=True)
    ax.set_ylabel("density",fontsize=15)
    ax.set_xlabel("难度系数",fontsize=15)
    ax.set_title("Codeforces难度系数分布图")
    #data['rating'].plot(kind = 'kde',label = '密度图')
    plt.savefig("./OutPut/ProblemDis.svg")

#这里最好给一个10x5的画布
def showInfoProblemLabels(ax:matplotlib.axes._axes.Axes):#可视化不同标签题目的数量和平均难度
    problems = dict()
    data = pd.read_csv("./NormalData/problemdata.csv")
    for i in range(data.shape[0]):
        arr = strToList(data.loc[i]['tags'])
        for tags in arr:
            if tags not in problems.keys():
                problems[tags]=list()
            if pd.isna(data.loc[i]['rating']):
                problems[tags].append(0)
            else:
                problems[tags].append(data.loc[i]['rating'])
    #ax.grid(True)
    xl = np.arange(0,len(problems.keys()),1)
    x_labels = list(problems.keys())
    nums = [len(x) for x in problems.values()]
    avge = [sum(x)/len(x) for x in problems.values()]
    ax.bar(xl-0.2,nums,width=0.4,color='skyblue')
    ax.set_ylabel("数量",fontsize=15)
    ax.tick_params(axis='y', labelcolor='skyblue')
    ax.set_xticks(range(len(x_labels)),labels=x_labels,rotation='vertical')
    ax.set_xlabel("问题类型",fontsize=15)
    ax.set_title("不同类型问题数目/平均难度",fontsize=15)
    ax1 = ax.twinx()
    ax1.bar(xl+0.2,avge,width=0.4,color='pink')
    ax1.set_ylabel("平均难度",fontsize=15)
    ax1.tick_params(axis='y',labelcolor='pink')
    plt.savefig("./OutPut/ProblemLabels.svg")

#getProData()

'''fig = plt.figure(figsize=(10,5))
ax = plt.subplot(111)
showInfoProblemLabels(ax)
plt.show()'''