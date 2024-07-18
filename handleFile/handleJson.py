import handleFile.fileUtil as fu
import json
import commonUtil
import handleFile.handleExcel as he

# 获取kibana日志的traceId行内容（包括前面的服务名、spanId），比如[xx-oms-oversea-boot,536e6d1105c1086d14ff9b9caaff5fb6,47488c37afe5e573,false]，
# 组成kibana的OR查询语句，以便进行下一步的查询
def get_traceId_line(file_path):
    # 读取数据
    data = fu.read_json_file(file_path)
    if not data:
        print("No data to process.")
        return

    extracted_messages = []
    for hit in data['hits']:
        message = hit['_source']['message']
        start_index = message.find('[')
        end_index = message.find(']', start_index)
        if start_index != -1 and end_index != -1:
            extracted_content = message[start_index:end_index+1]
            extracted_messages.append(f'message:"{extracted_content}"')

    # print(" OR ".join(extracted_messages))
    new_file_path = fu.generate_new_filename(file_path, '_result', '.txt')
    fu.write_file(new_file_path, " OR ".join(extracted_messages))
    print(f'\033[32mget_traceId_line处理结束，结果文件路径：{new_file_path}\033[0m')


# 从日志中获取json串指定key的值。要求日志内容必须包含json串。一般需要借助get_traceId_line进行前置查询
def get_value_from_json_in_log(file_path, filter_content, key_name, json_type='object'):
    # 读取数据
    data = fu.read_json_file(file_path)
    if not data:
        print("No data to process.")
        return

    extracted_messages = []
    for hit in data['hits']:
        message = hit['_source']['message']
        filter_index = message.find(filter_content)
        # filter_content有值，并且message没有包含filter_content，跳过
        if filter_content and (filter_index == -1):
            continue

        # key_name有值，说明需要解析json串获取值
        if key_name:
            if json_type == 'object':
                start_index = message.find('{', filter_index)
                end_index = message.rfind('}')
            else:
                start_index = message.find('[', filter_index)
                end_index = message.rfind(']')

            if start_index != -1 and end_index != -1:
                extracted_content = message[start_index:end_index+1]
                log_obj = json.loads(extracted_content)
                extracted_messages.append(log_obj[key_name])
            else:
                print(f'日志内容不包含json串，日志内容：{message}')

        else:
            # key_name无值，直接获取日志内容
            extracted_messages.append(extracted_content)

    # 对列表元素去重并排序
    extracted_messages = commonUtil.unique_elements_ordered(extracted_messages)
    new_file_path = fu.generate_new_filename(file_path, '_result', '.txt')
    fu.write_file(new_file_path, "\n".join(extracted_messages))
    print(f'\033[32mget_value_from_json_in_log处理结束，结果文件路径：{new_file_path}\033[0m')

# 从日志中获取数据生成Excel文件。要求日志内容必须包含json串。一般需要借助get_traceId_line进行前置查询
def generate_excel_from_json_obj_in_log(file_path, filter_content, key_name_list):
    # 读取数据
    data = fu.read_json_file(file_path)
    if not data:
        print("No data to process.")
        return

    extracted_messages = []
    for hit in data['hits']:
        message = hit['_source']['message']
        filter_index = message.find(filter_content)
        # filter_content有值，并且message没有包含filter_content，跳过
        if filter_content and (filter_index == -1):
            continue

        start_index = message.find('{', filter_index)
        end_index = message.rfind('}')
        # 解析到对象
        if start_index != -1 and end_index != -1:
            # key_name_list有值，说明需要解析json串获取值
            if bool(key_name_list):
                extracted_content = message[start_index:end_index+1]
                log_obj = json.loads(extracted_content)
                # 定义新对象
                obj = {}
                for key_name in key_name_list:
                    obj[key_name] = log_obj[key_name]
                extracted_messages.append(obj)
                # 取key_name_list的第一个元素进行去重、排序
                operate_key = key_name_list[0]
            else:
                # key_name无值，直接获取日志内容
                extracted_messages.append(log_obj)
                # 取log_obj的第一个key进行去重、排序
                operate_key = list(log_obj.keys())[0]
        else:
            print(f'日志内容不包含json串，日志内容：{message}')

    # 对列表元素根据operate_key去重并排序
    deduplicated_elements = {element[operate_key]: element for element in extracted_messages}.values()
    sorted_elements = sorted(deduplicated_elements, key=lambda x: x[operate_key])
    new_file_path = fu.generate_new_filename(file_path, '_result', '.xlsx')
    # 生成Excel文件
    he.save_data_to_excel(new_file_path, sorted_elements)
    print(f'\033[32mget_value_from_json_in_log处理结束，结果文件路径：{new_file_path}\033[0m')