import pandas as pd
import datetime
import os
import json
import sys
from pathlib import Path  # 替代os.path，路径处理更简洁


# -------------------------- 配置与路径处理 --------------------------
class ConfigHandler:
    """配置文件处理类"""
    def __init__(self, script_dir):
        self.config_path = Path(script_dir) / "excle" / "config.json"
        self.config = self._load_config()

    def _load_config(self):
        """加载配置文件，处理文件不存在/格式错误"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        except json.JSONDecodeError:
            raise ValueError(f"配置文件格式错误: {self.config_path}")
        except Exception as e:
            raise RuntimeError(f"加载配置失败: {str(e)}")


class PathManager:
    """路径管理类，统一处理文件路径"""
    def __init__(self, script_dir, work_dir, current_time):
        self.script_dir = Path(script_dir)
        self.work_dir = Path(work_dir)
        self.current_time = current_time
        self.excle_dir = self.script_dir / "excle"  # 源Excel目录
        self.output_dir = self.work_dir / "excle" / current_time  # 输出目录

    def get_source_file_path(self, filename):
        """获取源Excel文件路径"""
        return self.excle_dir / filename

    def get_output_file_path(self, filename):
        """获取输出文件路径"""
        self.output_dir.mkdir(parents=True, exist_ok=True)  # 确保输出目录存在
        return self.output_dir / filename

    def get_log_file_path(self, log_filename):
        """获取日志文件路径"""
        log_dir = self.work_dir / "excle"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir / log_filename


# -------------------------- 日志管理 --------------------------
class Logger:
    """日志管理类，封装日志相关操作"""
    def __init__(self, log_file_path):
        self.log_file = log_file_path
        self._clear_log()  # 初始化时清空日志

    def _clear_log(self):
        """清空日志文件"""
        if self.log_file.exists():
            self.log_file.write_text('')

    def write(self, message):
        """写入日志，带时间戳"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f'[{timestamp}] {message}\n'
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)
        print(log_line.strip())  # 同时打印到控制台


# -------------------------- Excel处理工具 --------------------------
class ExcelHandler:
    """Excel文件处理类，封装读取/写入操作"""
    @staticmethod
    def read_excel(file_path, sheet_name, keep_default_na=False, dtype=str):
        """读取Excel文件，返回DataFrame或None"""
        try:
            return pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                keep_default_na=keep_default_na,
                dtype=dtype,
                engine='openpyxl'  # 统一引擎，避免警告
            )
        except Exception as e:
            return None, f"读取失败: {file_path}，错误: {str(e)}"

    @staticmethod
    def write_excel(df, file_path, sheet_name):
        """写入Excel文件"""
        try:
            df.to_excel(
                file_path,
                sheet_name=sheet_name,
                index=False,
                engine='openpyxl'
            )
            return True, f"写入成功: {file_path}"
        except Exception as e:
            return False, f"写入失败: {file_path}，错误: {str(e)}"


