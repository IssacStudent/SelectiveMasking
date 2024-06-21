a=[1,2,3,4,5]
b=[2,4,6,8,10]

for aa, bb in zip(a, b):
    print("aa: ", aa)
    print("bb: ", bb)
    print("a:", a)
    a = [10,20,30,40,50]
import matplotlib.pyplot as plt

# 假设这是你的数据列表
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

# 创建一个图形实例
plt.figure()

# 画出数据的折线图
plt.plot(data)

# 添加标题
plt.title('Line Graph Example')

# 添加X轴和Y轴的标签
plt.xlabel('Index')
plt.ylabel('Value')

# 显示图形
plt.show()
