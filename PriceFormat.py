import pandas as pd
import datetime
import os
import json
import sys
# pkg  pyinstaller --onefile --add-data="D:\ldd-desk\myhtml\python\excle\**;excle/"  PriceFormat.py
# 运行时间
current_time = datetime.datetime.now().strftime('%m_%d_%H_%M_%S')
# 脚本所在目录
work_dir = os.path.dirname(__file__)
script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
if getattr(sys, 'frozen', False):
    work_dir = os.path.dirname(sys.executable)
    script_dir = work_dir
# 运行数据配置  data数据表路劲以及sheet名称  price 价格表路劲以及sheet名称
config = {}
# 读取配置文件
config_path = os.path.join(script_dir,"excle","config.json")
with open(config_path, 'r', encoding='utf-8') as file:
    config = json.load(file)
    # print(config)
# 数据表中订单列的名称-不区分国家
ex_order_id = config['data1']['订单编号表头'] #订单ID
ex_one_more_price = config['price1']['多1个的价格']#多个品类的价格
ex_one_price = config['price1']['总价_1个'] #单个产品价格
ex_data_price = config['data1']['写入价格表头'] #数据中的价格
ex_sku = config['data1']['sku_col_name'] #数据中的sku
ex_qty = config['data1']['数量表头']  #数据中的数量
ex_price_sku = "客户sku" #价格表中的sku
ex_overseas_attribute = config['data1']['Tracking_Company']#海外sku判断条件
# 数据表中订单列的名称-不区分国家begin
# 格式化产品价格
def format_price():
    result = {}
    list = price1_1[price1_1[ex_price_sku] != '']
    for index, row in list.iterrows():
        result[row[ex_price_sku]] = row["价格"]
    return result
# 读取表格 def  =========================================
def get_excel_file(file_name,sheet_name,keep_default_na=False,dtype=str):
    try:
        file_path = os.path.join(script_dir, "excle", file_name)
        return pd.read_excel(file_path, sheet_name=sheet_name, keep_default_na=keep_default_na, dtype=dtype)
    except Exception as e:
        print(f"读取表格失败{file_path},{e}")
        write_log(f"读取表格失败{file_path},{e}")
        return None
# 删除文件
def del_file():
    file_name = config['other']['日志文件']
    file_path = os.path.join(script_dir,"excle", file_name)
    if os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('')  
del_file()    
# 日志 def  =========================================
def write_log(log_str):
    file_name = config['other']['日志文件']
    LOG_FILE = os.path.join(work_dir,"excle", file_name)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{timestamp}] {log_str}\n'
    # 如果目录不存在就自动创建
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    # 追加写入
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)
        #print(line)
# 日志end
# 创建文件
def create_file():
    out_file_path = os.path.join(work_dir,"excle",current_time)
    os.mkdir(out_file_path)
create_file()  
# 读取表格数据
ex_data1_filename = config['data1']['file_name'] #数据文件名
ex_price1_filename = config['price1']['file_name'] #价格文件名
ex_data2_filename = config['data2']['file_name'] #数据文件名
ex_price2_filename = config['price2']['file_name'] #价格文件名
price1_1 = get_excel_file(ex_price1_filename,config['price1']['sheet_name_price1'])   # 单品价格
price1_2 = get_excel_file(ex_price1_filename,config['price1']['sheet_name_price2'])   # 多品价格
price1_3 = get_excel_file(ex_price1_filename,config['price1']['sheet_name_price3_width']) # 配件表
price1_4 = get_excel_file(ex_price1_filename,config['price1']['sheet_name_overseas']) # 海外仓sku表
price2_1= get_excel_file(ex_price2_filename,config['price2']['sheet_name_price1'])
price2_2= get_excel_file(ex_price2_filename,config['price2']['sheet_name_price2'])
price2_3= get_excel_file(ex_price2_filename,config['price2']['sheet_name_price3_width'])
data1 = get_excel_file(ex_data1_filename,config['data1']['sheet_name'])
data2 = get_excel_file(ex_data2_filename,config['data2']['sheet_name'])
#checkExcleData(data1)
def checkExcleData(data):
    print(data.columns.tolist(),'表头1')
    print(data.head())
