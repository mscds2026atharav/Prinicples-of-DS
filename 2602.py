#Roll no: 2602
words=["ant","apple","avacado","bat","banana","cherry","cat","ant","appricot","a","car"]

iterated_words=[]

dict={}

def get_count_of_words(alpha,list):
    temp=[]
    count=0
    for word in list:
        if word not in temp:
            temp.append(word)
            if word[0]==alpha:
                count=count + 1
    return count

def get_longest_word(word_List):
    temp=0
    length=0
    longest=""
    for word in word_List:
        for i in word:
            temp=temp+1
        if temp >= length:
            length = temp
            longest=word
        temp=0
    return longest

def get_shortest_word(word_List):
    temp=0
    length=0
    shortest=""
    for word in word_List:
        for i in word:
            temp=temp+1
        if word == word_List[0]:
            length=temp
            shortest=word
            temp=0
        elif temp <= length:
            length = temp
            shortest = word
        temp=0
    return shortest

for word in words:
    if word != "":
        if word not in iterated_words:
            iterated_words.append(word)
            alphabet=word[0]
            if alphabet not in dict:
                dict[alphabet]={
                    'words':[],
                    'count':0,
                    'longest':'',
                    'shortest':''
                }

            dict[alphabet]["words"].append(word)
            
            count=get_count_of_words(alphabet,words)
            dict[alphabet]["count"]=count

            dict[alphabet]["longest"]=get_longest_word(dict[alphabet]["words"])

            dict[alphabet]["shortest"]=get_shortest_word(dict[alphabet]["words"])

print("Dictionary")
print("\n",dict)

print("\nFormated Dictionary\n")
for i in dict:
    print("{")
    print(" '",i,"':{")
    print("\twords:",dict[i]["words"],",")
    print("\tcount:",dict[i]["count"],",")
    print("\tlongest:",dict[i]["longest"],",")
    print("\tshortest:",dict[i]["shortest"])
    print("},")