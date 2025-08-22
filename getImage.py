import requests
import pandas as pd
import datetime
import os
work_dir = os.path.dirname(__file__)
# 获取图片名称
def get_image_name(url):
    if 'ExportFile' in url:
        parts = url.split('/')
        if len(parts) > 0:
            return parts[-1]
    return None
def download_image(url):
    if not url:
        print("URL不能为空")
        return
    image_name = get_image_name(url)
    save_path = os.path.join(work_dir,'images', image_name)
    os.makedirs(os.path.dirname(work_dir), exist_ok=True)
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"图片已成功下载到 {save_path}")
    else:
        print("请求失败，状态码：", response.status_code)

# 示例使用
image_url = "https://cdn.customily.com/ExportFile/Benson/dd45ee2d-7876-41d8-a289-1e003b87593c.png"  # 替换为实际的图片URL
file_name = "image2.jpg"  # 保存的文件名
download_image(image_url)