# 格式化价格
# check return data =========================================
def check_data(lst):
    if not isinstance(lst, list):
        return None
    if not lst:
        return None
    return lst[0]
# 运行 def========== data2相似sku转换
def sku_a_equid_b1():
    sku_col_name = ex_sku
    same_skulist = config['other']['a1_equid_b1']
    for key, value in same_skulist.items():
        # print(key, value)
        data1[sku_col_name] = data1[sku_col_name].replace(key,value)
    return data1
# return row_index number  =========================================
def get_row_index_by_sku(sku,type,country="US"):
    row_index = []
    # 1 不区分国家 多品价格
    if type == 1:
        sku_col_name = config['price1']['sku_col_name']
        row_index = price1_2.index[price1_2[sku_col_name] == sku].tolist()
        return check_data(row_index)
    # 2 不区分国家 海外
    
    if type == 2:
        sku_col_name = config['price1']['sku_col_name']
        row_index = price1_4.index[price1_4[sku_col_name] == sku].tolist()  
        return check_data(row_index)
    #区分国家 单个
    if type == 3:
        sku_col_name = config['price2']['sku_col_name']
        mask = price2_1[sku_col_name] == sku 
        row_index = price2_1.index[mask].tolist()
        #print(row_index,'==')
        return check_data(row_index)
    #区分国家 多个
    if type == 4:
        sku_col_name = config['price2']['sku_col_name']
        if country in ['AU','CA','DE','FR','GB']:
            mask = price2_2[sku_col_name] == sku
            row_index = price2_2.index[mask].tolist()
            if check_data(row_index) is not None:
                index = check_data(row_index)
                end_index = index + 9
                subset = price2_2.iloc[index:end_index]
                filtered_data = subset[subset[ex_price2_country] == country]
                return check_data(filtered_data.index.tolist())
            else:
                return None
        elif country in ["US"]:
            mask = price2_2[sku_col_name] == sku
            row_index = price2_2.index[mask].tolist()
            if check_data(row_index) is not None:
                index = check_data(row_index)
                end_index = index + 9
                subset = price2_2.iloc[index:end_index]
                filtered_data = subset[subset[ex_price2_country] == "US Main"]
                return check_data(filtered_data.index.tolist())
            else:
                return None
        elif country in ["IE","FI","ES"]:
            mask = price2_2[sku_col_name] == sku
            row_index = price2_2.index[mask].tolist()
            if check_data(row_index) is not None:
                index = check_data(row_index)
                end_index = index + 9
                subset = price2_2.iloc[index:end_index]
                filtered_data = subset[subset[ex_price2_country] == "EU-Other"]
                return check_data(filtered_data.index.tolist())
            else:
                return None
        else:
            write_log(f"没有找到{sku}的价格所在的行,get_row_index_by_sku")
            return None
# 获取配件价格
def get_equipped_price(index,row):
    sku = row[ex_sku]
    list_sku = price1_3[ex_price_sku].values.tolist() or []
    qty = row[ex_qty] # 获取数量
    # print(list_sku,'list_sku')
    if sku in list_sku:
        mask = price1_3[config['price1']['sku_col_name']] == sku
        sku_list = price1_3.index[mask].tolist()
        if len(sku_list) > 0:
            row_index = sku_list[0]
            one = price1_3.loc[row_index, "总价（1个）"] 
            more = price1_3.loc[row_index, "多品价格"]
            if float(qty) > 1:
                data1.loc[[index], ex_data_price] = float(one) + (float(qty) - 1) * float(more)      
            else:
                data1.loc[[index], ex_data_price] = one
            write_log(f"填充配件-{sku}的价格为{data1.loc[index, ex_data_price]}") 
            print('配件价格填充成功')
