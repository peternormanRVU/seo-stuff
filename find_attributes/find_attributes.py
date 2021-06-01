import csv
import re

keywords = [line.strip().lower() for line in open('keywords.txt',encoding='utf-8')]
regex = [line.strip().lower().split(',') for line in open('regex.csv')] #what type is regex?

def classify_bucket(data):
    group = None
    holder = None
    for i in regex: #systematically goes through all regex rules for 1st keyword, then all regex rules for 2nd keyword etc...
        #if group != None: #if there is a keyword classification
           #return group #return the classification, ends loop
            #instead of return group, need to append group to string

        #else:
        if re.search(i[1],data) != None: #boolean: if regex condition is in keyword WHY DOES THIS ONLY TAKE FIRST MATCH
            group = i[0] #assign group the classification
        else:
            group = None

        if holder == None:
            if group != None:
                holder = group
            else:
                holder = None
        else:
            if group != None:
                holder += ","
                holder += group
            else:
                holder += ""

    return holder #return nothing when looped through all rules with no match



with open('results.csv', mode='w') as file:
    for key in keywords: #for loop through keyword set
        if classify_bucket(key) == None:
            key = ""
        else:
            key = classify_bucket(key)
        file.write("{}\n".format(key))