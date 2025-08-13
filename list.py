#!/usr/bin/python3

list = ['red', 'green', 'blue', 'yellow', 'white', 'black']
listAdd = ['a',"c",'d']
print( list[0] )
print( list[1] )
print( list[2] )
print( list[-1] )
print( list[-2] )
print( list[-3] )
listCopy = list.copy()
# append()
list.append('pink')
# extend() extend list with listAdd
list.extend(listAdd)
# insert() insert at index 2
list.insert(2,'purple')
# remove() remove element 'green'
list.remove('green')
# pop() pop last element
print(list.pop(),list)
# pop(2) pop element at index 2
print(list.pop(2),list)
# clear() clear list
# list.clear()
print('end of list',list)
# copy list to listCopy

print('listCopy',listCopy,list)
print(len(list),'list length')
# for in 遍历列表
for i in list:
    print(i)