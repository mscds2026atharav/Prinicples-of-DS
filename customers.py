import csv
import json

class Customers:
    customerId=0
    firstName=""
    lastName=""
    company=""
    city=""
    country=""
    phone1=""
    phone2=""
    email=""
    subscriptionDate=""
    website=""

list = []

dictList= []

dict={}

header= True

cnt=1

with open("customers-100.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',', quotechar='"')

    for line in reader :
        if(header == True) :
            header = False
            continue
        customer=Customers()
        customer.customerId = line[1]
        customer.firstName = line[2]
        customer.lastName = line[3]
        customer.company = line[4]
        customer.city = line[5]
        customer.country = line[6]
        customer.phone1 = line[7]
        customer.phone2 = line[8]
        customer.email = line[9]
        customer.subscriptionDate = line[10]
        customer.website = line[11]
        list.append(customer)

json_file=open("customer_summary.json", mode="w",encoding="UTF-8")

for item in list :
    print("Customer",cnt,":")
    print("CustomerId:",item.customerId)
    print("Customer Name:",item.firstName,item.lastName)
    print("Company:",item.company)
    print("City:",item.city)
    print("Country:",item.country)
    print("phone1:",item.phone1)
    print("phone2:",item.phone2)
    print("Email:",item.email)
    print("Subscription date:",item.subscriptionDate)
    print("Website:",item.website)
    print(" ")
    cnt=cnt+1

    dict["CustomerId"] = item.customerId
    dict["FirstName"] = item.firstName
    dict["LastName"] = item.lastName
    dict["Company"] = item.company
    dict["City"] = item.city
    dict["Country"] = item.country
    dict["Phone1"] = item.phone1
    dict["Phone2"] = item.phone2
    dict["Email"] = item.email
    dict["SubscriptionDate"] = item.subscriptionDate
    dict["Website"] = item.website

    dictList.append(dict)

json.dump(dictList,json_file, indent=4)