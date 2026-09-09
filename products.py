import csv
import json

file=open("products-100.csv", encoding="UTF-8")
csvfile= csv.reader(file)
header=True

categories = {}

price = {}

for line in csvfile:
    if(header == True) :
        header = False
        continue
    category = line[4]

    if category in categories:
        categories[category] += 1
    else:
        categories[category] = 1
        

for category, freq in categories.items():
    print(category, ":", freq)

file.close()

file=open("products-100.csv", encoding="UTF-8")
csvfile= csv.reader(file)
header=True
for line in csvfile:
    if(header == True) :
        header = False
        continue
    category = line[4]

    if category not in price:
        price[category] = 0
    price[category] = int(price[category]) + (int(line[5])*96.42)*int(line[7])

for category, total_price in price.items():
    print(category, ":", total_price)

file.close()

json_file=open("product_summary.json", mode="w",encoding="UTF-8")
json.dump(price,json_file, indent=4)

json_file.close()

print("data fed into json file")