# 不区分国家数量大于一 多品 设置价格 =========================================
def fill_price_by_quantity():
    # 不区分国家 查询多规格
    # 1.数量大于一的行
    data1['Quantity'] = pd.to_numeric(data1['Quantity'], errors='coerce')
    mask = data1['Quantity'] > 1
    row_list = data1.index[mask].tolist() or []
    # print(row_list,'数量大于1的行')
    if len(row_list) == 0:
        write_log("没有 Quantity > 1 的订单")
        return
    for row in row_list:  
        sku = data1.loc[row, ex_sku] # 获取sku
        qty = data1.loc[row, 'Quantity'] # 获取数量
        # print(sku,'sku')
        # 价格表匹配
        row_index = get_row_index_by_sku(sku, 1) # 获取价格表的行索引   
        if row_index is None:
            data1.loc[[row], ex_data_price] = 0
            write_log(f"填充{sku}的价格为{0}_error")
            continue
        price = price1_2.loc[row_index, '总价（1个）']
        add_one_price = price1_2.loc[row_index, '多1个的价格']
        data1.loc[[row], ex_data_price] = (float(price) + (qty - 1) * float(add_one_price)).round(2)
        write_log(f"填充{sku}的价格为{price}")
    # 保存
    #print(data1.loc[:12, 'Price'],"写入后的数据")
# 查询重复的项并且写入价格 def ===========================================
def fill_price_by_duplicated_id():
    # 1.查询重复的 order_id sku 重复的行
    duplicates = data1[data1.duplicated(subset=[ex_order_id,ex_sku], keep=False)]
    count_id = []
    if len(duplicates) > 0:
        write_log("有,id和sku同事重复的")
        for index, row in duplicates.iterrows():
            filtered_rows = data1[data1[ex_order_id] == row[ex_order_id]] #相同的sku id
            if row[ex_order_id] in count_id:
                continue
            count_id = count_id + [row[ex_order_id]]
            if len(filtered_rows) > 0:
                count = 0
                for index, row in filtered_rows.iterrows():
                    count = count + 1
                    sku = row[ex_sku]
                    qty = row[ex_qty] # 获取数量
                    row_index = get_row_index_by_sku(sku, 1) # 获取价格表的行索引   
                    if row_index is None:
                        data1.loc[[index],ex_data_price]  = 0
                        write_log(f"填充{sku}的价格为{0}_error")
                        continue
                    # count_dict_qty = count_dict[sku] #出现次数
                    price = price1_2.loc[row_index, ex_one_price]
                    add_one_price = price1_2.loc[row_index, ex_one_more_price] #加1个的价格
                    if qty>1 and count == 1: # 数量大于1 并且是第一次
                        data_price = float(price) + (qty - 1) * float(add_one_price)
                        data1.loc[[index],ex_data_price]  = data_price  
                    elif qty==1 and count == 1: # sku出现次数大于1 并且是第一次
                        data1.loc[[index],ex_data_price]  = price
                    else:
                        data_price = float(qty * float(add_one_price))
                        data1.loc[[index],ex_data_price]  = data_price
                    # 检查是不是配件 
                    get_equipped_price(index,row)
    # 2.查询重复的 order_id 重复的行 且sku不重复
    mask1 = data1.duplicated(subset=[ex_order_id], keep=False)
    result = data1[mask1 & ~data1.duplicated(subset=[ex_order_id,ex_sku], keep=False)]
    if len(result) > 0:
        for index, row in result.iterrows():
            sku = row[ex_sku]
            qty = row[ex_qty] # 获取数量
            row_index = get_row_index_by_sku(sku, 1)  # 不区分国家 单品价格
            if row_index is None:
                data1.loc[[index], ex_data_price] = 0
                write_log(f"填充{sku}的价格为{0}_error")
                continue
            price = price1_2.loc[row_index, ex_one_price] or '-'
            add_one_price = price1_2.loc[row_index, ex_one_more_price] or '-'
            # 数量大于一
            if float(qty) > 1:
                data1.loc[[index], ex_data_price] = float(price) + (row[ex_qty] - 1) * float(add_one_price)
            else:
                data1.loc[[index], ex_data_price] = price  
            # 检查是不是配件 
            get_equipped_price(index,row)
                        
