import requests
from hashlib import sha512
import json
import csv
import ast

key = "8ce082ccdac955cbfa2c6eaadf8d7d54a8b24720"
secret = '7a8a0ff0c3ae7ded0488320d72b7d7c25b385299'

def getUserRatingUrl(username:str):
    return "https://codeforces.com/api/user.rating?handle={}".format(username)

def writeJsonToFile(filename:str,data:str):#filename不带文件扩展
    with open(filename+".json",'w',encoding='utf-8') as f:
        f.write(data)
def strToDict(data:str):#字符串格式转字典
    return ast.literal_eval(data)
def changeJsonToCsv(filename:str):
    with open(filename+".json",'r',encoding='utf-8') as f:
        data = json.load(f)
    data = data['result'] #取出结果
    if len(data) == 0:
        print("数据为空")
        return
    columns = list(data[0].keys())
    with open(filename+".csv",'w',encoding='utf-8',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for items in data:
            dataarr = list()
            for x in columns:
                if x in items.keys():
                    dataarr.append(items[x])
                else:
                    dataarr.append(None)
            #writer.writerow(list(items.values()))
            writer.writerow(dataarr)
def getUserRatingData(username:str):#获取rating数据
    res = requests.get(getUserRatingUrl(username))
    writeJsonToFile("./NormalData/userrating",res.text)
    changeJsonToCsv("./NormalData/userrating")
    print("用户 {} Rating数据获取成功".format(username))

def getUserPhoto(url:str,savepath:str):#获取用户头像,这里path要加后缀
    with open(savepath,"wb") as f:
        res = requests.get(url)
        f.write(res.content)
    print("用户头像获取成功")

def strToList(data:str):#字符串转列表
    return ast.literal_eval(data)

def getHackData(contestid:int):
    url = "https://codeforces.com/api/contest.hacks?contestId={}".format(str(contestid))
    res = requests.get(url)
    writeJsonToFile("./NormalData/hackdata{}".format(str(contestid)),res.text)
    changeJsonToCsv("./NormalData/hackdata{}".format(str(contestid)))
    print("Contest {} hack数据获取成功".format(str(contestid)))

def getUserInfo(username:str)->None:
    url='https://codeforces.com/api/user.info?handles={}&checkHistoricHandles=false'.format(username)
    res = requests.get(url)
    writeJsonToFile("./NormalData/userinfo{}".format(username),res.text)
    changeJsonToCsv("./NormalData/userinfo{}".format(username))
    print("用户 {} 基本数据获取成功".format(username))