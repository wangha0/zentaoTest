#coding=utf-8
import sys
import unittest
from models import myunit, function
from bankcredit.test_case.page_task.logintask import LoginTask
from bankcredit.test_case.page_task.usermanagertask import UserManagerTask
from bankcredit.test_case.page_task.sysresponsetask import SysResponseTask
from time import sleep
import logging
sys.path.append('/models')
sys.path.append('/page_obj')
sys.path.append('/page_task')

#系统返回码相关测试案例，首先继承重写了setup和tearup方法的类
class SysResponseTest(myunit.MyTest):

    # 测试用户登录，给了默认值为空
    def user_login_verify(self, username='', password='', CAPTCHA=''):
        LoginTask(self.driver).user_login(username, password, CAPTCHA)

    def test_sysresponse1(self):

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver,'user_login_failed.jpg')
            raise

        #点击并切换窗口至系统返回码管理
        UserManagerTask(self.driver).sys_response_link()

        #验证是否进入系统返回码管理页面
        try:
            self.assertEqual(SysResponseTask(self.driver).pagename_label(),u'系统返回码管理')
        except BaseException:
            function.insert_img(self.driver,'filed.jpg')
            raise

        #新建返回码
        for i in range(10,72):
            SysResponseTask(self.driver).creatnew('800'+str(i),'800'+str(i),3,2)
            sleep(2)