# 所有数据按照单品写入一次价格  优先填一次sku的价格
def fill_price_by_sku():
    pricelist = format_price()  # 获取价格表的sku和价格
    list_sku = list(pricelist.keys()) # []
    # 填充价格 
    for index, row in data1.iterrows():
        sku = row[ex_sku]
        if sku in list_sku:
            data1.loc[[index], ex_data_price] = pricelist[row[ex_sku]]
        else: 
            data1.loc[[index], ex_data_price] = 0      
            write_log(f"填充{sku}的价格为{0}_error")
    # 保存数据
#处理海外多品价格和海外单品价格
def fill_price_by_overseas_sku():
    mask_overseas = data1[config['data1']["Tracking_Company"]] == "USPS"
    result = data1[mask_overseas]
    if len(result) > 0:
        for index, row in result.iterrows():
            sku = row[ex_sku]
            row_index = get_row_index_by_sku(sku, 2)  # 不区分国家 海外价格
            if row_index is None:
                data1.loc[[index], ex_data_price] = 0
                write_log(f"填充{sku}的价格为{0}_error")
                continue
            qty = row[ex_qty] # 获取数量
            price = price1_4.loc[row_index,ex_one_price]
            add_one_price = price1_4.loc[row_index, ex_one_more_price]
            if qty > 1: # 数量大于1
                data1.loc[[index], ex_data_price] = float(price) + (row[ex_qty] - 1) * float(add_one_price)
            else:   
                data1.loc[[index], ex_data_price] = price
            write_log(f"填充海外单品{row[ex_sku]}的价格")
        # 海外仓多品处理 相似sku
        maskduplicates = result[result.duplicated(subset=[ex_order_id,ex_sku], keep=False)]
        # print(maskduplicates,'similar sku')
        count_id = []
        if len(maskduplicates) > 0:
            write_log("海外仓库有id和sku同事重复的列表")
            for index, row in maskduplicates.iterrows():
                filtered_rows = result[result[ex_order_id] == row[ex_order_id]] #相同的sku id
                if row[ex_order_id] in count_id:
                    continue        
                count_id = count_id + [row[ex_order_id]]
                if len(filtered_rows) > 0:
                    count = 0
                    for index, row in filtered_rows.iterrows():
                        count = count + 1
                        sku = row[ex_sku]
                        qty = row[ex_qty] # 获取数量
                        row_index = get_row_index_by_sku(sku, 2) # 获取价格表的行索引   
                        if row_index is None:
                            data1.loc[[index], ex_data_price] = 0
                            write_log(f"填充{sku}的价格为{0}_error")
                            continue
                        price = price1_4.loc[row_index, ex_one_price]
                        add_one_price = price1_4.loc[row_index, ex_one_more_price] #加1个的价格
                        if qty>1 and count == 1: # 数量大于1 并且是第一次
                            data_price = float(price) + (qty - 1) * float(add_one_price)
                            data1.loc[[index],ex_data_price]  = data_price       
                        elif qty==1 and count == 1: # sku出现次数大于1 并且是第一次 
                            data1.loc[[index],ex_data_price]  = price
                        else:
                            data1.loc[[index],ex_data_price]  = float(qty * float(add_one_price))  
                        write_log(f"填充{row[ex_sku]}的价格为{data1.loc[[index],ex_data_price]},{index}")  
