import random

l = random.sample(range(1,1001),20)
print(l)
# l=[]

def sum(list):
    value = 0
    for i in list:
        value = value + i
    return value

def average(list):
    value = 0
    if len(list)==0:
        print("List is ampty")
        return
    else:
        value=sum(list)/len(list)
    return value

def median(list):
    value = 0
    if len(list)==0:
        print("List is empty")
        return
    else:
        sorted_l=sorted(list)
        print("Sorted list: ",sorted_l)
        n=len(list)
        if n % 2 == 0:
            value=(sorted_l[(n//2)-1]+sorted_l[(n//2)])/2
        else:
            value=sorted_l[n//2]
    
        return value

print("Sum: ",sum(l))
print("Average: ",average(l))
print("Median: ",median(l))