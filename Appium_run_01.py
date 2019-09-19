# 需要安装客户端的包
# pip install Appium-Python-Client
import os
import random
import re
import subprocess
import time
import traceback
from multiprocessing import Pool

import jieba
import requests
from appium import webdriver
from selenium.webdriver.common.keys import Keys

from APP_UA import UA


# 主动报错类
class CustomError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class Chrom_Run():
    def __init__(self, Cellphone_id, Mitmproxy_port, Appium_port):
        self.mitmproxy_port = Mitmproxy_port
        self.Appium_port = Appium_port
        # redis 数据库连接
        # self.pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
        # self.redis = redis.Redis(connection_pool=self.pool)
        # self.redis.set('ips', 'A')
        self.UA = UA
        self.ip_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=100017&port=1&pack=63643&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&gm=4"
        self.ua = random.choice(self.UA)
        print(self.ua)
        time.sleep(random.random())
        ip = requests.get(self.ip_url, timeout=5).text
        if "再试" in str(ip):
            time.sleep(random.randint(1, 4))
            ip = requests.get(self.ip_url, timeout=5).text
        # 如果没有在白名单，就添加白名单
        elif "请添加白名单" in str(ip):
            self_ip = re.compile('"请添加白名单(.*?)","', re.S).findall(str(ip))[0]
            print("白名单添加中，本机IP：", self_ip)
            try:
                x = requests.get(
                    "http://web.http.cnapi.cc/index/index/save_white?neek=79185&appkey=7b4bb8a059ff41c8f6782f11e73bff30&white={}".format(
                        self_ip))
                print(x.text)
            except Exception as f:
                print("白名单添加错误》》》", f)
            time.sleep(1)
            ip = requests.get(self.ip_url, timeout=5).text
        self.ip = ip.strip()
        try:
            print("测试IP中》》》》:当前代理IP", self.ip)
            i = int(self.ip.split(":")[1])
        except Exception as f:
            print("IP获取错误，程序退出")
            return
        self.cap = {
            "platformName": "Android",
            # "platformVersion": "5.1.1",  # 修改成匹配安卓版本，最好是版本低于7
            "platformVersion": "5.1.1",  # 修改成匹配安卓版本，最好是版本低于7
            "deviceName": Cellphone_id,  # 获取手机标识码
            # "appPackage": "com.android.chrome",  # 混合APP用这个
            "appActivity": "org.chromium.chrome.browser.ChromeTabbedActivity",
            # org.mozilla.focus.activity.MainActivity
            "browserName": "Chrome",  # 浏览器用这个
            # "browserName": "Firefox",  # 浏览器用这个
            "noReset": True,  # 不每次重置
            'unicodeKeyboard': True,  # 启用uni输入法
            'resetKeyboard': True,  # 结束后重置回原始输入法
            "noSign": True,
            "autoAcceptAlerts": True,  # 同意协议
            "automationName": "UiAutomator1",  # 指定UiAutomator版本，默认最新
            'dontStopAppOnReset': False,  # 不关闭应用
            'autoGrantPermissions': True,  # 自动获取权限
            # 允许传入chromeOptions参数
            "chromeOptions": {
                "args": ['--incognito', '--disable-search-geolocation-disclosure', "user-agent={}".format(self.ua),
                         '--proxy-server=http://{}'.format(self.ip)]}  # 允许传入chromeOptions参数
        }
        with open("C:\\Users\\asus\\Desktop\\gjc.txt", 'r')as f:
            m = f.read()
        self.gjcs = m.split("\n")
        # self.gjcs = gjc
        print(Cellphone_id, "|||", self.Appium_port)
        self.driver = webdriver.Remote("http://localhost:" + str(self.Appium_port) + "/wd/hub", self.cap)
        with open("C:\\Users\\asus\\Desktop\\pbc.txt", 'r')as f:
            m = f.read()
        self.urls = m.split("\n")

    def huadong(self):
        x1 = int(self.driver.get_window_size()['width'] * 0.5)
        y1 = int(self.driver.get_window_size()['height'] * 0.75)
        y2 = int(self.driver.get_window_size()['height'] * 0.25)
        # for i in range(1):
        self.driver.swipe(x1, y2, x1, y1)
        # time.sleep(time.time())

    def insert_login(self, name, url):
        print(name, "|", url, "|", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "|", "芝麻代理IP")
        with open("C:\\Users\\asus\\Desktop\\搜索日志.log", "a", encoding="utf-8")as f:
            f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            f.write("   ")
            f.write(name)
            f.write("   ")
            f.write(url)
            f.write("\n")

    # 屏幕下滑
    def sub_hua_dong(self):
        x1 = int(self.driver.get_window_size()['width'] * 0.5)
        y1 = int(self.driver.get_window_size()['height'] * 0.75)
        y2 = int(self.driver.get_window_size()['height'] * 0.25)
        for i in range(random.randint(2, 4)):
            self.driver.swipe(x1, y1, x1, y2)
            self.driver.implicitly_wait(5)
            time.sleep(random.randint(1, 4))

    # 屏幕上滑
    def sup_hua_dong(self):
        x1 = int(self.driver.get_window_size()['width'] * 0.5)
        y1 = int(self.driver.get_window_size()['height'] * 0.75)
        y2 = int(self.driver.get_window_size()['height'] * 0.25)
        for i in range(random.randint(1, 3)):
            self.driver.swipe(x1, y2, x1, y1)
            self.driver.implicitly_wait(5)
            time.sleep(random.randint(1, 4))

    # @retry(stop_max_attempt_number=3)
    def get_baidu_index(self, name):
        try:
            print("打开百度")
            self.driver.get("https://m.baidu.com/")
            self.driver.implicitly_wait(2)
            # self.huadong()
            try:
                # self.driver.find_element_by_id("index-kw")
                self.driver.find_element_by_xpath('//input[@type="search"]')
            except:
                self.driver.implicitly_wait(1)
                self.driver.refresh()
                print("刷新")
                self.driver.implicitly_wait(1)
            # name1 = "IP"
            name1 = list(jieba.cut(name))
            for i in name1:
                # self.driver.find_element_by_xpath('//input[@type="search"]').send_keys(i)
                self.driver.find_element_by_id("index-kw").send_keys(i)
                time.sleep(random.random())
            try:
                self.driver.find_element_by_id("index-bn").click()
            except:
                print("提交错误")
                self.driver.find_element_by_id("index-bn").send_keys(Keys.ENTER)
        except Exception as f:
            print("网络错误")
            return 0
        else:
            return 1

    def _next(self, i):
        v = random.randint(0, 1)
        if v:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            print("第", i, "次点击", self.driver.current_url)
            x = len(self.driver.find_elements_by_xpath("//a"))
            self.driver.find_elements_by_xpath("//a")[random.randint(5, x)].click()
            self.sub_hua_dong()

    def bak(self, name):
        self.driver.implicitly_wait(10)
        self.sup_hua_dong()
        x = self.driver.find_elements_by_xpath("//*[contains(@class,'c-showurl')]")
        m = list(filter(lambda v: "广告" in v.get_attribute('textContent'), x))  # 筛选出有广告关键字的A标签
        # print("筛选出有广告关键字的A标签",m)
        m1 = []
        for i in m:
            for il in self.urls:
                if il not in i.get_attribute('textContent'):
                    m1.append(i)
        # print("筛选屏蔽的",m1)
        i2 = random.choice(m1)
        # print("随机屏蔽的",i2)
        te = i2.get_attribute('textContent')
        te1 = str(te).replace("广告", "")
        for i in self.urls:
            if i in te:
                return
        if "pintai7" in te:
            return
        # elif "pintai6" in te:
        #     return
        elif "21cxhua" in te:
            return
        print(te)
        try:
            self.driver.execute_script("arguments[0].click();", i2)

        except Exception as f:
            traceback.print_exc()
            print(f)
            i2.click()
        self.driver.implicitly_wait(10)
        for i in self.urls:
            if i in self.driver.current_url:
                return
        print(self.driver.current_url)
        #     # self.driver.quit()
        #     return
        self.sub_hua_dong()
        try:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.implicitly_wait(5)
            print(self.driver.title)
            print("选中:", name, te, self.driver.current_url)
            self.insert_login(name, url=self.driver.current_url)
        except Exception as f:
            print(f)
        try:
            for i in range(5):
                self._next(i)
        except Exception as f:
            print("下一页错误，程序退出")
        for i in range(5):
            self._next(i)
        # time.sleep(random.randint(10, 30))
        print('正在退出')
        return

    # 杀死当前mitmproxy进程
    def kill_mitmproxy(self):
        p = os.popen('netstat -aon|findstr "{}"'.format(self.mitmproxy_port))
        p2 = p.read()
        # 第一版：

        p2 = str(p2).split("\n")
        p2 = p2[0:-1]
        p3 = []
        for i in p2:
            x = re.compile("(\d{1,5})$").findall(i)[0]
            if int(x) != 0:
                p3.append(x)
        p3 = set(p3)
        p3 = list(p3)
        for i in p3:
            p = os.popen('tasklist|findstr "{}"'.format(i))
            p2 = p.read()
            if "thon" in str(p2):
                subprocess.Popen('taskkill -PID {} -F'.format(i))
                print("结束mitmprxoy服务,端口号：", i)
        # 第二版改写，使用lambda不成功
        # for i in list(filter(lambda x: int(x) != 0, set(
        #         sum(list(map(lambda x: re.compile("(\d{1,5})$").findall(x), str(p2).split("\n")[0:-1])), []))))[1:]:
        #     print("结束mitmprxoy服务,端口号：", i)
        #     subprocess.Popen('taskkill -PID {} -F'.format(i))

    # 清除浏览器Cookies和缓存
    def chear_chrom_data(self):
        try:
            print("删除cokies")
            self.driver.delete_all_cookies()
            print("清除本地缓存")
            self.driver.execute_script("window.localStorage.clear();")
        except Exception as f:
            print("清缓失败", f)

    # 获取代理IP
    def get_ip(self):
        ip = requests.get(self.ip_url, timeout=5).text
        ip = ip.strip()
        if len(ip) < 22:
            print("当前IP：", ip)
            return ip
        else:
            time.sleep(1)
            print("提取失败：", ip)
            self.get_ip()

    # 启动mitmproxy服务
    def start_mitmproxy_server(self):
        self.kill_mitmproxy()
        p = os.path.exists('C:\\Users\\asus\\Desktop\\vps3\\mitmproxy_log\\' + str(self.mitmproxy_port) + '.log')
        if p:
            pass
        else:
            print("文件不存在，创建中")
            with open('./mitmproxy_log/' + str(self.mitmproxy_port) + '.log', "w") as fp:
                pass
        cmd = "mitmdump --mode=upstream:{} -p {}".format(
            self.get_ip(), str(self.mitmproxy_port))
        print("启动mitmproxy：", cmd)
        # return
        subprocess.Popen(cmd, stdout=open(
            'C:\\Users\\asus\\Desktop\\vps3\\mitmproxy_log\\' + str(self.mitmproxy_port) + '.log', 'a'),
                         stderr=subprocess.STDOUT)
        time.sleep(1)

    def run(self):
        # self._ip()
        # self.start_mitmproxy_server()
        # ua = random.choice(self.UA)
        # self.redis.set("UA", ua)
        try:
            self.driver.delete_all_cookies()
        except:
            pass

        try:
            name = random.choice(self.gjcs)
            try:
                self.driver.implicitly_wait(10)
                m = self.get_baidu_index(name)
                if m == 0:
                    print(m)
                    self.driver.quit()
                    return
            except Exception as f:
                print(f)
                self.driver.quit()
                return
            urls = self.driver.find_elements_by_xpath('//span[@class="c-showurl"]')
            if not urls:
                # self.start_mitmproxy_server()
                # time.sleep(4)
                self.driver.refresh()
            self.sub_hua_dong()
            time.sleep(random.randint(1, 4))
            self.sup_hua_dong()
            self.driver.implicitly_wait(5)
            self.bak(name)
            self.chear_chrom_data()
        except Exception as f:
            pass
        print("结束")
        self.driver.quit()


