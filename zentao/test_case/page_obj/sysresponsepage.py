#coding=utf-8
import time
from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class SysResponsePage(BasePage):

    # 页面url后缀
    url = '/sys_response/'

    #页面元素定位方式
    pagename_label_loc=(By.XPATH,"//p[@class='page_name']")
    creatnew_button_loc=(By.XPATH,"//b[@id='creat_new']")
    repcode_input_loc=(By.XPATH,"//input[@name='rep_code']")
    repinfo_input_loc=(By.XPATH,"//input[@name='rep_info']")
    istrue_select_loc=(By.XPATH,"//select[@name='is_true']")
    ischarge_select_loc=(By.XPATH,"//select[@name='is_charge']")
    save_button_loc=(By.XPATH,"//button[@id='add_sysRes']")

    #页面可执行动作函数
    def pagename_label(self):
        return self.find_element(*self.pagename_label_loc).text

    def creatnew_button(self):
        self.find_element(*self.creatnew_button_loc).click()

    def repcode_input(self,text):
        self.find_element(*self.repcode_input_loc).send_keys(text)

    def repinfo_input(self,text):
        self.find_element(*self.repinfo_input_loc).send_keys(text)

    def istrue_select(self,index):
        Select(self.find_element(*self.istrue_select_loc)).select_by_index(index)

    def ischarge_select(self,index):
        Select(self.find_element(*self.ischarge_select_loc)).select_by_index(index)

    def save_button(self):
        self.find_element(*self.save_button_loc).click()