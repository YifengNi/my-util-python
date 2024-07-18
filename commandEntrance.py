import handleFile.handleExcel as he
import handleFile.handleJson as hj


# 处理命令
def handle_command(command, params):
    if command == commandList[0]:
        # 把csv文件转换成Excel文件且把字符串列左边的单引号去掉
        # 入参示例：csvToExcel C:\\Users\\用户\\Downloads\\南天门20240530.csv
        he.csv_to_excel(params[0])

    elif command == commandList[1]:
        file_path = params[0]
        column_name = params[1]
        string_type = params[2] if len(params) >= 3 else True
        # 根据列数据生成SQL的in条件
        # 入参示例：formatColumnDataToInClause C:\\Users\\XPeng\\Downloads\\南天门20240507_new.xlsx 'CITYCOMPANY_CODE
        # 入参示例：formatColumnDataToInClause C:\\Users\\XPeng\\Downloads\\南天门20240507_new.xlsx A
        inCodition = he.get_sql_in_condition_from_column(file_path, column_name, string_type)
        print(f'\033[32m{inCodition}\033[0m')

    elif command == commandList[2]:
        file_path = params[0]
        # 获取kibana日志的traceId行内容（包括前面的服务名、spanId）
        # 入参示例：getTraceIdLine C:\\Users\\xx\\Downloads\\log-getTraceIdLine.json
        hj.get_traceId_line(file_path)

    elif command == commandList[3]:
        file_path = params[0]
        filter_content = params[1]
        key_name = params[2]
        # 从日志中获取json串指定key的值
        # 入参示例：getValueFromJsonInLog C:\\Users\\xx\\Downloads\\log-getValueFromJsonInLog.json 采购子订单ERP车辆状态同步，同步参数 vin
        hj.get_value_from_json_in_log(file_path, filter_content, key_name)

    elif command == commandList[4]:
        file_path = params[0]
        filter_content = params[1]
        key_name_list = params[2:]
        # 从日志中获取数据生成Excel文件
        # 入参示例：generateExcelFromJsonObjInLog C:\\Users\\xx\\Downloads\\log-getValueFromJsonInLog.json 采购子订单ERP车辆状态同步，同步参数 vin purchaseSubOrderNo
        hj.generate_excel_from_json_obj_in_log(file_path, filter_content, key_name_list)

    else:
        print(f'Unknown command: {command}')


# 命令列表
commandList = ['csvToExcel', 'formatColumnDataToInClause', 'getTraceIdLine', 'getValueFromJsonInLog', 'generateExcelFromJsonObjInLog']

# 输入命令，执行不同处理逻辑
while True:
    tips = f'''\033[33m
按如下提示输入命令实现功能：
1、把csv文件转换成Excel文件且把字符串列左边的单引号去掉：{commandList[0]} 文件名全路径
2、把整列数据组装成SQL的in条件：{commandList[1]} 文件名全路径 列名 字符串类型（可选）
3、获取kibana日志的traceId行内容（包括前面的服务名、spanId）：{commandList[2]} 文件名全路径
4、从日志中获取json串指定key的值：{commandList[3]} 文件名全路径 过滤内容（包含内容） key名称 json类型
5、从日志中获取json串指定key的值：{commandList[4]} 文件名全路径 过滤内容（包含内容） key名称列表（可选）
输入命令：\033[0m
'''
    
    # 获取输入
    user_input = input(tips)
    if user_input == 'exit':
        break

    split_input = user_input.split(' ')
    command = split_input[0]
    params = split_input[1:]

    handle_command(command, params)