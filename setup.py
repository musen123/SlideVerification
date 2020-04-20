"""
============================
Author:柠檬班-木森
Time:2020/4/20   17:50
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
============================
"""

import setuptools
from distutils.core import setup


"""
setup函数各参数详解：
>>python setup.py --help
  --name              包名称
  --version (-V)      包版本
  --author            程序的作者
  --author_email      程序的作者的邮箱地址
  --maintainer        维护者
  --maintainer_email  维护者的邮箱地址
  --url               程序的官网地址
  --license           程序的授权信息
  --description       程序的简单描述
  --long_description  程序的详细描述
  --platforms         程序适用的软件平台列表
  --classifiers       程序的所属分类列表
  --keywords          程序的关键字列表
  --packages  需要打包的目录列表
  --py_modules  需要打包的python文件列表
  --download_url  程序的下载地址
  --cmdclass  
  --data_files  打包时需要打包的数据文件，如图片，配置文件等
  --scripts  安装时需要执行的脚步列表

setup.py打包命令各参数详解：
>>python setup.py --help-commands
  --python setup.py build     # 仅编译不安装
  --python setup.py install    #安装到python安装目录的lib下
  --python setup.py sdist      #生成压缩包(zip/tar.gz)
  --python setup.py bdist_wininst  #生成NT平台安装包(.exe)
  --python setup.py bdist_rpm #生成rpm包  


"""
setup(
    name='',
    version='v0.0.1',
    author='musen',
    maintainer_email='musen_nmb@qq.com',
    requires=[],
    py_modules=[],
    packages=setuptools.find_packages(),
)
