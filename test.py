
class MyClass:
    def __init__(self, options):
        self.name = options["name"]  # 实例变量 name
        self.age = options.get("age", 0)  # 实例变量 age，默认值为 0

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def update_name(self, new_name):
        self.name = new_name  # 修改实例变量 name
        print(f"My name has been updated to {self.name}.")

# 创建实例
my_object = MyClass({"name": "join", "age": 25})

# 调用方法
my_object.say_hello()  # 输出: Hello, my name is join and I am 25 years old.

# 更新实例变量
my_object.update_name("John")  # 输出: My name has been updated to John.
my_object.say_hello()  # 输出: Hello, my name is John and I am 25 years old.