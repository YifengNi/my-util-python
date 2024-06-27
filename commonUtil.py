import handleExcel as he


# 处理命令
def handle_command(command, params):
    if command == commandList[0]:
        # 把csv文件转换成Excel文件且把字符串列左边的单引号去掉
        he.csv_to_excel(params[0])

    elif command == commandList[1]:
        file_path = params[0]
        column_name = params[1]
        string_type = params[2] if len(params) >= 3 else True
        # 根据列数据生成SQL的in条件
        inCodition = he.get_sql_in_condition_from_column(file_path, column_name, string_type)
        print(f'\033[32m{inCodition}\033[0m')

    else:
        print(f'Unknown command: {command}')


# 命令列表
commandList = ['csvToExcel', 'formatColumnDataToInClause']

# 输入命令，执行不同处理逻辑
while True:
    tips = f'''\033[33m
按如下提示输入命令实现功能：
1、把csv文件转换成Excel文件且把字符串列左边的单引号去掉：{commandList[0]} 文件名全路径
2、把整列数据组装成SQL的in条件：{commandList[1]} 文件名全路径 列名 字符串类型（可选）
输入命令：\033[0m'''
    # 获取输入
    user_input = input(tips)
    if user_input == 'exit':
        break

    split_input = user_input.split(' ')
    command = split_input[0]
    params = split_input[1:]

    handle_command(command, params)