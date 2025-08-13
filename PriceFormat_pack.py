import os
import subprocess
import sys

def pack_script(script_name, output_dir="dist", one_file=True, no_console=False, additional_data=None):
    """
    使用 PyInstaller 打包指定的 Python 脚本，并包含额外的数据文件或文件夹。
    :param script_name: 要打包的脚本文件名（包含路径）
    :param output_dir: 打包后的输出目录
    :param one_file: 是否打包为单文件（默认 True）
    :param no_console: 是否隐藏控制台窗口（默认 False）
    :param additional_data: 要包含的额外数据文件或文件夹列表，格式为 [(<source>, <destination>), ...]
    """
    # 构造 PyInstaller 命令
    command = [sys.executable, "-m", "PyInstaller"]
    
    # 添加单文件选项
    if one_file:
        command.append("--onefile")
    
    # 添加隐藏控制台窗口选项
    if no_console:
        command.append("--noconsole")
    
    # 设置输出目录
    command.extend(["--distpath", output_dir])
    
    # 添加额外的数据文件或文件夹
    if additional_data:
        for src, dest in additional_data:
            command.extend(["--add-data", f"{src};{dest}"])
    
    # 添加要打包的脚本
    command.append(script_name)

    # 执行 PyInstaller 命令
    try:
        print(f"正在打包 {script_name}...")
        subprocess.run(command, check=True)
        print(f"打包完成，可执行文件已保存到 {output_dir} 目录。")
    except subprocess.CalledProcessError as e:
        print(f"打包失败：{e}")

if __name__ == "__main__":
    # 示例：打包 main.py，并包含 config.json 和 data/ 文件夹
    script_to_pack = "PriceFormat.py"
    additional_data = [(r"D:\ldd-desk\python\py_price\excle\**", "excle/")]
    pack_script(script_to_pack, one_file=True, no_console=False, additional_data=additional_data)