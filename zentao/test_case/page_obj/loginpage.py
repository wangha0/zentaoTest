import time

from selenium.webdriver.common.by import By

from .basepage import BasePage

class LoginPage(BasePage):

    #页面url后缀
    url='/zentao/'

    #页面元素定位方式
    account_input_loc=(By.XPATH,"//input[@id='account']")
    password_input_loc=(By.XPATH,"//input[@name='password']")
    login_button_loc=(By.XPATH,"//button[@id='submit']")
    keep_input_loc=(By.XPATH,"//input[@id='keepLoginon']")
    forget_link_loc=(By.XPATH,"//a[contains(text(),'忘记密码')]")

    #页面可执行动作函数
    def account_input(self,username):
        self.find_element(*self.account_input_loc).clear()
        self.find_element(*self.account_input_loc).send_keys(username)

    def password_input(self,password):
        self.find_element(*self.password_input_loc).clear()
        self.find_element(*self.password_input_loc).send_keys(password)

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