# 处理不区分国家的海外多品价格
def start_fill_price_data1():
    file_path = os.path.join(script_dir, "excle", ex_data1_filename)
    write_log("开始填充价格")
    # 格式化数据
    data_old = get_excel_file(file_path,config['data1']['sheet_name'])
    # 检测数据是否为空
    if data_old is None:
        print("===>不区分国家 文件不存在/名称不对")
        return
    # 检测表头是否为空
    header_list = data_old.columns.tolist()
    config_header_list = [ex_order_id,ex_sku,ex_qty,ex_overseas_attribute]
    flag = all(item in header_list for item in config_header_list)
    if not flag:
        print(f"数据表头=> {header_list}")
        print(f"1表头不匹配=> {config_header_list}")
        return
    data1 = sku_a_equid_b1()
    write_log("开始填充不区分国家的价格")
    # 1.根据sku填充价格
    fill_price_by_sku()
    # 2.填充数量大于1的价格 
    fill_price_by_quantity()
    # 3.查询重复的订单id和sku的价格
    fill_price_by_duplicated_id()
    # 4.查询海外sku 数量大于1计价，不大于1原价
    fill_price_by_overseas_sku()
    # 5.保存数据
    data1[ex_data_price] = pd.to_numeric(data1[ex_data_price], errors='coerce')
    data1[ex_data_price] = data1[ex_data_price].round(2)
    data_old.update(data1[[ex_data_price]])
    name = config['data1']['outName']
    file_path = os.path.join(work_dir,"excle",current_time, name)
    data_old.to_excel(file_path,sheet_name=config['data1']['sheet_name'],index=False,engine='openpyxl')
    print(f"填充价格完成:{file_path}")
# 运行 def==========================================start_fill_price
start_fill_price_data1()
# end fill data1=====================================================================

# 处理区分国家的价格
#公共参数 config['data2']['sku_col_name'] #订单ID
ex_data2_sku = config['data2']['sku_col_name']  # 数据sku列名
ex_data2_qty = config['data2']['数量_表头'] 
ex_data2_country = config['data2']['国家_表头'] 
ex_data2_price = config['data2']['写入价格_表头'] 
ex_data2_order_id = config['data2']['订单编号_表头'] 
ex_price2_country = config['price2']['country_col_name'] 
ex_price2_price = config['price2']['总价_1个'] 
ex_price2_shippingfee = config['price2']['第2件运费'] 
ex_price2_goodsfee = config['price2']['产品价格'] 
ex_price2_3_sku = config['price2']['配件SKU']
# 获取配件-行数
def get_equipped_row_index(sku):
    mask = price2_3[config['price2']['sku_col_name']] == sku
    row_index = price2_3.index[mask].tolist()
    return check_data(row_index)
# 配件价格处理
def fill_price_by_equipped_data2(index,row):
    sku = row[ex_data2_sku]
    qty = row[ex_data2_qty] # 获取数量
    country = row[ex_data2_country]
    list_sku = price2_3[ex_price2_3_sku].values.tolist() or []
    if sku in list_sku and len(list_sku) > 0:
        row_index = get_equipped_row_index(sku)
        if row_index is None:
            data2.loc[[index], ex_data2_price] = 0
            write_log(f"填充{sku}的价格为{0}_error")
            return
        price = 0
        if country in ['AU','CA','DE','FR','GB','US']:
            price = price2_3.loc[row_index,ex_price2_price]
        elif country in ["IE","FI","ES"]: #获取价格
            price = price2_3.loc[row_index,'WW-Other']
        else:
            price = 0
        data2.loc[[index], ex_data2_price] = float(price)*qty
        write_log(f"填充{sku}的价格为{data2.loc[[index], ex_data2_price]}")