# -------------------------- 价格填充核心逻辑 --------------------------
class PriceFiller:
    """价格填充器，封装通用价格填充逻辑"""
    def __init__(self, data, price_tables, config, logger):
        self.data = data  # 待填充数据的DataFrame
        self.price_tables = price_tables  # 价格表字典
        self.config = config  # 当前数据的配置（如data1或data2的配置）
        self.logger = logger  # 日志实例
        self._init_columns()  # 初始化列名

    def _init_columns(self):
        """初始化列名变量（从配置中提取）"""
        self.sku_col = self.config['sku_col_name']
        self.qty_col = self.config['数量表头'] if '数量表头' in self.config else self.config['数量_表头']
        self.price_col = self.config['写入价格表头'] if '写入价格表头' in self.config else self.config['写入价格_表头']
        self.order_id_col = self.config['订单编号表头'] if '订单编号表头' in self.config else self.config['订单编号_表头']
        self.country_col = self.config.get('国家_表头')  # 区分国家时用到

    def _get_first_index(self, lst):
        """获取列表第一个元素（用于提取索引）"""
        return lst[0] if isinstance(lst, list) and lst else None

    def _format_price_map(self, price_table, sku_col, price_col):
        """生成SKU到价格的映射字典"""
        valid_rows = price_table[price_table[sku_col] != '']
        return dict(valid_rows[[sku_col, price_col]].values)

    def fill_by_sku(self, price_table, sku_col, price_col):
        """根据SKU填充基础价格"""
        price_map = self._format_price_map(price_table, sku_col, price_col)
        self.data[self.price_col] = self.data[self.sku_col].map(price_map).fillna(0)
        self.logger.write("完成SKU基础价格填充")

    def fill_by_quantity(self, price_table, sku_col, one_price_col, more_price_col):
        """处理数量大于1的价格计算"""
        self.data[self.qty_col] = pd.to_numeric(self.data[self.qty_col], errors='coerce')
        mask = self.data[self.qty_col] > 1
        target_rows = self.data[mask].index.tolist()

        if not target_rows:
            self.logger.write("无数量>1的记录，跳过数量处理")
            return

        for idx in target_rows:
            sku = self.data.at[idx, self.sku_col]
            qty = self.data.at[idx, self.qty_col]
            # 查找价格表中SKU对应的行
            row_indices = price_table.index[price_table[sku_col] == sku].tolist()
            price_idx = self._get_first_index(row_indices)

            if not price_idx:
                self.data.at[idx, self.price_col] = 0
                self.logger.write(f"SKU {sku} 未找到价格表记录，价格设为0")
                continue

            # 计算价格
            one_price = float(price_table.at[price_idx, one_price_col])
            more_price = float(price_table.at[price_idx, more_price_col])
            total = one_price + (qty - 1) * more_price
            self.data.at[idx, self.price_col] = round(total, 2)
        self.logger.write("完成数量>1的价格处理")

    def fill_by_duplicated(self, price_table, sku_col, one_price_col, more_price_col):
        """处理重复订单ID+SKU的价格计算"""
        # 1. 处理订单ID+SKU均重复的情况
        duplicates = self.data[self.data.duplicated(subset=[self.order_id_col, self.sku_col], keep=False)]
        processed_ids = set()

        for idx, row in duplicates.iterrows():
            order_id = row[self.order_id_col]
            if order_id in processed_ids:
                continue
            processed_ids.add(order_id)

            same_order_rows = self.data[self.data[self.order_id_col] == order_id].index.tolist()
            if not same_order_rows:
                continue

            count = 0
            for row_idx in same_order_rows:
                count += 1
                sku = self.data.at[row_idx, self.sku_col]
                qty = float(self.data.at[row_idx, self.qty_col] or 0)
                # 查找价格表索引
                price_indices = price_table.index[price_table[sku_col] == sku].tolist()
                price_idx = self._get_first_index(price_indices)

                if not price_idx:
                    self.data.at[row_idx, self.price_col] = 0
                    self.logger.write(f"重复订单SKU {sku} 未找到价格，设为0")
                    continue

                # 计算价格
                one_price = float(price_table.at[price_idx, one_price_col])
                more_price = float(price_table.at[price_idx, more_price_col])
                if qty > 1 and count == 1:
                    total = one_price + (qty - 1) * more_price
                elif qty == 1 and count == 1:
                    total = one_price
                else:
                    total = qty * more_price

                self.data.at[row_idx, self.price_col] = round(total, 2)

        self.logger.write("完成重复订单价格处理")

    def finalize_price(self):
        """最终处理价格（四舍五入等）"""
        self.data[self.price_col] = pd.to_numeric(self.data[self.price_col], errors='coerce').round(2)


