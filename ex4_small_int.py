'''
Write a Python program to get the smallest number from a list.
'''
list1 = [1,3,5,7,15,-1,5,7,9,12]

sml = list1[0]

i = 0
while i < len(list1):
    if sml >= list1[i]:
      sml = list1[i]
    
    i += 1 
    
print sml
