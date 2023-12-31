import time # 导入 time 模块，用于时间相关操作
from PIL import Image # 导入 Image 模块，用于图像处理
from selenium import webdriver # 导入 webdriver 模块，用于自动化测试和控制浏览器
from selenium.webdriver import ActionChains # 导入 ActionChains 类，用于模拟用户操作
from selenium.webdriver.common.by import By # 导入 By 类，用于定位元素
from selenium.webdriver.support.wait import WebDriverWait # 导入 WebDriverWait 类，用于等待元素加载
from selenium.webdriver.support import expected_conditions as EC # 导入 EC 模块，用于预期条件判断
from chaojiying_Python.chaojiying import Chaojiying_Client # 引入超级鹰验证码识别 API 客户端

class Bili_login(object):
    # 初始法方法，用户名跟密码
    def __init__(self, username, password):
        # 加载驱动
        self.driver = webdriver.Chrome()
        # 窗口最大化
        self.driver.maximize_window()
        # 目标 url
        self.url = 'https://www.bilibili.com/'
        # 用户名
        self.username = username
        # 密码
        self.password = password
        # 显示等待，判断驱动是否加载出来
        self.wait = WebDriverWait(self.driver, 100)

    # 加载得到验证码图片
    def get_img(self):
        # 加载网站
        self.driver.get(self.url)
        # 等待2秒
        time.sleep(2)
        # 点击登录
        self.driver.find_element(By.CLASS_NAME, 'header-login-entry').click()
        # 显示等待，判断账号与密码输入框是否加载出来
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'login-pwd-wp')) # 注意方法里面要填元组
        )
        # 输入账号
        self.driver.find_element(By.XPATH, '//form[@class="tab__form"]/div[1]/input').send_keys(self.username)
        # 等待0.5秒
        time.sleep(0.5)
        # 输入密码
        self.driver.find_element(By.XPATH, '//form[@class="tab__form"]/div[3]/input').send_keys(self.username)
        # 点击登录
        self.driver.find_element(By.CLASS_NAME, 'btn_primary ').click()
        # 判断验证码元素是否加载出来
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img'))
        )
        # 保存验证码图片
        div_img = self.save_img()
        # 返回验证码图片
        return div_img

    # 下载验证码图片到本地
    def save_img(self):
        # 等待2秒
        time.sleep(2)
        # 截全屏图片
        self.driver.save_screenshot('images/back_img.png')
        # 获取验证码图片的元素
        div_img = self.driver.find_element(By.CLASS_NAME, 'geetest_panel_next')
        # 获取左上角的坐标，返回 x,y 的坐标
        location = div_img.location
        # 获取宽度和高度
        size = div_img.size
        # 获取左上角的坐标
        x1, y1 = int(location['x']), int(location['y'])
        # 获取右下角的坐标
        x2, y2 = x1 + size['width'], y1 + size['height']
        # 加载背景图
        back_img = Image.open('images/back_img.png')
        # 截图，截图建议电脑缩放比例为100%
        img = back_img.crop((x1, y1, x2, y2))
        # 保存图片
        img.save('images/验证码图片.png')
        # 返回验证码图片的元素
        return div_img

    # 点击文字做验证
    def click_font(self, loc_dic, div_img):
        # 循环依次点击
        for x, y in loc_dic.items():
            # 鼠标行为链
            action = ActionChains(self.driver)
            # 鼠标移动点击
            action.move_to_element_with_offset(div_img, int(x), int(y)).click().perform()
        # 等待1秒
        time.sleep(1)
        # 点击确定
        self.driver.find_element(By.CLASS_NAME, 'geetest_commit_tip').click()

    # 主逻辑处理
    def main(self):
        # 加载得到验证码图片
        div_img = self.get_img()
        # 用超级鹰识别位置
        chaojiying = Chaojiying_Client('替换超级鹰用户名', '替换超级鹰用户名的密码', '949117')
        # 本地图片文件路径
        im = open('images/验证码图片.png', 'rb').read()
        # 验证码类型
        log_list = chaojiying.PostPic(im, 9004)['pic_str'].split('|')
        # 处理坐标数据
        loc_dic = {i.split(',')[0]: i.split(',')[1] for i in log_list}
        # 打印位置坐标
        # print(loc_dic)
        # 点击图片内文字
        self.click_font(loc_dic, div_img)

# 主程序
if __name__ == '__main__':
    # 创建了一个对象
    b = Bili_login('123456', '123456')
    # 调用 main 方法
    b.main()