#coding=utf-8
from time import sleep
from ..page_obj.bkselfvertifypage import BkSelfVertifyPage
from ..page_task.basetask import BaseTask

class BkSelfVertifyTask(BaseTask):

    #新建银行短路验证规则
    def creat_role(self,order,sys_return,sys_info=None,**kw):
        BkSelfVertifyPage(self.driver).add_button()
        sleep(1)
        BkSelfVertifyPage(self.driver).order_input(order)
        sleep(1)

        if 'bank_name' in kw:
            BkSelfVertifyPage(self.driver).bank_name_input(kw.get('bank_name'))
            sleep(1)
            BkSelfVertifyPage(self.driver).card_type_click()
            sleep(1)
            BkSelfVertifyPage(self.driver).card_type_click()

        if 'card_type' in kw:
            BkSelfVertifyPage(self.driver).card_type_select(kw.get('card_type'))

        if 'card_bin' in kw:
            BkSelfVertifyPage(self.driver).card_bin_input(kw.get('card_bin'))

        if 'without_card_bin' in kw:
            BkSelfVertifyPage(self.driver).without_card_bin_input(kw.get('without_card_bin'))

        BkSelfVertifyPage(self.driver).sys_return_select(sys_return)
        sleep(1)

        if sys_info==None:
            info=BkSelfVertifyPage(self.driver).get_sys_info_input()
            BkSelfVertifyPage(self.driver).save_button()
            return info
        else:
            BkSelfVertifyPage(self.driver).sys_info_input(sys_info)
            BkSelfVertifyPage(self.driver).save_button()
            return sys_info

    def del_role(self,order):
        orderlist=BkSelfVertifyPage(self.driver).getlist_order_label()
        delbuttonlist=BkSelfVertifyPage(self.driver).getdel_button_loc()
        for l in range(len(orderlist)):
            if orderlist[l].text==order:
                delbuttonlist[l].click()
                sleep(2)