# -------------------------- 主程序 --------------------------
def main():
    # 初始化基础信息
    current_time = datetime.datetime.now().strftime('%m_%d_%H_%M_%S')
    # 处理脚本路径（兼容打包后环境）
    if getattr(sys, 'frozen', False):
        work_dir = Path(sys.executable).parent
        script_dir = work_dir
    else:
        script_dir = Path(__file__).parent
        work_dir = script_dir

    # 1. 加载配置
    try:
        config_handler = ConfigHandler(script_dir)
        config = config_handler.config
    except Exception as e:
        print(f"配置加载失败: {str(e)}")
        input("按任意键退出")
        return

    # 2. 初始化路径和日志
    path_manager = PathManager(script_dir, work_dir, current_time)
    log_file_path = path_manager.get_log_file_path(config['other']['日志文件'])
    logger = Logger(log_file_path)
    logger.write("程序启动，开始处理价格填充")

    # 3. 读取Excel文件（统一读取所有需要的表）
    excel_handler = ExcelHandler
    price_tables = {}  # 存储所有价格表

    # 读取data1相关表格
    data1_config = config['data1']
    price1_1, err = excel_handler.read_excel(
        path_manager.get_source_file_path(config['price1']['file_name']),
        config['price1']['sheet_name_price1']
    )
    if err:
        logger.write(err)
        return
    price_tables['price1_1'] = price1_1
    price_tables['price1_2'], _ = excel_handler.read_excel(
        path_manager.get_source_file_path(config['price1']['file_name']),
        config['price1']['sheet_name_price2']
    )
    price_tables['price1_4'], _ = excel_handler.read_excel(
        path_manager.get_source_file_path(config['price1']['file_name']),
        config['price1']['sheet_name_overseas']
    )

    # 读取data1数据
    data1, err = excel_handler.read_excel(
        path_manager.get_source_file_path(data1_config['file_name']),
        data1_config['sheet_name']
    )
    if err:
        logger.write(err)
        return

    # 4. 处理data1（不区分国家）
    logger.write("开始处理data1（不区分国家）")
    data1_filler = PriceFiller(data1, price_tables, data1_config, logger)
    # 转换相似SKU
    same_sku_map = config['other']['a1_equid_b1']
    data1[data1_filler.sku_col] = data1[data1_filler.sku_col].replace(same_sku_map)
    # 填充价格
    data1_filler.fill_by_sku(price_tables['price1_1'], config['price1']['sku_col_name'], "价格")
    data1_filler.fill_by_quantity(price_tables['price1_2'], config['price1']['sku_col_name'], "总价（1个）", "多1个的价格")
    data1_filler.fill_by_duplicated(price_tables['price1_2'], config['price1']['sku_col_name'], "总价（1个）", "多1个的价格")
    data1_filler.finalize_price()

    # 写入data1结果
    data1_old, _ = excel_handler.read_excel(
        path_manager.get_source_file_path(data1_config['file_name']),
        data1_config['sheet_name']
    )
    data1_old.update(data1[[data1_filler.price_col]])
    output_path = path_manager.get_output_file_path(data1_config['outName'])
    success, msg = excel_handler.write_excel(data1_old, output_path, data1_config['sheet_name'])
    logger.write(msg)

    # 5. 处理data2（区分国家，逻辑类似，复用PriceFiller）
    logger.write("开始处理data2（区分国家）")
    data2_config = config['data2']
    price2_1, _ = excel_handler.read_excel(
        path_manager.get_source_file_path(config['price2']['file_name']),
        config['price2']['sheet_name_price1']
    )
    price_tables['price2_1'] = price2_1
    price_tables['price2_2'], _ = excel_handler.read_excel(
        path_manager.get_source_file_path(config['price2']['file_name']),
        config['price2']['sheet_name_price2']
    )

    data2, err = excel_handler.read_excel(
        path_manager.get_source_file_path(data2_config['file_name']),
        data2_config['sheet_name']
    )
    if err:
        logger.write(err)
        return

    data2_filler = PriceFiller(data2, price_tables, data2_config, logger)
    # 转换相似SKU
    same_sku_map2 = config['other']['a2_equid_b2']
    data2[data2_filler.sku_col] = data2[data2_filler.sku_col].replace(same_sku_map2)
    # 填充价格（区分国家的逻辑可基于PriceFiller扩展）
    data2_filler.fill_by_sku(price_tables['price2_1'], config['price2']['sku_col_name'], data2_config['国家_表头'])  # 示例，需根据实际调整
    data2_filler.finalize_price()

    # 写入data2结果
    data2_old, _ = excel_handler.read_excel(
        path_manager.get_source_file_path(data2_config['file_name']),
        data2_config['sheet_name']
    )
    data2_old.update(data2[[data2_filler.price_col]])
    output_path2 = path_manager.get_output_file_path(data2_config['outName'])
    success, msg = excel_handler.write_excel(data2_old, output_path2, data2_config['sheet_name'])
    logger.write(msg)

    logger.write("所有价格填充完成")
    input("请按任意键退出")


if __name__ == "__main__":
    main()