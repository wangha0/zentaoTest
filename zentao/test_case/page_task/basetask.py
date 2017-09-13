class BaseTask(object):

    # 保理金融云公共url地址
    zentao_url = 'http://192.168.137.216'

    # 初始化函数
    def __init__(self, selenium_drvier, base_url=zentao_url, parent=None):
        self.base_url = base_url  # 私有变公共
        self.driver = selenium_drvier  # 私有变公共
        self.timeout = 30  # 定义超时时长
        self.parent = parent

    def getPage(self,page):
        self.page=page

    # 私有函数，只是让开发人员知道，系统中实际不存在私有变量和私有函数的功能
    def _open(self, url):
        url = self.base_url + url
        self.driver.get(url)
        assert self.on_page(), 'Did not land on %s' % url

    # 用于打开baolijinongyun的地址
    def open(self):
        self._open(self.page.url)

    # 判断当前url是否是base_url+url的地址
    def on_page(self):
        return self.driver.current_url == (self.base_url + self.page.url)