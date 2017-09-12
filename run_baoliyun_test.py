#coding=utf-8
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import unittest
import time
import os

#发送邮件的函数，参数是要发送的内容
def send_email(file_new):

    #打开这个文件
    f=open(file_new,'rb')

    #读取文件内容当作邮件正文
    mail_body=f.read()

    #关闭文件
    f.close()

    #创建MIMEText类实例，调用MIMEText的__init__方法
    msg=MIMEText(mail_body,'html','utf-8')

    #定义邮件主题，发送者和接收者
    msg['Subject']=Header(u'征信项目自动化测试报告','utf-8')
    msg['From'] = 'wangha0mai1@163.com'
    msg['To'] = "770536182@qq.com"

    #创建smtp类实例
    smtp=smtplib.SMTP()

    #连接stmp发送邮件服务器
    smtp.connect('smtp.163.com')

    #发送邮箱用户名密码
    smtp.login('wangha0mai1@163.com','youxiang-123')

    #发送邮件
    smtp.sendmail('wangha0mai1@163.com','770536182@qq.com',msg.as_string())

    #关闭smtp连接
    smtp.quit()

#查找测试报告目录，找到最新生成的测试报告文件
def new_report(testreport):

    #返回目录下所有文件和目录名
    lists=os.listdir(testreport)

    #按照文件创建时间排序
    lists.sort(key=lambda fn:os.path.getmtime(testreport+"\\"+fn))

    #找到最新文件
    file_new=os.path.join(testreport,lists[-1])

    return file_new

if __name__=='__main__':

    #格式化当前时间
    now=time.strftime("%Y-%m-%d %H_%M_%S")

    #定义报告存放路径
    filename='./bankcredit/report/'+now+'_result.html'

    #打开文件
    fp=open(filename,'wb')

    #定义报告
    runner=HTMLTestRunner(stream=fp,title=u'征信项目自动化测试报告',description=u'环境：win10-x64，浏览器：firefox')

    #指定用例为给定目录下，所有*_sta.py文件
    discover=unittest.defaultTestLoader.discover('./bankcredit/test_case',pattern='login*_sta.py')

    #运行测试用例
    runner.run(discover)

    #关闭文件
    fp.close()

    #获得最新报告
    file_path=new_report('./bankcredit/report/')

    #将最新报告通过邮件发送
    #send_email(file_path)