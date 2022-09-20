#input: tokenization-input-part-A.txt
#output: tokenized-A.txt, one term per line, order of tokenizer, stopword removal, stemmer
import re

'''
PART 1: Tokenize input text, abbreviations are only of single alphanumeric characters and only if immediately followed by a period
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
        #does not remove _ for some reason?
        cleaned = re.sub(r'\S+\.\S\.(?=.)',de_acronym,line.replace("'",""))
        print(re.findall(r'\w+',cleaned))
        
