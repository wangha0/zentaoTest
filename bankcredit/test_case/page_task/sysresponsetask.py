#coding=utf-8
from time import sleep
from ..page_obj.sysresponsepage import SysResponsePage
from ..page_task.basetask import BaseTask
from ..models import function

class SysResponseTask(BaseTask):

    #验证是否进入系统返回码页面
    def pagename_label(self):
        return SysResponsePage(self.driver).pagename_label()

    #新建一条系统返回码
    def creatnew(self,repcode,repinfo,istrueindex,ischargeindex):
        SysResponsePage(self.driver).creatnew_button()
        sleep(1)
        SysResponsePage(self.driver).repcode_input(repcode)
        sleep(1)
        SysResponsePage(self.driver).repinfo_input(repinfo)
        sleep(1)
        SysResponsePage(self.driver).istrue_select(istrueindex)
        sleep(1)
        SysResponsePage(self.driver).ischarge_select(ischargeindex)
        sleep(1)
        SysResponsePage(self.driver).save_button()
        sleep(1)