def run_app(Cellphone_id, Mitmproxy_port, Appium_port):
    # hk = str(Cellphone_id).split(":")[1]
    # if hk:
    #     if int(hk) == 62001:
    #         Mitmproxy_port = 8080
    #     else:
    #         k = int(hk) - 62025
    #         Mitmproxy_port += 1 + int(k)
    # Cellphone_id: 模拟器ID
    # Mitmproxy_port: mitmproxy端口号
    try:
        # 启动之前先查看端口是否占用，如果占用就杀死对应进程
        p = os.popen('netstat -aon|findstr "{}"'.format(Appium_port))
        p2 = p.read()
        for i in list(filter(lambda x: int(x) != 0, set(
                sum(list(map(lambda x: re.compile("(\d{1,5})$").findall(x), str(p2).split("\n")[0:-1])), [])))):
            print("结束Appium服务：端口号：", i)
            subprocess.Popen('taskkill -PID {} -F'.format(i))
        # 启动Appium服务
        host = '127.0.0.1'
        bootstrap_port = str(Appium_port + 1)
        cmd = 'appium -a ' + host + ' -p ' + str(Appium_port) + ' -bp ' + str(
            bootstrap_port + " -U " + str(Cellphone_id))
        print(Cellphone_id, "|||", cmd)
        subprocess.Popen(cmd, shell=True,
                         stdout=open('C:\\Users\\asus\\Desktop\\vps3\\appium_log\\' + str(Appium_port) + '.log', 'a'),
                         stderr=subprocess.STDOUT)
        while True:
            try:
                print("Cellphone_id: ", Cellphone_id, "  Mitmproxy_port: ", Mitmproxy_port, "  Appium_port:",
                      Appium_port)
                # 启动程序
                time.sleep(random.randint(1, 4))
                mians = Chrom_Run(Cellphone_id, Mitmproxy_port, Appium_port)
                mians.run()
                # name="name"
                # mians.get_baidu_index(name)
                print("一次点击完成")
            except:
                pass
    except Exception as f:
        print(f)


