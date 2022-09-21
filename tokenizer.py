#input: tokenization-input-part-A.txt
#output: tokenized-A.txt, one term per line, order of tokenizer, stopword removal, stemmer
import re

'''
PART A
------
Step 1: Tokenize input text, abbreviations are only of single alphanumeric characters and only if immediately followed by a period
So "Ph.D." is not an abbreviation for this project and will result in "Ph" and "D" as token
'''
#array to store each line as seperated arrays
lines = []
tokens = []

#helper function to de-acronyze acronyms
def de_acronym(str):
    return str.group().replace(".","")

with open('tokenization-input-part-A.txt') as f:
    for line in f:
        #remove Mr. and Mrs. titles
        line = line.replace("Mr. ","Mr")
        line = line.replace("Mrs. ","Mrs")

        #make all lowercase
        line = line.lower()

        #identify acronyms and remove apostrophes
        cleaned = re.sub(r'\S+\.\S\.(?=.)',de_acronym,line.replace("'",""))

        #remove all punctuation
        tokenized = re.findall(r'[a-zA-Z0-9]+',cleaned)

        if len(tokenized) == 0:
            continue
        tokens.extend(tokenized)
        #print(tokenized)
    #print(tokens)
'''
Step 2: Implement stopword removal based on stopwords.txt
Collapsed abbreviations might be stop words
'''
#store stopwords as a dict
stopwords = {}
with open('stopwords.txt') as f:
    for line in f:
        word = line.strip("\n")
        if word is not None:
            stopwords[word] = ''

#list of tokens with stopwords removed
no_stop = []

for token in tokens:
    if token not in stopwords:
        no_stop.append(token)

'''
Step 3: Implement the first 2 steps of of Porter stemming (defined below)
1a:
- Replace sses by ss (e.g., stresses → stress).
- Delete s if the preceding word part contains a vowel not immediately before the s (e.g., gaps → gap but gas → gas).
- Replace ied or ies by i if preceded by more than one letter, otherwise by ie
(e.g., ties → tie, cries → cri).
- If suffix is us or ss do nothing (e.g., stress → stress).
1b:
- Replace eed, eedly by ee if it is in the part of the word after the first nonvowel following a vowel (e.g., agreed → agree, feed → feed).
- Delete ed, edly, ing, ingly if the preceding word part contains a vowel, and
then if the word ends in at, bl, or iz add e (e.g., fished → fish, pirating →
pirate), or if the word ends with a double letter that is notll,ss, or zz, remove
the last letter (e.g., falling→ fall, dripping → drip), or if the word is short, add
e (e.g., hoping → hope).
'''
stem_list = []

#helper function to carry out step 1b after 1a is applied to a word
def porter_1b(str):
    stem_eedly = re.sub(r'eedly',"ee",str)
    if stem_1b != str:
        return stem_1b


for word in no_stop:
    stem_sses = re.sub(r'sses',"ss",word)
    stem_i = re.sub(r'[a-zA-Z]{2,}ies|[a-zA-Z]{2,}ied',"i",word)
    stem_ie = re.sub(r'[a-zA-Z]ies|[a-zA-Z]ied',"ie",word)

    if stem_sses != word:
        stem_list.append(porter_1b(stem_sses))

    elif stem_i != word:
        stem_list.append(porter_1b(stem_i))

    elif stem_ie != word:
        stem_list.append(porter_1b(stem_ie))
    
    #check constonants
    

        
