import random  # 导入 random 模块，用于生成随机数
import time  # 导入 time 模块，用于时间相关操作
import pyautogui  # 导入 pyautogui 模块，用于控制鼠标和键盘
from PIL import Image  # 导入 Image 模块，用于图像处理
from selenium.webdriver.support.wait import WebDriverWait  # 导入 WebDriverWait 类，用于等待元素加载
from selenium import webdriver  # 导入 webdriver 模块，用于自动化测试和控制浏览器
from selenium.webdriver.support import expected_conditions as EC  # 导入 EC 模块，用于预期条件判断
from selenium.webdriver.common.by import By  # 导入 By 类，用于定位元素

class FloatSlide(object):
    # 初始化方法
    def __init__(self):
        # 确定 url
        self.url = 'https://www.geetest.com/demo/slide-float.html'
        # 加载驱动
        self.driver = webdriver.Chrome()
        # 最大化窗口
        self.driver.maximize_window()
        # 显示等待
        self.wait = WebDriverWait(self.driver, 100)
        # 缺口图片保存位置
        self.gap_img = 'images/gap.png'
        # 完整图片保存位置
        self.intact_img = 'images/intact.png'

    # 加载图片并截取图片
    def load_img(self):
        # 加载网站
        self.driver.get(self.url)
        # 等待2秒
        time.sleep(2)
        # 点击按钮
        self.driver.find_element(By.CLASS_NAME, 'geetest_radar_tip').click()
        # 用显示判断，图片是否加载出来
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slicebg geetest_absolute"]'))
        )
        # 修改样式，获取缺口图片
        self.driver.execute_script('document.querySelectorAll("canvas")[1].style="opacity: 1; display: none;"')
        # 找到验证码图片的标签元素
        div_img = self.driver.find_element(By.CLASS_NAME, 'geetest_window')
        # 等待1秒
        time.sleep(1)
        # 缺口图片的保存位置
        div_img.screenshot(self.gap_img)
        # 修改样式，获取完整图片
        self.driver.execute_script('document.querySelectorAll("canvas")[2].style=""')
        # 完整图片的保存位置
        div_img.screenshot(self.intact_img)
        # 恢复样式
        self.driver.execute_script('document.querySelectorAll("canvas")[1].style="opacity: 1; display: block;"')

    # 对比验证图片，获取缺口位置
    def get_gap(self):
        # 加载缺口图片
        gap_img = Image.open(self.gap_img)
        # 加载完整图片
        intact_img = Image.open(self.intact_img)
        # 从第一个位置开始做对比
        left = 0
        # 嵌套循环做对比
        for x in range(0, gap_img.size[0]):
            for y in range(0, gap_img.size[1]):
                # 判断像素
                if not self.is_pixel_equal(gap_img, intact_img, x, y):
                    # 相同赋值给 left
                    left = x
                    # 不相同，返回 x 坐标
                    return left

    # 判断像素
    def is_pixel_equal(self, gap_img, intact_img, x, y):
        # 加载缺口图片位置
        pixel1 = gap_img.load()[x, y]
        # 加载完整图片位置
        pixel2 = intact_img.load()[x, y]
        # 打印图片位置
        # print(pixel1, pixel2)
        # 阈值
        threshold = 60
        # 对比 RGB
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            # 在阈值内相似返回 True
            return True
        # 不在阈值内不相似返回 False，缺口找到
        return False

    # 滑动滑块
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
        pyautogui.moveTo(offset_x + int(left * random.randint(17, 23) / 20), offset_y,duration=random.randint(20, 31) / 100)
        # 在当前 offset_y 的基础上增加一个随机值
        offset_y += random.randint(0, 8)
        # 将鼠标移动到偏移位置 (offset_x + int(left * 随机值), offset_y)
        pyautogui.moveTo(offset_x + int(left * random.randint(19, 21) / 20), offset_y,duration=random.randint(20, 40) / 100)
        # 在当前 offset_y 的基础上增加或减少一个随机值
        offset_y += random.randint(-3, 3)
        # 将鼠标移动到偏移位置 (left + offset_x + 随机值, offset_y)
        pyautogui.moveTo(left + offset_x + random.randint(-3, 3), offset_y,duration=0.5 + random.randint(-10, 10) / 100)
        # 在当前 offset_y 的基础上增加或减少一个随机值
        offset_y += random.randint(-2, 2)
        # 将鼠标移动到偏移位置 (left + offset_x + 随机值, offset_y)
        pyautogui.moveTo(left + offset_x + random.randint(-2, 2), offset_y, duration=0.5 + random.randint(-3, 3) / 100)
        # 松开鼠标左键，结束滑动操作
        pyautogui.mouseUp()
        # 等待3秒
        time.sleep(3)

    # 主函数
    def main(self):
        # 加载图片并截取图片
        self.load_img()
        # 对比验证图片，获取缺口位置
        left = self.get_gap()
        # 误差值
        left -= 6
        # 根据位置滑动滑块(测量一下浏览器左上角到滑块按钮的距离)
        x = 1260
        y = 490
        # 滑动滑块
        self.move_slide(x, y, left)

# 主程序
if __name__ == '__main__':
    # 创建了一个对象
    f = FloatSlide()
    # 调用 main 方法
    f.main()