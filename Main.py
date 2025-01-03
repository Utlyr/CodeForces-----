from AllProblemInfoShow import getProData,showAllProblemRatingDis,showInfoProblemLabels
from AllUserInfoShow import getAllUserInfo,showAllUserCountry,showAllUserRatingDist,showTop20HighRating,showTop20MostFriend
from BlogCommentEmotionAna import commentEmotionAna
from MultiUserRatingCom import showAllUserRating
from showHack import showHackData,showHackOfContest
from UserSubmissionInfo import ShowSubmission
from UserInfoDisplay import ShowInfo
import matplotlib.pyplot as plt

if __name__ == "__main__":
    while True:
        print("--------------------------------------------------------------------------")
        print("可视化数据")
        print("1.公共数据\n2.用户数据\n3.非用户数据\n4.退出\n")
        string = input("请输入操作编号：")
        if string == "1":
            print("请输入可视化对象：")
            while True:
                print("1.问题集\n2.全体用户数据\n3.返回上一级\n")
                string1 = input("请输入操作编号：")
                if string1 == '1':
                    getProData() #获取问题集数据
                    while True:
                        print("请输入可视化子对象：")
                        print("1.问题集难度分布\n2.问题标签可视化\n3.返回上一级\n")
                        string2 = input("请输入操作编号：")
                        if string2 == '1':
                            plt.figure(figsize=(10,5))
                            ax = plt.subplot(111)
                            showAllProblemRatingDis(ax)
                        elif string2 == '2':
                            plt.figure(figsize=(14,5))
                            ax = plt.subplot(111)
                            showInfoProblemLabels(ax)
                        elif string2 == '3':
                            break
                        else:
                            print("输入有误！")
                            exit()
                        plt.show()
                elif string1 == '2':
                    getAllUserInfo() #获取所有用户数据
                    while True:
                        print("请输入可视化子对象：")
                        print("1.用户国家分布情况\n2.Rating前20名\n3.朋友数量前20名\n4.Rating分布情况\n5.返回上一级\n")
                        string2 = input("请输入操作编号：")
                        if string2 == '1':
                            plt.figure(figsize=(14,5))
                            ax = plt.subplot(111)
                            showAllUserCountry(ax)
                        elif string2 == '2':
                            plt.figure(figsize=(10,5))
                            ax = plt.subplot(111)
                            showTop20HighRating(ax)
                        elif string2 == '3':
                            plt.figure(figsize=(10,5))
                            ax = plt.subplot(111)
                            showTop20MostFriend(ax)
                        elif string2 == '4':
                            plt.figure(figsize=(8,5))
                            ax = plt.subplot(111)
                            showAllUserRatingDist(ax)
                        elif string2 == '5':
                            break
                        else:
                            print("输入有误！")
                            exit()
                        plt.show()
                elif string1 == '3':
                    break
                else:
                    print("输入有误！")
                    exit()
        elif string == '2':
            print("请输入可视化对象：")
            while True:
                print("1.用户基本信息\n2.用户最近提交数据\n3.用户Rating变化\n4.返回上一级\n")
                string1 = input("请输入操作编号：")
                if string1 == '1':
                    username = input("请输入用户昵称：")
                    ShowInfo(username)
                elif string1 == '2':
                    username,days = input("请输入用户昵称和要查看的天数：").split(' ')
                    days = int(days)
                    ShowSubmission(username,days)
                elif string1 == '3':
                    userlist = input("请输入用户昵称列表：").split(' ')
                    showAllUserRating(userlist)
                elif string1 == '4':
                    break
                else:
                    print("输入有误！")
                    exit()
                plt.show()
        elif string == '3':
            print("请输入可视化对象：")
            while True:
                print("1.竞赛Hack数据可视化\n2.博客情感分析可视化\n3.返回上一级\n")
                string1 = input("请输入操作编号：")
                if string1 == '1':
                    cid = int(input("请输入竞赛ID："))
                    showHackOfContest(cid)
                    plt.show()
                    showHackData(cid)
                    print("Hack图已经存入./OutPut目录下")
                elif string1 == '2':
                    bid = int(input("请输入BlogID："))
                    commentEmotionAna(bid)
                    plt.show()
                elif string1 == '3':
                    break
                else:
                    print("输入有误！")
                    exit()
        elif string == '4':
            break
        else:
            print("输入有误!")
            exit()