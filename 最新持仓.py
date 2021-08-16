

import tushare
import pandas
import time
import smtplib
from email.mime.text import MIMEText


#股票类
class Share(object):

    def __init__(self,code,buy,sale):
        self.code=code
        self.name=None #公司名字
        self.openn=None#开盘价
        self.pre_close=None #昨日收盘价
        self.price=None #实时价格
        self.high=None #最高
        self.low=None #最低
        self.change=None #涨幅

        self.buy=buy  #买点或止损点
        self.sale=sale #止盈点


#邮件发送的方法  需要下载安装pyemail模块
def sendMail(subject,content):

    msg_from='1465054996@qq.com'  #发送方邮箱
    passwd='ppkiwzpsdkybhjbh'              #授权码
    msg_to='1465054996@qq.com'      #收件人邮箱                              

    mailServer="smtp.qq.com"       #邮件服务器
    port=465                        #端口号

    #构造邮件部分
    msg=MIMEText(content)       #把正文添加到邮件
    msg['Subject'] = subject    #把主题添加到邮件
    msg['From'] = msg_from      #把发送人添加到邮件
    msg['To'] = msg_to          #把接收人添加到邮件

#发送邮件代码
    try:
        s = smtplib.SMTP_SSL(mailServer,port)     
        s.login(msg_from, passwd)                     #客户端登录发送人邮箱
        s.sendmail(msg_from, msg_to, msg.as_string()) #发送邮件
        print ("发送成功")
    except Exception as e:
        print(e)
        print ("发送失败")
    finally:
        print("结束！")
        s.quit()



#获取股票行情数据的方法
def getData(shareList):

    for share in shareList:

        data=tushare.get_realtime_quotes(share.code)

#给传进来的股票对象的属性赋值
        share.name=data.loc[0][0] #公司名字
        share.openn=float(data.loc[0][1])#开盘价
        share.pre_close=float(data.loc[0][2]) #昨日收盘价
        share.price=float(data.loc[0][3]) #实时价格
        share.high=float(data.loc[0][4]) #最高
        share.low=float(data.loc[0][5]) #最低
        share.change=round((share.price-share.pre_close)/share.pre_close*100,2) #涨幅

        dis="股票名："+share.name+" 价格："+str(share.price)+" 涨幅：\
        "+str(share.change)+"%"+" 开："+str(share.openn)+" 昨收：\
        "+str(share.pre_close)+" 高："+str(share.high)+" 低："+str(share.low)

        print(dis)

        msg="投资建议：继续躺着！"
        if share.price>=share.sale:
            msg="股票名："+share.name+"达到止盈点"+str(share.sale)+"，当前价格"+str(share.price)+"，建议卖出！"
            subject="股票名："+share.name+"注意！价格上涨！"
            print("准备发送邮件...")
            sendMail(subject,msg) #股票价格上涨时发送邮件

        elif share.price<=share.buy:
            msg="股票名："+share.name+"达到止损或买入点"+str(share.buy)+"，当前价格"+str(share.price)+"，建议买入或者止损！"
            subject="股票名："+share.name+"注意！价格下跌！"
            print("准备发送邮件...")
            sendMail(subject,msg)#股票价格下跌时发送邮件
        print(msg)


#主逻辑
while 1==1:

    share1=Share("113596",87.7,110)
    share2=Share("600340",3.9,4.78) 
    share3=Share("600706",5.8,8.2)
    share4=Share("601318",50.8,63.5)
    share5=Share("601727",3.9,6.0)
    share6=Share("000430",4.75,7.25)
    share7=Share("000725",5.4,8.0)
    share8=Share("000430",4.75,7.25)
    share9=Share("002310",2.6,4.1)
    share10=Share("002780",16.6,25.0)
    share11=Share("128062",75.0,92)
    share12=Share("600104",18.0,22)
    share13=Share("128013",105,125)



    sssList=[share1,share2,share3,share4,share5,share6,share7,share8,share9,share10,share11,share12,share13]

    getData(sssList)#股票对象作为参数传入函数

    time.sleep(300)