#coding=utf-8
import time
from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

class BkSelfVertifyPage(BasePage):

    # 页面url后缀
    url = '/bk_selfvertify/'

    #页面元素定位方式
    add_button_loc=(By.XPATH,"//b[@id='creat_new']")
    order_input_loc=(By.XPATH,"//input[@name='sort']")
    bank_name_input_loc=(By.XPATH,"//input[@name='bank_name']")
    card_type_select_loc=(By.XPATH,"//select[@name='ctype_name']")
    card_bin_input_loc=(By.XPATH,"//input[@name='include_bin']")
    without_card_bin_input_loc=(By.XPATH,"//input[@name='exclude_bin']")
    sys_return_select_loc=(By.XPATH,"//select[@name='rep_code']")
    sys_info_input_loc=(By.XPATH,"//input[@name='rep_info']")
    save_button_loc=(By.XPATH,"//button[@id='add_vertify']")
    list_order_label_loc=(By.XPATH,"//td[@class='sorting_1']")
    del_button_loc=(By.XPATH,"//button[@class='st_delete']")

    #页面执行操作
    def add_button(self):
        self.find_element(*self.add_button_loc).click()

    def order_input(self,text):
        self.find_element(*self.order_input_loc).send_keys(text)

    def bank_name_input(self,text):
        self.find_element(*self.bank_name_input_loc).send_keys(text)

    def card_type_select(self,value):
        Select(self.find_element(*self.card_type_select_loc)).select_by_value(value)

    def card_type_click(self):
        self.find_element(*self.card_type_select_loc).click()

    def card_bin_input(self,text):
        self.find_element(*self.card_bin_input_loc).send_keys(text)

    def without_card_bin_input(self,text):
        self.find_element(*self.without_card_bin_input_loc).send_keys(text)

    def sys_return_select(self,value):
        Select(self.find_element(*self.sys_return_select_loc)).select_by_value(value)

    def sys_info_input(self,text):
        self.find_element(*self.sys_info_input_loc).send_keys(text)

    def get_sys_info_input(self):
        return self.find_element(*self.sys_info_input_loc).get_attribute('value')

    def save_button(self):
        self.find_element(*self.save_button_loc).click()

    def getlist_order_label(self):
        return self.find_elements(*self.list_order_label_loc)

    def getdel_button_loc(self):
        return self.find_elements(*self.del_button_loc)

