#coding=utf-8
import sys
import unittest
sys.path.append('/models')
sys.path.append('/page_obj')
sys.path.append('/page_task')
from models import myunit, function
from zentao.test_case.page_task.logintask import LoginTask
from zentao.test_case.page_task.mytask import MyTask

#登录相关测试案例，首先继承重写了setup和tearup方法的类
class loginTest(myunit.MyTest):

    #测试用户登录，给了默认值为空
    def user_login_verify(self,username='',password=''):
        LoginTask(self.driver).user_login(username,password)

    #@unittest.skip("无条件跳过测试")
    def test_login1(self):
        u"""用户名admin，密码wangha0_MS"""
        self.user_login_verify('admin','wangha0_MS')
        try:
            self.assertEqual(MyTask(self.driver).user_login_success(),'admin')
        except BaseException:
            function.insert_img(self.driver,'user_login_failed.jpg')
            raise

if __name__=='__main__':
    unittest.main