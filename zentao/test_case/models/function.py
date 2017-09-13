#coding=utf-8
from selenium import webdriver
import os

def insert_img(driver,file_name):

    base_dir=os.path.dirname(os.path.dirname(__file__))
    base_dir=str(base_dir)

    #将字符串中的\\替换成/
    base_dir=base_dir.replace('\\','/')

    #以/test_case为分隔进行切片，返回数组的第一段字符串
    base=base_dir.split('/test_case')[0]

    #拼接图片文件路径
    file_path=base+'/report/image/'+file_name

    #截图保存到该地址
    driver.get_screenshot_as_file(file_path)

if __name__ == "__main__":
    driver=webdriver.Firefox()
    driver.get('https://www.baidu.com')
    insert_img(driver,'baidu.jpg')
    driver.quit()