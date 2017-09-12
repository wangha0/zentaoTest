#coding=utf-8
from time import sleep
from ..page_obj.usermanagerpage import UserManagerPage
from ..page_task.basetask import BaseTask

class UserManagerTask(BaseTask):
    # 登录成功用户名
    def user_login_success(self):
        return UserManagerPage(self.driver).user_login_success()

    #点击进入银行卡短路验证规则
    def bk_selfvertify_link(self):
        UserManagerPage(self.driver).bk_selfvertify_link()
        sleep(1)
        UserManagerPage(self.driver).short_circuit_link()
        sleep(1)

    #进入特殊路由
    def special_routes_lin(self):
        UserManagerPage(self.driver).short_circuit_link()

    #进入系统返回码管理
    def sys_response_link(self):
        UserManagerPage(self.driver).parameter_config_link()
        sleep(1)
        UserManagerPage(self.driver).sys_response_link()
        sleep(1)
