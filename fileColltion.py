# mymodule.py

def greet(name):
    print(f"Hello, {name}!")

def add(a, b):
    return a + b

# 定义一个变量
message = "Welcome to my module!"
class MyClass: 
    def __init__(self, name): 
         self.name = name 
    # 定义一个函数
    def my_function(self, x): 
        print(self.name + " says: " + message) 
        return x * x 
a = MyClass("John") 
print(a.my_function(5)) 