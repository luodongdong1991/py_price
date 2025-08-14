    
# 集合（set）是一种无序的、不重复的元素的集合。集合中的元素必须是不可变的，因此集合不能包含可变对象。



# 1. 使用{}创建空集合
s1 = {}
print(type(s1), s1)  # <class 'dict'> {}        


# 2. 使用set()函数创建空集合
s2 = set()
print(type(s2), s2)  # <class'set'> set()

    # 3. 使用set()函数创建非空集合
s3 = set([1, 2, 3, 2, 1])
print(type(s3), s3)  # <class'set'> {1, 2, 3}


# 4. 使用list转换为集合
s4 = set([1, 2, 3, 4, 5])
print(type(s4), s4)  # <class'set'> {1, 2, 3, 4, 5}

# 5. 使用元组转换为集合
s5 = set((1, 2, 3, 4, 5))
print(type(s5), s5)  # <class'set'> {1, 2, 3, 4, 5}

# 6. 使用字符串转换为集合
s6 = set("hello world")
# 7. 使用字典转换为集合
s7 = set({'a': 1, 'b': 2, 'c': 3})
print(type(s7), s7)  # <class'set'> {'a', 'c', 'b'}

# 8. 使用集合转换为集合
s8 = set(s4)
print(type(s8), s8)  # <class'set'> {1, 2, 3, 4, 5}

# 9. 使用range对象转换为集合
s9 = set(range(1, 6))
print(type(s9), s9)  # <class'set'> {1, 2, 3, 4, 5}

# 10. 使用迭代器转换为集合
s10 = set(iter([1, 2, 3, 4, 5]))
print(type(s10), s10)  # <class'set'> {1, 2, 3, 4, 5}

# 11. 使用生成器表达式转换为集合
s11 = set(x for x in [1, 2, 3, 4, 5])
print(type(s11), s11)  # <class'set'> {1, 2, 3, 4, 5}

# 12. 使用集合运算符进行集合操作
s12 = {1, 2, 3}
s13 = {3, 4, 5}
s14 = s12 | s13  # 并集
print(type(s14), s14)  # <class'set'> {1, 2, 3, 4, 5}

s15 = s12 & s13  # 交集
print(type(s15), s15)  # <class'set'> {3}

s16 = s12 - s13  # 差集
print(type(s16), s16)  # <class'set'> {1, 2}

# 13. 使用集合方法进行集合操作
s17 = {1, 2, 3}
s18 = {3, 4, 5}
s19 = s17.union(s18)  # 并集
print(type(s19), s19)  # <class'set'> {1, 2, 3, 4, 5}

s20 = s17.intersection(s18)  # 交集
print(type(s20), s20)  # <class'set'> {3}

s21 = s17.difference(s18)  # 差集
print(type(s21), s21)  # <class'set'> {1, 2}

# 14. 使用集合推导式进行集合操作            
# 15. 使用集合的内置函数进行集合操
# 16. 使用集合的高级特性进行集合操作