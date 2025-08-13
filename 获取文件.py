# extract_I.py
from pathlib import Path
import openpyxl

FILE = Path(r"D:\实在RPA\图片识别\images.xlsx")


def get_i_links():
    """返回 I 列非空链接，跳过首行"""
    if not FILE.exists():
        return {"result": []}

    ws = openpyxl.load_workbook(FILE, data_only=True).active
    links = [
        str(cell.value).strip()
        for cell in ws["I"][1:]  # 跳过首行
        if cell.value and str(cell.value).strip()
    ]
    return {"result": links}


# 当脚本直接运行时，也可打印查看
if __name__ == "__main__":
    print(get_i_links())
