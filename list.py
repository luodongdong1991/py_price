#!/usr/bin/python3

list = ['red', 'green', 'blue', 'yellow', 'white', 'black']
listAdd = ['a',"c",'d']
list.extend(listAdd)
print(list.count("a"))
list.extend([1,2,3])
print(list)
print(list.index("a"))
