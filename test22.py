def contains_sublist(main_list, sublist):
    return all(item in main_list for item in sublist)

# 示例用法
main_list = [1, 2, 3, 4, 5]
sublist = [2, 3, 4]

result = contains_sublist(main_list, sublist)
print(result)  # 输出: True

sublist = [2, 6]
result = contains_sublist(main_list, sublist)
print(result) 