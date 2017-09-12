#coding=utf-8
import sys
import unittest
sys.path.append('/models')
sys.path.append('/page_obj')
sys.path.append('/page_task')
from models import myunit, function
from bankcredit.test_case.page_task.logintask import LoginTask
from bankcredit.test_case.page_task.usermanagertask import UserManagerTask

#登录相关测试案例，首先继承重写了setup和tearup方法的类
class loginTest(myunit.MyTest):

    #测试用户登录，给了默认值为空
    def user_login_verify(self,username='',password='',CAPTCHA=''):
        LoginTask(self.driver).user_login(username,password,CAPTCHA)

    #@unittest.skip("无条件跳过测试")
    def test_login1(self):
        u"""用户名nbry，密码s123456，验证码为空登录"""
        self.user_login_verify('nbry','s123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(),'nbry')
        except BaseException:
            function.insert_img(self.driver,'user_login_failed.jpg')
            raise

if __name__=='__main__':
    unittest.main