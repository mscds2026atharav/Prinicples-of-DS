from datetime import datetime

file = open("people-100.csv", "r")

male_under = 0
female_under = 0

male_work = 0
female_work = 0

male_retire = 0
female_retire = 0

header = True
today = datetime.today()

for line in file:
    if(header == True):
        header = False
        continue

    data = line.strip().split(",")

    dob = data[7]
    gender = data[4].strip().lower()

    dob = datetime.strptime(dob, "%Y-%m-%d")

    age = today.year - dob.year

    if(today.month, today.day) < (dob.month, dob.day):
        age = age - 1

    if(age <= 14):
        if(gender == "male"):
            male_under = male_under + 1
        elif(gender == "female"):
            female_under = female_under + 1

    elif(age <= 59):
        if(gender == "male"):
            male_work = male_work + 1
        elif(gender == "female"):
            female_work = female_work + 1

    else:
        if(gender == "male"):
            male_retire = male_retire + 1
        elif(gender == "female"):
            female_retire = female_retire + 1

file.close()

output = open("age_gender_summary.csv", "w")

output.write("Age Category,Male,Female,Total\n")

output.write("Underage (0-14)," + str(male_under) + "," + str(female_under) + "," + str(male_under + female_under) + "\n")

output.write("Working Age (15-59)," + str(male_work) + "," + str(female_work) + "," + str(male_work + female_work) + "\n")

output.write("Retiring Age (60+)," + str(male_retire) + "," + str(female_retire) + "," + str(male_retire + female_retire) + "\n")

output.write("Total," + str(male_under + male_work + male_retire) + "," + str(female_under + female_work + female_retire) + "," + str(male_under + male_work + male_retire+female_under + female_work + female_retire) + "\n")

output.close()

print("age_gender_summary.csv created successfully")