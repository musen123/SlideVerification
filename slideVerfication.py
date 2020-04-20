"""
Author:柠檬班-木森
Time:2020/4/15   11:11
E-mail:musen_nmb@qq.com
本模块专门用来处理滑动验证码的问题，

"""

from selenium.webdriver import ActionChains
import random, time, os
import cv2
from PIL import Image as Im
import numpy as np
import requests


class SlideVerificationCode():
    """滑动验证码破解"""

    def __init__(self, count=5, save_image=False):
        """
        :param count: 验证重试的次数，默认为5次
        :param save_image: 是否保存验证过程中的图片，默认不保存
        """
        self.count = count
        self.save_image = save_image

    def slide_verification(self, driver, slide_element, distance):
        """
        :param driver: driver对象
        :type driver:webdriver.Chrome
        :param slide_element: 滑块的元组
        :type slider_ele: WebElement
        :param distance:  滑动的距离
        :type: int
        :return:
        """
        # 获取滑动前页面的url地址
        start_url = driver.current_url
        print("需要滑动的距离为：", distance)
        # 根据滑动距离生成滑动轨迹
        locus = self.get_slide_locus(distance)
        print("生成的滑动轨迹为:{}，轨迹的距离之和为{}".format(locus, distance))
        # 按下鼠标左键
        ActionChains(driver).click_and_hold(slide_element).perform()
        time.sleep(0.5)
        # 遍历轨迹进行滑动
        for loc in locus:
            time.sleep(0.01)
            ActionChains(driver).move_by_offset(loc, random.randint(-5, 5)).perform()
            ActionChains(driver).context_click(slide_element)
        # 释放鼠标
        ActionChains(driver).release(on_element=slide_element).perform()
        # 判读是否验证通过，未通过的情况下重新滑动
        time.sleep(2)
        # 滑动之后再次获取url地址
        end_url = driver.current_url
        # 滑动失败的情况下，重试5次
        if start_url == end_url and self.count > 0:
            print("第{}次验证失败，开启重试")
            self.count -= 1
            self.slide_verification(driver, slide_element, distance)


    def onload_save_img(self, url, filename="image.png"):
        """
        下载图片保存
        :param url:图片地址
        :param filename: 保存的图片名
        :return:
        """
        try:
            response = requests.get(url=url)
        except(requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError)as e:
            print("图片下载失败")
            raise e
        else:
            with open(filename, "wb") as f:
                f.write(response.content)

    def get_element_slide_distance(self, slider_ele, background_ele, correct=0):
        """
        根据传入滑块，和背景的节点，计算滑块的距离

        该方法只能计算 滑块和背景图都是一张完整图片的场景，
        如果是通过多张小图拼接起来的背景图，该方法不适用，后续会补充一个专门针对处理该场景的方法
        :param slider_ele: 滑块图片的节点
        :type slider_ele: WebElement
        :param background_ele: 背景图的节点
        :type background_ele:WebElement
        :param correct:滑块缺口截图的修正值，默认为0,调试截图是否正确的情况下才会用
        :type: int
        :return: 背景图缺口位置的X轴坐标位置（缺口图片左边界位置）
        """
        # 获取验证码的图片
        slider_url = slider_ele.get_attribute("src")
        background_url = background_ele.get_attribute("src")
        # 下载验证码背景图,滑动图片
        slider = "slider.jpg"
        background = "background.jpg"
        self.onload_save_img(slider_url, slider)
        self.onload_save_img(background_url, background)
        # 读取进行色度图片，转换为numpy中的数组类型数据，
        slider_pic = cv2.imread(slider, 0)
        background_pic = cv2.imread(background, 0)
        # 获取缺口图数组的形状 -->缺口图的宽和高
        width, height = slider_pic.shape[::-1]
        # 将处理之后的图片另存
        slider01 = "slider01.jpg"
        background_01 = "background01.jpg"
        cv2.imwrite(background_01, background_pic)
        cv2.imwrite(slider01, slider_pic)
        # 读取另存的滑块图
        slider_pic = cv2.imread(slider01)
        # 进行色彩转换
        slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
        # 获取色差的绝对值
        slider_pic = abs(255 - slider_pic)
        # 保存图片
        cv2.imwrite(slider01, slider_pic)
        # 读取滑块
        slider_pic = cv2.imread(slider01)
        # 读取背景图
        background_pic = cv2.imread(background_01)
        # 比较两张图的重叠区域
        result = cv2.matchTemplate(slider_pic, background_pic, cv2.TM_CCOEFF_NORMED)
        # 获取图片的缺口位置
        top, left = np.unravel_index(result.argmax(), result.shape)
        # 背景图中的图片缺口坐标位置
        print("当前滑块的缺口位置：", (left, top, left + width, top + height))

        # 判读是否需求保存识别过程中的截图文件
        if self.save_image:
            # 截图滑块保存
            # 进行坐标修正
            loc = (left + correct, top + correct, left + width - correct, top + height - correct)
            self.image_crop(background, loc)
        else:
            # 删除识别过程中保存的临时文件
            os.remove(slider01)
            os.remove(background_01)
            os.remove(slider)
            os.remove(background)

        # 返回需要移动的位置距离
        return left

    def get_image_slide_dictance(self,slider_image, background_image,correct=0):
        """
        根据传入滑块，和背景的图片，计算滑块的距离

        该方法只能计算 滑块和背景图都是一张完整图片的场景，
        如果是通过多张小图拼接起来的背景图，该方法不适用，后续会补充一个专门针对处理该场景的方法
        :param slider_iamge: 滑块图的图片
        :type slider_image: str
        :param background_image: 背景图的图片
        :type background_image: str
        :param correct:滑块缺口截图的修正值，默认为0,调试截图是否正确的情况下才会用
        :type: int
        :return: 背景图缺口位置的X轴坐标位置（缺口图片左边界位置）
        """
        # 读取进行色度图片，转换为numpy中的数组类型数据，
        slider_pic = cv2.imread(slider_image, 0)
        background_pic = cv2.imread(background_image, 0)
        # 获取缺口图数组的形状 -->缺口图的宽和高
        width, height = slider_pic.shape[::-1]
        # 将处理之后的图片另存
        slider01 = "slider01.jpg"
        background_01 = "background01.jpg"
        cv2.imwrite(background_01, background_pic)
        cv2.imwrite(slider01, slider_pic)
        # 读取另存的滑块图
        slider_pic = cv2.imread(slider01)
        # 进行色彩转换
        slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
        # 获取色差的绝对值
        slider_pic = abs(255 - slider_pic)
        # 保存图片
        cv2.imwrite(slider01, slider_pic)
        # 读取滑块
        slider_pic = cv2.imread(slider01)
        # 读取背景图
        background_pic = cv2.imread(background_01)
        # 比较两张图的重叠区域
        result = cv2.matchTemplate(slider_pic, background_pic, cv2.TM_CCOEFF_NORMED)
        # 获取图片的缺口位置
        top, left = np.unravel_index(result.argmax(), result.shape)
        # 背景图中的图片缺口坐标位置
        print("当前滑块的缺口位置：", (left, top, left + width, top + height))
        # 判读是否需求保存识别过程中的截图文件
        if self.save_image:
            # 截图滑块保存
            # 进行坐标修正
            loc = (left + correct, top + correct, left + width - correct, top + height - correct)
            self.image_crop(background_image, loc)
        else:
            # 删除识别过程中保存的临时文件
            os.remove(slider01)
            os.remove(background_01)
        # 返回需要移动的位置距离
        return left

    @classmethod
    def get_slide_locus(self, distance):
        """
        根据移动坐标位置构造移动轨迹,前期移动慢，中期块，后期慢
        :param distance:移动距离
        :type:int
        :return:移动轨迹
        :rtype:list
        """
        remaining_dist = distance
        locus = []
        while remaining_dist > 0:
            ratio = remaining_dist / distance
            if ratio < 0.2:
                # 开始阶段移动较慢
                span = random.randint(2, 8)
            elif ratio > 0.8:
                # 结束阶段移动较慢
                span = random.randint(5, 8)
            else:
                # 中间部分移动快
                span = random.randint(10, 16)
            locus.append(span)
            remaining_dist -= span
        return locus

    def image_crop(self, image, location, new_name="new_image.png"):
        """
        对图片的指定位置进行截图
        :param image: 被截取图片的坐标位置
        :param location:需要截图的坐标位置：（left,top,right,button）
        :type location: tuple
        :return:
        """
        # 打开图片
        image = Im.open(image)
        # 切割图片
        imagecrop = image.crop(location)
        # 保存图片
        imagecrop.save(new_name)
