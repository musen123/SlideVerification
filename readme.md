# 滑动验证码识别模块V0.0.1

基于opencv-python模块实现的滑动验证码模块，目前只实现了滑动验证，后续会持续更新其他类型验证码的解决方案





- 使用案例如下：

```python
from selenium import webdriver
from slideVerfication import SlideVerificationCode

# 访问目标页面
self.driver = webdriver.Chrome()      
self.driver.get(url="https://www.baidu.com/xxxxxx/")
driver.switch_to.frame(if_ele)
# 获取背景图,滑动图片的节点
background_ele = driver.find_element_by_xpath("//img[@id='slideBg']")
slider_ele = driver.find_element_by_xpath("//img[@id='slideBlock']")
# 获取滑动块元素
slide_element = driver.find_element_by_id('tcaptcha_drag_button')

#1、创建一个验证对象
sv = SlideVerificationCode()
#2、获取滑动距离
distance = sv.get_slide_distance(slider_ele, background_ele)
#3、误差校准(滑动距离*背景图的缩放比，减去滑块在背景图的左边距)
distance = distance * (280.0 / 680.0) - 31
#4、滑动验证码进行验证
sv.slide_verification(driver, slide_element, distance)
```



