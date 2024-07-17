import os
import json

# 根据旧文件名生成新文件名
def generate_new_filename(old_filename, new_suffix="_new", new_ext=".xlsx"):
    # 获取文件名和扩展名
    base_name, ext = os.path.splitext(old_filename)
    # 生成新的文件名
    new_filename = base_name + new_suffix + new_ext
    return new_filename


# 读取 JSON 文件并解析其内容
# 文件名实例：'C:\\Users\\用户\\Downloads\\南天门20240419-new.xlsx'
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# 把内容写到文件中
def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)