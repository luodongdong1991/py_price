import tkinter as tk

# 定义一个函数，当按钮被点击时调用
def on_button_click():
    message = "Hello, Tkinter!"
    text_box.delete(1.0, tk.END)  # 清空文本框
    text_box.insert(tk.END, message)  # 在文本框中显示消息

# 创建主窗口
root = tk.Tk()
root.title("Tkinter 示例应用")

# 创建一个按钮
button = tk.Button(root, text="点击我", command=on_button_click)
button.pack()

# 创建一个文本框
text_box = tk.Text(root, height=5, width=30)
text_box.pack()

# 启动事件循环
root.mainloop()