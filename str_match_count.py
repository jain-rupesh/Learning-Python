'''
Write a Python program to count the number of strings where the string length is 2 or more and the first and last character are same from a given list of strings. Go to the editor 
Sample List : ['abc', 'xyz', 'aba', '1221']
Expected Result : 2
'''

list1 = ['abc', 'robin', 'pop', 'aa', 'bob']

count = 0

for x in list1:
    if len(x) > 2:
      if x[0] == x[-1]:
        count += 1
    
print count
