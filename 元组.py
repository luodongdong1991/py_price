
# 元组（Tuple）

# 元组是另一种有序列表，但是元组一旦定义就不能修改。元组用圆括号 () 表示，元素之间用逗号隔开。

# 定义元组
tup1 = (1, 2, 3, 4, 5)
tup2 = ('apple', 'banana', 'cherry')
tup3 = (True, False, True)

# 访问元组元素
print(tup1[0])  # 输出 1
print(tup2[1])  # 输出 'banana'
print(tup3[2])  # 输出 True
# 修改元组元素
# 元组一旦定义就不能修改，所以不能对元组元素进行修改。  
# 错误方式：
# tup1[0] = 100  # 错误，不能修改元组元素
# 正确方式：
# 重新定义一个新的元组
tup1 = (100, 2, 3, 4, 5)
print(tup1)  # 输出 (100, 2, 3, 4, 5) 
len(tup1)  # 输出 5
c = tup1 + tup2  # 连接元组
print(c)  # 输出 (100, 2, 3, 4, 5, 'apple', 'banana', 'cherry')
for x in (1, 2, 3): 
    print (x,end="|")