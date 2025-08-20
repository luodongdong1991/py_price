import pandas as pd
import datetime
import os
import json
import sys
# 获取当前工作目录
work_dir = os.path.dirname(__file__)
# 定义表格名称
sheet_name = "Recovered_Sheet1"
# 运行时间
current_time = datetime.datetime.now().strftime('%m_%d_%H_%M_%S')
if getattr(sys, 'frozen', False):
    work_dir = os.path.dirname(sys.executable)
def get_excel_file(file_name,sheet_name,keep_default_na=False,dtype=str):
    try:
        file_path = os.path.join(work_dir, file_name)
        return pd.read_excel(file_path, sheet_name=sheet_name, keep_default_na=keep_default_na, dtype=dtype)
    except Exception as e:
        print(f"读取表格失败{file_path},{e}")
        return None
excle = get_excel_file("订单列表.xlsx", sheet_name)
def format_excle(excle):
    if excle is None:
        return None
    excle.columns = [i.strip() for i in excle.columns]
    # 商品中文名称 包含抠图
    # contains_koutu = excle['商品中文名称'].str.contains('抠图', na=False)
    # filtered_data = excle[contains_koutu]
    # 空值处理
    empty_list = excle[excle['交易编号'].str.len() == 0,'交易编号'].tolist()
    print(f"空值行数{len(empty_list)}")
    # for index,row in excle.iterrows():
       
    # save
    name = f"test_{current_time}.xlsx"
    file_path = os.path.join(work_dir,name)
    # excle.to_excel(file_path,sheet_name=sheet_name,index=False,engine='openpyxl')
excle = format_excle(excle)