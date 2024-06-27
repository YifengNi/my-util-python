import pandas as pd
import os
import sys
import argparse

# 根据旧文件名生成新文件名
def generate_new_filename(old_filename, new_suffix="_new", new_ext=".xlsx"):
    # 获取文件名和扩展名
    base_name, ext = os.path.splitext(old_filename)
    # 生成新的文件名
    new_filename = base_name + new_suffix + new_ext
    return new_filename


# 把csv文件转换成Excel文件，并且把字符串列左边的单引号去掉
def csv_to_excel(fileName = 'C:\\Users\\用户\\Downloads\\南天门20240530.csv'):
    # newFileName = 'C:\\Users\\用户\\Downloads\\南天门20240419-new.xlsx'
    newFileName = generate_new_filename(fileName)

    # 读取CSV文件
    df = pd.read_csv(fileName)

    # 去除每个元素前面的单引号
    df = df.map(lambda x: x.lstrip('\'') if isinstance(x, str) else x)

    # 将结果保存到新的Excel文件中
    df.to_excel(newFileName, index=False)
    print(f'csv转换Excel文件完成，新文件：{newFileName}\n')


# Excel文件英文下标转成数字下标，比如AA->27
def column_to_number(column):
    number = 0
    for i in range(len(column)):
        number = number * 26 + (ord(column[i].upper()) - ord('A') + 1)
    return number


# 根据列数据生成SQL的in条件
def get_sql_in_condition_from_column(file_path, column_name, string_type = True):
    # 获取文件名和扩展名
    base_name, ext = os.path.splitext(file_path)
    if ext == '.xlsx':
        # 读取Excel文件
        df = pd.read_excel(file_path)
    elif ext == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: '{ext}'") 
    

    # 检查列名是否存在
    if column_name in df.columns:
        # 根据列名获取指定列的数据
        column_data = df[column_name]
    else:
        # 根据英文列下标获取数字列下标
        idx = column_to_number(column_name)
        # 根据英文列下标获取数据
        column_data = df.iloc[:, idx]

    # 根据字段类型格式化数据
    if string_type:
        if ext == '.xlsx':
            formatted_data = [f"'{item}'" for item in column_data]
        elif ext == '.csv':
            formatted_data = [f"{item}'" for item in column_data]
    else:
        formatted_data = column_data

    # 拼接成SQL语句中的IN条件的形式
    in_condition = ', '.join(formatted_data)

    return f"生成in条件语句：\n in ({in_condition})"