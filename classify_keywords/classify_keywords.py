import csv
import re

keywords = [line.strip().lower() for line in open('keywords.txt',encoding='utf-8')]
regex = [line.strip().lower().split(',') for line in open('regex.csv')]

def classify_bucket(data):
    group = None
    for i in regex:
        if group != None:
            return group
        else:
            if re.search(i[1],data) != None:
                group = i[0]
    return ""

with open('results.csv', mode='w') as file:
    for key in keywords:
        key = classify_bucket(key)
        file.write("{}\n".format(key))