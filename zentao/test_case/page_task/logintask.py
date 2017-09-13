from time import sleep

from ..page_obj.loginpage import LoginPage
from ..page_task.basetask import BaseTask

class LoginTask(BaseTask):

    #因为登录动作会被其他页面频繁调用，所以写在登录页面，方便其他页面调用
    #这里的username,password如果其他页面使用的一致的话，可以设置默认值，其他页面调用的时候可以不用重复设置
    #因为保理金融云的角色比较多，不适用于这种情况，所以不设置默认值
    def user_login(self,username,password):
        self.getPage(LoginPage(self.driver))
        self.open()
        self.page.account_input(username)
        self.page.password_input(password)
        self.page.login_button()
        sleep(1)

    # 用户名错误提示
    def user_error_hint(self):
        return LoginPage(self.driver).user_error_hint()

    # 密码错误提示
    def pawd_error_hint(self):
        return LoginPage(self.driver).pawd_error_hint()

    # 验证码错误提示
    def CAPTCHA_error_hint(self):
        return LoginPage(self.driver).CAPTCHA_error_hint()

    # 登录成功用户名
    def user_login_success(self):
        return LoginPage(self.driver).user_login_success()

