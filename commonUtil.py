# 对列表元素去重并排序
def unique_elements_ordered(input_list):
    # 使用字典从左到右遍历，因为字典是有序的
    return sorted(set(input_list))
