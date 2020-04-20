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
        start_url = driver.current_url
        print("需要滑动的距离为：", distance)
        locus = self.get_slide_locus(distance)
        print("生成的滑动轨迹为:{}，轨迹的距离之和为{}".format(locus, distance))
        ActionChains(driver).click_and_hold(slide_element).perform()
        time.sleep(0.5)
        for loc in locus:
            time.sleep(0.01)
            ActionChains(driver).move_by_offset(loc, random.randint(-5, 5)).perform()
            ActionChains(driver).context_click(slide_element)
        ActionChains(driver).release(on_element=slide_element).perform()
        time.sleep(2)
        end_url = driver.current_url
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
        slider_url = slider_ele.get_attribute("src")
        background_url = background_ele.get_attribute("src")
        slider = "slider.jpg"
        background = "background.jpg"
        self.onload_save_img(slider_url, slider)
        self.onload_save_img(background_url, background)
        slider_pic = cv2.imread(slider, 0)
        background_pic = cv2.imread(background, 0)
        width, height = slider_pic.shape[::-1]
        slider01 = "slider01.jpg"
        background_01 = "background01.jpg"
        cv2.imwrite(background_01, background_pic)
        cv2.imwrite(slider01, slider_pic)
        slider_pic = cv2.imread(slider01)
        slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
        slider_pic = abs(255 - slider_pic)
        cv2.imwrite(slider01, slider_pic)
        slider_pic = cv2.imread(slider01)
        background_pic = cv2.imread(background_01)
        result = cv2.matchTemplate(slider_pic, background_pic, cv2.TM_CCOEFF_NORMED)
        top, left = np.unravel_index(result.argmax(), result.shape)
        print("当前滑块的缺口位置：", (left, top, left + width, top + height))
        if self.save_image:
            loc = (left + correct, top + correct, left + width - correct, top + height - correct)
            self.image_crop(background, loc)
        else:
            os.remove(slider01)
            os.remove(background_01)
            os.remove(slider)
            os.remove(background)
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
        slider_pic = cv2.imread(slider_image, 0)
        background_pic = cv2.imread(background_image, 0)
        width, height = slider_pic.shape[::-1]
        slider01 = "slider01.jpg"
        background_01 = "background01.jpg"
        cv2.imwrite(background_01, background_pic)
        cv2.imwrite(slider01, slider_pic)
        slider_pic = cv2.imread(slider01)
        slider_pic = cv2.cvtColor(slider_pic, cv2.COLOR_BGR2GRAY)
        slider_pic = abs(255 - slider_pic)
        cv2.imwrite(slider01, slider_pic)
        slider_pic = cv2.imread(slider01)
        background_pic = cv2.imread(background_01)
        result = cv2.matchTemplate(slider_pic, background_pic, cv2.TM_CCOEFF_NORMED)
        top, left = np.unravel_index(result.argmax(), result.shape)
        print("当前滑块的缺口位置：", (left, top, left + width, top + height))
        if self.save_image:
            loc = (left + correct, top + correct, left + width - correct, top + height - correct)
            self.image_crop(background_image, loc)
        else:
            os.remove(slider01)
            os.remove(background_01)
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
                span = random.randint(2, 8)
            elif ratio > 0.8:
                span = random.randint(5, 8)
            else:
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
        image = Im.open(image)
        imagecrop = image.crop(location)
        imagecrop.save(new_name)
