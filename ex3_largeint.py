list1 = [1,3,5,7,15,3,5,7,9,12]

lrg = 0
i = 0
while i < len(list1):
    
    if list1[i] >= lrg:
      lrg = list1[i]
    
    i += 1 
    
print lrg
