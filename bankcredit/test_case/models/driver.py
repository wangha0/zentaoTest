#coding=utf-8
from selenium.webdriver import Remote
from selenium import webdriver
import platform
#浏览器初始化，这里使用Selenium Grid设置调用远程主机
def browser():
    #option = webdriver.ChromeOptions()
    #option.add_argument("--user-data-dir=C:/Users/Default/AppData/Local/Google/Chrome/User Data")
    #driver=webdriver.Chrome(chrome_options=option)

    #host='127.0.0.1:4444'    #运行主机：端口号
    #dc={'browserName':'chrome'}    #指定浏览器

    #command_executor默认指向本机的4444端口号，这里将host作为变量，通过配置可以修改默认配置
    #desired_capabilities配置浏览器，具体参数可以查看
    #driver=Remote(command_executor='http://'+host+'/wd/hub',desired_capabilities=dc)

    #driver=webdriver.Chrome()
    Profile=webdriver.FirefoxProfile("C:\Users\Default\AppData"
                                     "\Roaming\Mozilla\Firefox"
                                     "\Profiles\\t43212t8.default")
    driver=webdriver.Firefox(Profile)
    return driver

if __name__ == "__main__":
    dr=browser()
    dr.get('http://www.baidu.com')
    dr.quit()