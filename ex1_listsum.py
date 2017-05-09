'''
Write a Python program to sum all the items in a list.
'''
list1 = [1,3,5,7,9,3,5,7,9,12]

sum = 0
i = 0
while i < len(list1):
    sum += list1[i]
    i += 1 
    
print sum