# 填充所有价格 data2 单品处理
def fill_price_by_sku_data2():
    for index, row in data2.iterrows():
        sku = row[ex_data2_sku]
        country = row[ex_data2_country]
        row_index = get_row_index_by_sku(sku, 3)
        if row_index is None:
            data2.loc[[index], ex_data2_price] = price
            write_log(f"填充{sku}的价格为{0}_error")
            continue
        price = 0
        if country in ['AU','CA','DE','FR','GB','US']:
            price = price2_1.loc[row_index,country]
        elif country in ["IE","FI","ES"]: #获取价格
            price = price2_1.loc[row_index,'WW-Other']
        else:
            price = 0
        data2.loc[[index], ex_data2_price] = price
        write_log(f"填充{row[ex_data2_sku]}的价格为{price},county:{country}")  
#  数量大于1的行 多品处理
def fill_price_by_quantity_data2(): 
    write_log(f"开始填充数量大于1的行")
    data2[ex_data2_qty] = pd.to_numeric(data2[ex_data2_qty], errors='coerce')   
    mask = data2[ex_data2_qty] > 1
    row_list = data2.index[mask].tolist() or []
    write_log(f"数量大于1的行:{row_list}")
    if len(row_list) == 0:
        write_log("没有 Quantity > 1 的订单")
        return
    write_log(f"row_list:{data2.loc[2,ex_data2_sku]}")
    for index in row_list: 
        sku = data2.loc[index,ex_data2_sku]
        qty = data2.loc[index,ex_data2_qty]
        country = data2.loc[index,ex_data2_country]
        row_index = get_row_index_by_sku(sku,4,country)
        if row_index is None:
            write_log(f"填充{sku}的价格为{0}_error")
            data2.loc[[index], ex_data2_price] = 0
            continue
        write_log(f"开始填充{sku},---,{country}的价格,price2_2行索引{row_index}")
        price = 0
        one_more_price = 0
        if country in ['AU','CA','DE','FR','GB','US']:
            price = price2_2.loc[row_index,ex_price2_price]
            shipping_fee = price2_2.loc[row_index,ex_price2_shippingfee]
            goods_fee = price2_2.loc[row_index,ex_price2_goodsfee]
            one_more_price = float(shipping_fee) + float(goods_fee)
        else:
            price = 0
            one_more_price = 0
        data2.loc[[index], ex_data2_price] = float(price) + (qty - 1) * float(one_more_price)
        write_log(f"填充{sku}的价格为{data2.loc[[index], ex_data2_price]}")    
