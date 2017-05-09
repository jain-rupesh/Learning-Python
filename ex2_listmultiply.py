'''
Write a Python program to multiplies all the items in a list.
'''

list1 = [1,3,7,6,4,7,9,12]

sum = 1
i = 0
while i < len(list1):
    sum *= list1[i]
    i += 1 
    
print sum
