class BasePage(object):

    # 初始化函数
    def __init__(self, selenium_drvier):
        self.driver = selenium_drvier  # 私有变公共

    def find_element(self,*loc):
        return self.driver.find_element(*loc)

    def find_elements(self,*loc):
        return self.driver.find_elements(*loc)

    def script(self,src):
        return self.driver.execute_script(src)