#
def fill_price_by_duplicated_id_data2():
    # 1.查询重复的 order_id sku 重复的行
    duplicates = data2[data2.duplicated(subset=[ex_data2_order_id,ex_data2_sku], keep=False)]
    count_id = []
    if len(duplicates) > 0:
        for index, row in duplicates.iterrows():
            if row[ex_data2_order_id] in count_id:
                continue
            count_id = count_id + [row[ex_data2_order_id]]
            filtered_rows = data2[data2[ex_data2_order_id] == row[ex_data2_order_id]] #相同的sku id
            if len(filtered_rows) > 0:
                count = 0
                for index, row in filtered_rows.iterrows():
                    count = count + 1
                    sku = row[ex_data2_sku]
                    qty = row[ex_data2_qty] # 获取数量
                    country = row[ex_data2_country]
                    row_index = get_row_index_by_sku(sku, 4,country) # 获取价格表的行索引 
                    if row_index is None:
                        data2.loc[[index], ex_data2_price] = 0
                        write_log(f"填充{sku}的价格为{0}_error")
                        continue
                    price = price2_2.loc[row_index,ex_price2_price]
                    shipping_fee = price2_2.loc[row_index,ex_price2_shippingfee]
                    goods_fee = price2_2.loc[row_index,ex_price2_goodsfee]  
                    one_more_price = float(shipping_fee) + float(goods_fee)
                    qty = float(qty)
                    if qty > 1 and count == 1: # 数量大于1 并且是第一次
                        data2.loc[[index],ex_data2_price]  = float(price) + (qty - 1) * float(one_more_price)
                    elif qty == 1 and count == 1: # sku出现次数大于1 并且是第一次
                        data2.loc[[index],ex_data2_price]  = price
                    else:
                        data2.loc[[index],ex_data2_price]  = float(qty * float(one_more_price))
                        write_log(f"{count}xxxx填充{row[ex_data2_sku]}的价格为{data2.loc[[index],ex_data2_price]}")
                    # 设置配件价格
                    fill_price_by_equipped_data2(index,row)
    # 2.查询重复的 order_id 重复的行 且sku不重复
    mask1 = data2.duplicated(subset=[ex_data2_order_id], keep=False)
    result = data2[mask1 & ~data2.duplicated(subset=[ex_data2_order_id,ex_data2_sku], keep=False)]
    if len(result) > 0:
        for index, row in result.iterrows():
            sku = row[ex_data2_sku]
            qty = row[ex_data2_qty] # 获取数量
            country = row[ex_data2_country]
            row_index = get_row_index_by_sku(row[ex_data2_sku],4,country)
            if row_index is None:
                data2.loc[[index], ex_data2_price] = 0
                write_log(f"填充{sku}的价格为{0}_error")
                continue
            price = price2_2.loc[row_index,ex_price2_price]
            shipping_fee = price2_2.loc[row_index,ex_price2_shippingfee]
            goods_fee = price2_2.loc[row_index,ex_price2_goodsfee]
            one_more_price = float(shipping_fee) + float(goods_fee)
            # 检查是不是配件 配件单发价格不一样的
            # 数量大于一   
            qty = float(qty) 
            if qty> 1:
                data2.loc[[index], ex_data2_price] = float(price) + (qty - 1) * float(one_more_price)
            else:
                data2.loc[[index], ex_data2_price] = price
            # 设置配件价格
            fill_price_by_equipped_data2(index,row)
 
# data2相似sku转换 先格式化数据用来处理sku中视为相同的清款
def sku_a_equid_b2():
    same_skulist = config['other']['a2_equid_b2']
    for key, value in same_skulist.items():
        # print(key, value)
        data2[ex_data2_sku] = data2[ex_data2_sku].replace(key,value)
    return data2
def start_fill_price_data2():
    file_path = os.path.join(script_dir, "excle", ex_data2_filename)
    data_old = get_excel_file(file_path,config['data2']['sheet_name'])
    # 检测数据是否为空
    if data_old is None:
        print("===>区分国家 文件不存在/名称不对")
        return
    # 检测表头是否为空
    header_list = data_old.columns.tolist()
    config_header_list = [ex_data2_order_id,ex_data2_sku,ex_data2_qty,ex_data2_country]
    flag = all(item in header_list for item in config_header_list)
    if not flag:
        print(f"数据表头=> {header_list}")
        print(f"2表头不匹配=> {config_header_list}")
        return
    # 格式化数据
    data2 = sku_a_equid_b2()
    # print(data2.iloc[229:234][ex_data2_sku])
    # 1.填充价格
    fill_price_by_sku_data2()
    # 2.填充数量大于1的价格 
    fill_price_by_quantity_data2()
    # 3.填充数量大于1的价格 
    fill_price_by_duplicated_id_data2()
    # 5.保存数据
    data2[ex_data2_price] = pd.to_numeric(data2[ex_data2_price], errors='coerce')
    data2[ex_data2_price] = data2[ex_data2_price].round(2)
    # 覆盖
    data_old.update(data2[[ex_data2_price]])
    name = config['data2']['outName']
    file_path = os.path.join(work_dir,"excle",current_time, name)
    data_old.to_excel(file_path,sheet_name=config['data2']['sheet_name'],index=False,engine='openpyxl') 
    print(f"填充价格完成:{file_path}")
start_fill_price_data2()
# 保持窗口打开
input("请按任意键退出")
