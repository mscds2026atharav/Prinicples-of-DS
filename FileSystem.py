import csv
file = open("/home/atharvmscds/ATHARV KOCHAREKAR/people-100.csv")

header = True

list=[0] * 12

monthlist=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

for line in file :
    if(header == True):
        header = False
        continue
    recordDetails = line.split(',')
    date = recordDetails[7]
    dateline = date.split('-')
    month = int(dateline[1])

    list[month-1]=list[month-1]+1

# print(list)

print("MONTH \t COUNT \t BUDGET")
for i in range(0,12) :
    print(monthlist[i],"\t",list[i],"\t",list[i]*1000)

file.close()


# with open("/home/atharvmscds/ATHARV KOCHAREKAR/budget.csv","w", newline="") as budget :
#     writer = csv.writer(budget)
#     writer.writerow(["MONTH","COUNT","BUDGET"])
#     for i in range(0,12) :
#         writer.writerow([monthlist[i],list[i],list[i]*1000])



budget = open("/home/atharvmscds/ATHARV KOCHAREKAR/budget.csv","w", newline="")

budget.write("MONTH,COUNT,BUDGET\n")
for i in range(0,12) :
        budget.write(f"{monthlist[i]},{list[i]},{list[i]*1000}\n")

print("Data Written Succesfully")