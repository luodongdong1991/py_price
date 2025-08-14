import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_images(url, save_folder='images'):
    # 创建保存图片的文件夹
    os.makedirs(save_folder, exist_ok=True)

    # 设置请求头，伪装浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': url  # 有些网站要求加 Referer
    }

    # 请求网页内容
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        print(f"请求网页时出错: {e}")
        return

    # 解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有图片标签
    img_tags = soup.find_all('img')

    for img in img_tags:
        # 获取图片的 src 或 data-src 属性
        img_url = img.get('src') or img.get('data-src') or img.get('srcset')
        if not img_url:
            continue

        # 转换相对路径为绝对路径
        img_url = urljoin(url, img_url.split()[0])  # 去除 srcset 中多个地址

        try:
            # 请求图片内容
            img_response = requests.get(img_url, headers=headers, timeout=10)
            img_response.raise_for_status()

            # 获取文件扩展名
            ext = os.path.splitext(img_url)[1]
            if not ext or len(ext) > 5:
                ext = '.jpg'  # 默认扩展名

            # 保存图片
            file_path = os.path.join(save_folder, f'image_{img_url.split("/")[-1]}{ext}')
            with open(file_path, 'wb') as f:
                f.write(img_response.content)
            print(f"[✓] 下载成功：{img_url}")
        except Exception as e:
            print(f"[✗] 下载失败：{img_url}，原因：{e}")

# 示例用法
if __name__ == "__main__":
    target_url = 'https://hypershell.tech/en-us'  # 替换为实际要抓取的网页 URL
    download_images(target_url)