# 简单数据分析案例，太简单了，直接上代码：这里统计了房屋的面积，价格的平均值，标准差，并用直方图来显示结果
 

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 13:07:02 2018

@author: Jun
"""

import numpy
import matplotlib.pyplot as plt

# 读取 house.csv 文件中价格和面积列
price, size = numpy.loadtxt(open('house.csv',encoding='ISO-8859-1') ,delimiter='|', usecols=(1, 2), unpack=True,)

# 求价格和面积的平均值
price_mean = numpy.mean(price)
size_mean = numpy.mean(size)
print("平均价格为：(万元)", price_mean)
print("平均面积为：(平方米)", size_mean)

# 求价格和面积的方差
#price_var = numpy.var(price)
price_var = numpy.std(price)
#size_var = numpy.var(size)
size_var = numpy.std(size)
print("价格的标准差为：(万元)", price_var)
print("面积的标准差为：", size_var)

price, size = numpy.loadtxt(open('house.csv',encoding='ISO-8859-1'), delimiter='|', usecols=(1, 2), unpack=True)
plt.figure()
plt.subplot(211)
plt.title("/10000RMB")
plt.hist(price, bins=20)

plt.subplot(212)
plt.xlabel("/m**2")

plt.hist(size, bins=20)
plt.show()
