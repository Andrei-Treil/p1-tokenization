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

with open('tokenization-input-part-A.txt') as f:
    for line in f:
        print(re.findall(r'\S+\.\S\.(?=.)',line.replace("'","")))
