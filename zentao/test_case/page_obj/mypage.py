import time
from selenium.webdriver.common.by import By
from .basepage import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class MyPage(BasePage):

    # 页面url后缀
    url = '/zentao/my.html'

    #页面元素定位方式
    user_login_success_loc=(By.XPATH,"//div[@id='userMenu']/a[1]")
    product_link_loc=(By.XPATH,"//a[@href='/product']")
    channel_link_loc=(By.XPATH,"//a[@href='/channel']")
    bk_selfvertify_link_loc=(By.XPATH,"//a[contains(.,'路由管理')]")
    deal_search_link_loc=(By.XPATH,"//a[@href='/deal_search']")
    account_search_set_link_loc=(By.XPATH,"//a[contains(.,'对账管理')]")
    test_veracity1_link_loc=(By.XPATH,"//a[@href='/test_veracity1']")
    parameter_config_link_loc=(By.XPATH,"//a[contains(.,'参数配置')]")
    bank_bin_link_loc=(By.XPATH,"//a[@href='/bank_bin']")
    sys_response_link_loc=(By.XPATH,"//a[@href='/sys_response']")
    add_button_loc=(By.XPATH,"//b[@id='creatnewuser']")
    short_circuit_link_loc=(By.XPATH,"//a[contains(.,'银行卡短路验证规则')]")
    special_routes_link_loc=(By.XPATH,"//a[@href='/bk_sproute']")
    businessman_routes_link_loc=(By.XPATH,"//a[@href='/bk_orgroute']")

    #新建商户弹出页页面元素定位方式
    businessman_name_input_loc=(By.XPATH,"//input[@aria-describedby='busName-error']")
    businessman_from_select_loc=(By.XPATH,"//select[@aria-describedby='from01-error']")



    #页面可执行动作函数
    def user_login_success(self):
        return self.find_element(*self.user_login_success_loc).text

    def add_button_loc(self):
        self.find_element(*self.add_button_loc()).click()

    def businessman_name_input(self,name):
        self.find_element(*self.businessman_name_input_loc).send_keys(name)

    def businessman_from_select(self,value):
        Select(self.find_element(*self.businessman_from_select_loc)).select_by_value(value)

    def bk_selfvertify_link(self):
        ActionChains(self.driver).move_to_element(self.find_element(*self.bk_selfvertify_link_loc)).perform()

    def parameter_config_link(self):
        ActionChains(self.driver).move_to_element(self.find_element(*self.parameter_config_link_loc)).perform()

    def short_circuit_link(self):
        self.find_element(*self.short_circuit_link_loc).click()
        sleep(3)

    def special_routes_link(self):
        self.find_element(*self.special_routes_link_loc).click()

    def businessman_routes_link(self):
        self.find_element(*self.businessman_routes_link_loc).click()

    def sys_response_link(self):
        self.find_element(*self.sys_response_link_loc).click()
