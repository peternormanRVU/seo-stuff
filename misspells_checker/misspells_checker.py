from spellchecker import SpellChecker

spell = SpellChecker(language='en')

##spell.word_frequency.load_words(['coronavirus','moneysupermarket','comparethemarket','gocompare'])
keywords = [line.strip().lower() for line in open('keywords.txt',encoding='utf-8')]
valid_keywords = [line.strip().lower() for line in open('valid_keywords.txt',encoding='utf-8')]
spell.word_frequency.load_words(valid_keywords)


def is_empty(any_structure):
    if any_structure:
        ##print('Structure is not empty.')
        return False
    else:
        ##print('Structure is empty.')
        return True

for i in keywords:
    word = i.split() ##creates a tuple each time
    count = 0
    for j in word:
        ##print(word[j])
        misspelled = spell.unknown(word)
        if is_empty(misspelled):
            'cool'
        else:
            count+=1
    print(count)


'''
with open('results.csv', mode='w') as file:
    for key in keywords: #for loop through keyword set
        if classify_bucket(key) == None:
            key = ""
        else:
            key = classify_bucket(key)
'''