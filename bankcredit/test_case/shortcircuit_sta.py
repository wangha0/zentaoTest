#coding=utf-8
import sys
import unittest
from models import myunit, function
from bankcredit.test_case.page_task.logintask import LoginTask
from bankcredit.test_case.page_task.usermanagertask import UserManagerTask
from bankcredit.test_case.page_task.bkselfvertifytask import BkSelfVertifyTask
from time import sleep
from apitest import creditapi
import logging
import xlrd
sys.path.append('/models')
sys.path.append('/page_obj')
sys.path.append('/page_task')

#短路认证相关测试案例，首先继承重写了setup和tearup方法的类
class ShortCircuitTest(myunit.MyTest):

    #测试用户登录，给了默认值为空
    def user_login_verify(self,username='',password='',CAPTCHA=''):
        LoginTask(self.driver).user_login(username,password,CAPTCHA)

    @unittest.skip('skip')
    def test_shortcircuit1(self):
        u"""用户名nbry，密码s123456，银行名称正常短路"""
        filename= self.__str__().split(' (')[0].replace('test_','')
        readfilepath="E:/bankCredit/bankcredit/data/"+filename+'.csv'
        writefilepath='E:/bankCredit/bankcredit/data/'+filename+'result.csv'
        configfilepath='E:/bankCredit/bankcredit/data/'+filename+'config.xls'

        #登录
        self.user_login_verify('nbry','s123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(),'nbry')
        except BaseException:
            function.insert_img(self.driver,'user_login_failed.jpg')
            raise

        #读取配置文件
        configfile=xlrd.open_workbook(configfilepath)
        sheet=configfile.sheet_by_index(0)
        nrows=sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[5]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

           #创建短路认证规则
            sys_info=BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0',''),
                                                               str(sheet.row_values(row)[1]).replace('.0',''),
                                                               bank_name=sheet.row_values(row)[3])
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',','') == sys_info.replace(',',''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            #删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0',''))
            sleep(5)

    @unittest.skip('skip')
    def test_shortcircuit2(self):
        u"""用户名nbry，密码s123456，卡类型正常"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[5]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            sys_info = BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                                 str(sheet.row_values(row)[1]).replace('.0', ''),
                                                                 card_type=sheet.row_values(row)[4])
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',','') == sys_info.replace(',',''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    @unittest.skip('skip')
    def test_shortcircuit3(self):
        u"""用户名nbry，密码s123456，卡BIN单项"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        #定义从第几条数据开始跑，跑几条数据
        start = 0
        leng=0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):
            #读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[5]).replace('.0', '').count('|')==0:
                if leng==0:
                    start=start+1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row==0:
                start=start+1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                                 str(sheet.row_values(row)[1]).replace('.0', ''),
                                                                 card_bin=str(sheet.row_values(row)[5]).replace('.0', ''))
            sleep(1)

            #获取配置文件预计返回信息拼接串
            sys_info=str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i=creditapi.run(readfilepath,writefilepath,start,leng ,'010020000120','8eynXJjkjlNuhoNTC8VE')

            #验证命中情况
            if i.replace(',','') == sys_info.replace(',',''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit4(self):
        u"""用户名nbry，密码s123456，例外卡BIN单项"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):
            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',','') == sys_info.replace(',',''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit5(self):
        u"""用户名nbry，密码s123456，银行名称+卡类型"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      bank_name=sheet.row_values(row)[3],
                                                      card_type=sheet.row_values(row)[4])
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')
            
            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit6(self):
        u"""用户名nbry，密码s123456，银行名称+单一卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      bank_name=sheet.row_values(row)[3],
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit7(self):
        u"""用户名nbry，密码s123456，银行名称+多卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[5]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      bank_name=sheet.row_values(row)[3],
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit8(self):
        u"""用户名nbry，密码s123456，银行名称+例外单卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      bank_name=sheet.row_values(row)[3],
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit9(self):
        u"""用户名nbry，密码s123456，银行名称+例外多卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      bank_name=sheet.row_values(row)[3],
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit10(self):
        u"""用户名nbry，密码s123456，卡类型+单卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      card_type=sheet.row_values(row)[4],
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit11(self):
        u"""用户名nbry，密码s123456，卡类型+多卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      card_type=sheet.row_values(row)[4],
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit12(self):
        u"""用户名nbry，密码s123456，卡类型+例外单卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      card_type=sheet.row_values(row)[4],
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit13(self):
        u"""用户名nbry，密码s123456，卡类型+例外多卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      card_type=sheet.row_values(row)[4],
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit14(self):
        u"""用户名nbry，密码s123456，单一卡BIN+例外单一卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''),
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit15(self):
        u"""用户名nbry，密码s123456，多卡BIN+例外多卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''),
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit16(self):
        u"""用户名nbry，密码s123456，银行名称+卡类型+单卡or多卡BIN"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''),
                                                      bank_name=sheet.row_values(row)[3],
                                                      card_bin=str(sheet.row_values(row)[5]).replace('.0', ''),
                                                      without_card_bin=str(sheet.row_values(row)[6]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

    #@unittest.skip('skip')
    def test_shortcircuit17(self):
        u"""用户名nbry，密码s123456，银行名称+卡类型+卡BIN+例外卡BIN为空"""
        filename = self.__str__().split(' (')[0].replace('test_', '')
        readfilepath = "E:/bankCredit/bankcredit/data/" + filename + '.csv'
        writefilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'result.csv'
        configfilepath = 'E:/bankCredit/bankcredit/data/' + filename + 'config.xls'

        # 登录
        self.user_login_verify('nbry', 's123456')
        try:
            self.assertEqual(UserManagerTask(self.driver).user_login_success(), 'nbry')
        except BaseException:
            function.insert_img(self.driver, 'user_login_failed.jpg')
            raise

        # 读取配置文件
        configfile = xlrd.open_workbook(configfilepath)
        sheet = configfile.sheet_by_index(0)
        nrows = sheet.nrows

        # 定义从第几条数据开始跑，跑几条数据
        start = 0
        leng = 0

        # 进入短路认证
        UserManagerTask(self.driver).bk_selfvertify_link()

        for row in range(nrows):

            # 读取配置文件，给出读取数据起始位置和条数
            if str(sheet.row_values(row)[6]).replace('.0', '').count('|') == 0:
                if leng == 0:
                    start = start + 1
                    leng = 1
                else:
                    start = start + leng
                    leng = 1
            elif row == 0:
                start = start + 1
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1
            else:
                start = start + leng
                leng = str(sheet.row_values(row)[5]).replace('.0', '').count('|') + 1

            # 创建短路认证规则
            BkSelfVertifyTask(self.driver).creat_role(str(sheet.row_values(row)[0]).replace('.0', ''),
                                                      str(sheet.row_values(row)[1]).replace('.0', ''))
            sleep(1)

            # 获取配置文件预计返回信息拼接串
            sys_info = str(sheet.row_values(row)[7]).replace('.0', '')

            # 调用接口验证短路认证规则
            logging.warning(u'开始发送征信请求....')
            i = creditapi.run(readfilepath, writefilepath, start, leng, '010020000120', '8eynXJjkjlNuhoNTC8VE')

            # 验证命中情况
            if i.replace(',', '') == sys_info.replace(',', ''):
                logging.warning(u'短路认证规则命中准确')
            else:
                logging.warning(u'短路认证规则命中不准确')
                logging.warning(u'接口返回message：' + i)
                logging.warning(u'短路认证规则定义返回message:' + sys_info)
            logging.warning(u'结束发送征信请求....\n')

            # 删除短路认证规则
            BkSelfVertifyTask(self.driver).del_role(str(sheet.row_values(row)[0]).replace('.0', ''))
            sleep(5)

if __name__=='__main__':
    unittest.main