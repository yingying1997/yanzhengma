import random # 导入 random 模块，用于生成随机数
import time # 导入 time 模块，用于添加时间延迟
import cv2 # 导入 OpenCV 模块，用于图像处理
import pyautogui # 导入 pyautogui 模块，用于模拟鼠标和键盘操作
from selenium.webdriver.chrome.options import Options # 导入 ChromeOptions 类，用于配置 Chrome 浏览器选项
from selenium.webdriver.support.wait import WebDriverWait # 导入 WebDriverWait 类，用于等待条件
from selenium import webdriver # 导入 webdriver 模块，用于控制浏览器
from selenium.webdriver.support import expected_conditions as EC # 导入 expected_conditions 模块，用于指定预期条件
from selenium.webdriver.common.by import By # 导入 By 模块，用于指定元素定位方式
from PIL import Image # 导入 Image 模块，用于图像处理
import urllib.request # 导入 urllib.request 模块，用于进行网络请求

class JinDong_Logic(object):
    # 初始化操作
    def __init__(self, username, password):
        # 确定 url
        self.url = 'https://passport.jd.com/new/login.aspx'
        # 账号
        self.username = username
        # 密码
        self.password = password
        # 创建 Options 对象，用于配置浏览器选项
        options = Options()
        # 连接浏览器到指定的调试地址
        options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
        # 加载驱动
        self.driver = webdriver.Chrome(options=options)
        # 窗口最大化
        self.driver.maximize_window()
        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)
        # 设置图片保存位置
        # 有缺口的背景图片
        self.bg_img = 'images/bg_img.png'
        # 缺口小图片
        self.gap_img = 'images/gap_img.png'

    # 获取缺口图片
    def login(self):
        # 加载 url
        self.driver.get(self.url)
        # 等待1秒
        time.sleep(1)
        # 切换登录方式
        self.driver.find_element(By.CLASS_NAME, 'login-tab-r').click()
        # 输入账号
        self.driver.find_element(By.ID, 'loginname').send_keys(self.username)
        # 输入密码
        self.driver.find_element(By.ID, 'nloginpwd').send_keys(self.password)
        # 等待0.5秒
        time.sleep(0.5)
        # 点击登录按钮
        self.driver.find_element(By.ID, 'loginsubmit').click()
        # 显示等待判断图片是否加载出来
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'JDJRV-slide '))
        )
        # 获取背景图片（向图片链接发请求，获取图片)
        bg_img_url = self.driver.find_element(By.XPATH, '//div[@class="JDJRV-bigimg"]/img').get_attribute('src')
        # 保存图片
        urllib.request.urlretrieve(bg_img_url, self.bg_img)
        # 获取缺口图片
        gap_img_url = self.driver.find_element(By.XPATH, '//div[@class="JDJRV-smallimg"]/img').get_attribute('src')
        # 保存图片
        urllib.request.urlretrieve(gap_img_url, self.gap_img)
        # 修改背景图片的尺寸
        im = Image.open(self.bg_img)
        # 重新设置图片尺寸
        image = im.resize((278, 108))
        # 保存图片
        image.save('images/1.png')
        # 修改缺口图片的尺寸
        im1 = Image.open(self.gap_img)
        # 重新设置图片尺寸
        image1 = im1.resize((39, 39))
        # 保存图片
        image1.save('images/2.png')
        # 获取两张图片，计算缺口位置，识别距离
        left = self.identify_gap('images/1.png', 'images/2.png')
        # 根据位置滑动滑块(测量一下浏览器左上角到滑块按钮的距离)
        x, y = 1485, 455
        # 滑动
        self.move_slide(x, y, left)

    # 计算缺口位置
    def identify_gap(self, bg_image, tp_image, out="images/new_image.png"):
        """
            通过cv2计算缺口位置
            :param bg_image: 有缺口的背景图片文件
            :param tp_image: 缺口小图文件图片文件
            :param out: 绘制缺口边框之后的图片
            :return: 返回缺口位置
            """
        # 读取背景图片和缺口图片
        bg_img = cv2.imread(bg_image)  # 背景图片
        tp_img = cv2.imread(tp_image)  # 缺口图片
        # 识别图片边缘
        # 因为验证码图片里面的目标缺口通常是有比较明显的边缘 所以可以借助边缘检测算法结合调整阈值来识别缺口
        # 目前应用比较广泛的边缘检测算法是Canny John F.Canny在1986年所开发的一个多级边缘检测算法 效果挺好的
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        print(bg_edge, tp_edge)
        # 转换图片格式
        # 得到了图片边缘的灰度图，进一步将其图片格式转为RGB格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 缺口匹配
        # 一幅图像中找与另一幅图像最匹配(相似)部分 算法：cv2.TM_CCOEFF_NORMED
        # 在背景图片中搜索对应的缺口
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        # res为每个位置的匹配结果，代表了匹配的概率，选出其中「概率最高」的点，即为缺口匹配的位置
        # 从中获取min_val，max_val，min_loc，max_loc分别为匹配的最小值、匹配的最大值、最小值的位置、最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(out, bg_img)  # 保存在本地

        # 返回缺口的X坐标
        return tl[0]

    # 滑动函数
    def move_slide(self, offset_x, offset_y, left):
        # pip install pyautogui 导入 pyautogui 模块，用于控制鼠标和键盘
        # 将鼠标移动到指定位置 (offset_x, offset_y)
        pyautogui.moveTo(offset_x, offset_y, duration=0.1 + random.uniform(0, 0.1 + random.randint(1, 100) / 100))
        # 按下鼠标，准备开始滑动
        pyautogui.mouseDown()
        # 在当前 offset_y 的基础上增加一个随机值
        offset_y += random.randint(9, 19)
        # 将鼠标移动到偏移位置 (offset_x + int(left * 随机值), offset_y)
        pyautogui.moveTo(offset_x + int(left * random.randint(15, 25) / 20), offset_y, duration=0.28)
        # 在当前 offset_y 的基础上减少一个随机值
        offset_y += random.randint(-9, 0)
        # 将鼠标移动到偏移位置 (offset_x + int(left * 随机值), offset_y)
        pyautogui.moveTo(offset_x + int(left * random.randint(17, 23) / 20), offset_y,
                         duration=random.randint(20, 31) / 100)
        # 在当前 offset_y 的基础上增加一个随机值
        offset_y += random.randint(0, 8)
        # 将鼠标移动到偏移位置 (offset_x + int(left * 随机值), offset_y)
        pyautogui.moveTo(offset_x + int(left * random.randint(19, 21) / 20), offset_y,
                         duration=random.randint(20, 40) / 100)
        # 在当前 offset_y 的基础上增加或减少一个随机值
        offset_y += random.randint(-3, 3)
        # 将鼠标移动到偏移位置 (left + offset_x + 随机值, offset_y)
        pyautogui.moveTo(left + offset_x + random.randint(-3, 3), offset_y,
                         duration=0.5 + random.randint(-10, 10) / 100)
        # 在当前 offset_y 的基础上增加或减少一个随机值
        offset_y += random.randint(-2, 2)
        # 将鼠标移动到偏移位置 (left + offset_x + 随机值, offset_y)
        pyautogui.moveTo(left + offset_x + random.randint(-2, 2), offset_y, duration=0.5 + random.randint(-3, 3) / 100)
        # 松开鼠标左键，结束滑动操作
        pyautogui.mouseUp()
        # 等待3秒
        time.sleep(3)

# 主程序
if __name__ == '__main__':
    # 创建对象
    l = JinDong_Logic('123', 'abcd')
    # 调用 login 方法
    l.login()