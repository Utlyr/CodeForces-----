#Codeforces评论区情感分析
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import brown,stopwords
from nltk.tag import pos_tag
import requests
import matplotlib.pyplot as plt
import matplotlib.axes
from DataGet import writeJsonToFile,changeJsonToCsv
import pandas as pd
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.dates as mdate
plt.rcParams['font.sans-serif'] = 'kaiti'
plt.rcParams['axes.unicode_minus'] = False

def listToStr(arr:list)->str:
    res=str()
    for i in arr:
        res+=i
        res+=' '
    return res

def getComment(blogid:int)->None:
    blogUrl = "https://codeforces.com/api/blogEntry.comments?blogEntryId={}".format(str(blogid))#自己加入id
    res = requests.get(blogUrl)
    writeJsonToFile("./NormalData/blog{}".format(str(blogid)),res.text)
    changeJsonToCsv("./NormalData/blog{}".format(str(blogid)))
    print("Blog {} 评论数据获取成功".format(blogid))

def _commentEmotionAna(blogid:int,ax1:matplotlib.axes._axes.Axes,
                      ax2:matplotlib.axes._axes.Axes,ax3:matplotlib.axes._axes.Axes)->None:
    '''
    这里我认定pos-neg=0的评论为中性，大于0则为积极的，反之则为消极评论，我将其定义为情感系数。
    ax1:可视化评论情感分布
    ax2:用于可视化词云
    ax3:可视化随时间变化的情感变化
    '''
    getComment(blogid)
    data = pd.read_csv("./NormalData/blog{}.csv".format(str(blogid)))
    #data = pd.read_csv("tttt.csv")
    stop_words = set(stopwords.words('english'))
    comments = []
    arrScore = [] #情感系数
    emodit = dict()
    #数据是html格式，先提取出评论
    for i in range(data.shape[0]):#所有评论存放于comments列表
        text = data.loc[i]['text']
        soup = BeautifulSoup(text,"html.parser")
        #print(soup.prettify())
        t = soup.find("p")
        #print(t.text)
        if t is not None:
            comments.append((data.loc[i]['creationTimeSeconds'],t.text))
        else:
            arrScore.append(0)
    text = comments[0]
    

    sid = SentimentIntensityAnalyzer()
    for sen in comments:
        senti = sid.polarity_scores(sen[1])
        #print(senti)
        arrScore.append(senti['pos']-senti['neg'])
        emodit[sen[0]]=senti['pos']-senti['neg']
    ax1.hist(arrScore,bins=50,range=(-1,1),color="skyblue",density=True,edgecolor='black')
    ax1.set_xlabel("情感系数",fontsize=13)
    ax1.set_ylabel("情感分布直方图",color="skyblue",fontsize=13)
    ax1.set_title("情感分布图")
    axtmp=ax1.twinx()
    axtmp.ecdf(arrScore,color='orange')
    axtmp.set_ylabel("累积密度",color='orange',fontsize=13)

    ax2.axis("off")
    ax2.set_title("词云",fontsize=13)
    wordcloud = WordCloud(
        background_color='white',
        height=450,
        width=450,
        margin=10
    ).generate(listToStr([x[1] for x in comments]))
    #wordcloud.to_file('blog{}ciyun.png'.format(blogid))
    ax2.imshow(wordcloud)
    
    base=0
    arr=[]
    for x in emodit.values():
        base+=x
        arr.append(base)
    ax3.xaxis.set_major_formatter(mdate.DateFormatter("%Y-%m-%d"))
    ax3.plot([pd.to_datetime(x,unit='s') for x in emodit.keys()],arr,color='skyblue')
    ax3.set_title("情感随时间变化图",fontsize=13)
    ax3.set_xlabel("时间",fontsize=13)
    ax3.set_ylabel("情感系数和",fontsize=13)


def commentEmotionAna(id:int)->None:
    fig = plt.figure(figsize=(10,10))
    plt.title("Blog{}评论情感可视化".format(id),fontsize=15)
    plt.axis("off")
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,2)
    ax3 = plt.subplot(2,1,2)
    
    _commentEmotionAna(id,ax1,ax2,ax3)
    plt.tight_layout()
    plt.show()
    fig.savefig("./OutPut/Blog{}.svg".format(id))

#commentEmotionAna(135588)