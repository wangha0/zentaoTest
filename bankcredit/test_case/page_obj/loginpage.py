#coding=utf-8
import time

from selenium.webdriver.common.by import By

from .basepage import BasePage


class LoginPage(BasePage):

    #页面url后缀
    url='/login/'

    #页面元素定位方式
    login_username_loc=(By.XPATH,"//input[@id='username']")
    login_password_loc=(By.XPATH,"//input[@id='password']")
    login_button_loc=(By.XPATH,"//a[@class='btn btn-info btn_login']")
    login_CAPTCHA_loc=(By.XPATH,"//input[@class='form-control form_check']")
    login_auto_loc=(By.XPATH,"//input[@id='remember_me']")

    #页面可执行动作函数
    def login_username(self,username):
        self.find_element(*self.login_username_loc).clear()
        self.find_element(*self.login_username_loc).send_keys(username)

    def login_password(self,password):
        self.find_element(*self.login_password_loc).clear()
        self.find_element(*self.login_password_loc).send_keys(password)

    def login_CAPTCHA(self,CAPTCHA):
        self.find_element(*self.login_CAPTCHA_loc).clear()
        self.find_element(*self.login_CAPTCHA_loc).send_keys(CAPTCHA)

    def login_button(self):
        for i in range(5):
            try:
                self.find_element(*self.login_button_loc).click()
                break
            except BaseException:
                time.sleep(1)
                continue
        else:
            raise AssertionError