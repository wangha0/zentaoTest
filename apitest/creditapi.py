#coding=utf-8
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#调用征信接口
def credit(type,bankCard,name,idCard,phone,securityCode,userKey,pwd):
    req=requests.get('http://10.12.12.117:8080/api/bank_card_info/?type='
                     + type +
                     '&bankCard='
                     + bankCard +
                     '&name='
                     +name+
                     '&idCard='
                     +idCard+
                     '&phone='
                     +phone+
                     '&securityCode='
                     +securityCode+
                     '&userKey='
                     +userKey+
                     '&pwd='
                     +pwd)
    responsetext=req.text.replace(r'"','').replace(r'{data:{serialNo:,requestParas:{','').replace(r',','')
    responsephone=responsetext.split('phone:')[1].split('idCard')[0]
    responseidcard=responsetext.split('idCard:')[1].split('name')[0]
    responsename=responsetext.split('name:')[1].split('type')[0]
    responsetype=responsetext.split('type:')[1].split('bankCard')[0]
    responsebankCard=responsetext.split('bankCard:')[1].split('}unionpayC')[0]
    responsemsg = responsetext.split('msg:')[1].split('code:')[0]
    responsecode=responsetext.split('code:')[1].split('}')[0]
    return responsetype,responsebankCard,responsename,responseidcard,responsephone,responsemsg,responsecode

#读取数据，调用接口，写入文件，返回返回信息拼接串
def run(readfilepath,writerfilepath,start,leng,usrkey,password):
    readfile=open(readfilepath,'r')
    readdata=csv.reader(readfile)
    readdata=list(readdata)

    writefile = open(writerfilepath, 'ab')
    writedata = csv.writer(writefile, dialect='excel')

    msgstring=''

    for row in readdata[start-1:start-1+leng]:
        req=credit(row[0],row[1],row[2],row[3],row[4],row[5],usrkey,password)
        msgstring=msgstring+req[5]
        writedata.writerow(req)

    readfile.close()
    writefile.close()

    return msgstring

if __name__=="__main__":
    req=requests.get('http://10.12.10.170:9090/yxzb/static/upload/temp/T2mYrH8aXCZPNGLZZ2PO20170710112658.mp4')
    print req.status_code