if __name__ == "__main__":
    # 结束之前的adb服务
    subprocess.Popen('adb kill-server')
    time.sleep(1)
    subprocess.Popen('adb start-server')
    time.sleep(1)
    # 结束之前的夜神模拟器
    subprocess.Popen('nox -quit')
    time.sleep(0.2)
    for i in range(1, 5):
        subprocess.Popen('nox -clone:Nox_{} -quit'.format(str(i)))
        time.sleep(0.2)
    time.sleep(5)
    # 重新启动夜神模拟器
    for i in range(1, 5):
        phone = random.randint(18511223344, 18711223344)
        subprocess.Popen('Nox.exe -clone:Nox_{} -phoneNumber:{}'.format(str(i), phone))
        time.sleep(10)
    time.sleep(10)
    p = os.popen("adb devices")
    x = str(p.read()).split("\n")[1:]
    Cellphone_ids = []
    for i in x:
        if i != "":
            x = str(i).split("\t")[0]
            if "device" in str(i).split("\t")[1]:
                Cellphone_ids.append(x)
    print(Cellphone_ids)
    pools = Pool()
    # # 创建进程池
    while True:
        try:
            for Cellphone_id, mitmproxy_port, Appium_port in zip(Cellphone_ids, range(8080, 8088),
                                                                 range(4723, 8080, 2)):
                pools.apply_async(run_app, args=(Cellphone_id, mitmproxy_port, Appium_port))
            pools.close()
            pools.join()
        except:
            pass
    #
    #
    # desired_process=[]
    #
    # #加载desied进程
    # for Cellphone_id, mitmproxy_port, Appium_port in zip(Cellphone_ids, range(8080, 8088), range(4723, 8080, 2)):
    #     desired=multiprocessing.Process(target=run_app,args=(Cellphone_id, mitmproxy_port, Appium_port))
    #     desired_process.append(desired)
    #
    # if __name__ == '__main__':
    #     # 启动多设备执行测试
    #     for desired in desired_process:
    #         desired.start()
    #     for desired in desired_process:
    #         desired.join()
