    
# 字典的创建            
my_dict = {'apple': 2, 'banana': 3, 'orange': 4}
print(my_dict)

# 字典的访问    
print(my_dict['apple'])

# 字典的更新    
my_dict['banana'] = 5
# 字典的删除    
del my_dict['orange']
# del dict_name[key] clear
# 字典的遍历    
for key in my_dict:
    print(key, my_dict[key])
len(my_dict) # 字典的长度    
# 字典的合并    
my_dict2 = {'grape': 6, 'pear': 7}
my_dict.update(my_dict2)
print(my_dict)
kk = my_dict.keys()
print(kk)
vv = my_dict.values()
print(vv)
for key in vv:
    print(key)