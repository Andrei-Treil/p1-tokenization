#input: tokenization-input-part-A.txt, tokenization-input-part-B.txt
#output: tokenized-A.txt, terms-B.txt, vocab_growth.pdf
import re
import sys
from collections import Counter,defaultdict
import matplotlib.pyplot as plt



def main(file,arg):

    #variable to indicate wether a graph needs to be made
    should_graph = arg
    
    '''
    Step 1: Tokenize input text, abbreviations are only of single alphanumeric characters and only if immediately followed by a period
    So "Ph.D." is not an abbreviation for this project and will result in "Ph" and "D" as token
    '''

    #array to store each line as seperated arrays
    tokens = []

    #helper function to de-acronyze acronyms
    def de_acronym(str):
        return str.group().replace(".","") + "."

    with open(file) as f:
        for line in f:
            #remove Mr. and Mrs. titles
            line = re.sub(r'(Mr[s]{0,1})\.\s([a-zA-Z0-9])',r'\1\2',line)
            
            #make all lowercase
            line = line.lower()

            #identify acronyms and remove apostrophes
            cleaned = re.sub(r'\S+\.\S\.(?=.)',de_acronym,line.replace("'",""))

            #remove all punctuation
            tokenized = re.findall(r'[a-zA-Z0-9]+',cleaned)

            if len(tokenized) == 0:
                continue
            tokens.extend(tokenized)


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

    #only add non stopwords to the no_stop list
    for token in tokens:
        if token not in stopwords:
            no_stop.append(token)

    '''
    Step 3: Implement the first 2 steps (1a,1b) of Porter stemming
    '''
    stem_list = []

    #helper function for porter_1b to check for word endings and length for words ending in ed, edly, ing, ingly
    def porter_1b_helper(stem_1b):
        stem_atbliz = re.sub(r'[at,bl,iz]$',r'e',stem_1b)
        if stem_atbliz != stem_1b:
            return stem_atbliz
        
        stem_dub_let = re.sub(r'(.)[^lsz]$',r'\1',stem_1b)
        if stem_dub_let != stem_1b:
            return stem_dub_let
        
        stem_short = re.sub(r'\A([^aeiou]{0,}[aeiou]{1,}[^aeiou]{1,}[aeiou]{0,})$',r'\1e',stem_1b)
        if stem_short != stem_1b:
            return stem_short
        
        return stem_1b

    '''
    porter 1b:
    - Replace eed, eedly by ee if it is in the part of the word after the first nonvowel following a vowel (e.g., agreed → agree, feed → feed).
    - Delete ed, edly, ing, ingly if the preceding word part contains a vowel, and
    then if the word ends in at, bl, or iz add e (e.g., fished → fish, pirating →
    pirate), or if the word ends with a double letter that is not ll,ss, or zz, remove
    the last letter (e.g., falling→ fall, dripping → drip), or if the word is short, add
    e (e.g., hoping → hope).
    short: [C]VC[V] -> must be CVCV, CVC, VCV, or VC
    '''

    #function to carry out step 1b after 1a is applied to a word
    #attempt to apply a rule to the word, if it doesnt change the word, try the next largest rule
    def porter_1b(str):
        stem_eedly = re.sub(r'(\A[aeiou]{1,}[^aeiou][a-z]ee)dly',r'\1',str)
        if stem_eedly != str:
            return stem_eedly

        stem_ingly = re.sub(r'([aeiou][a-zA-Z]*)ingly',r'\1',str)
        if stem_ingly != str:
            return porter_1b_helper(stem_ingly)

        stem_edly = re.sub(r'([aeiou][a-zA-Z]*)edly',r'\1',str)
        if stem_edly != str:
            return porter_1b_helper(stem_edly)

        stem_eed = re.sub(r'(\A[aeiou]{1,}[^aeiou][a-z]ee)d',r'\1',str)
        if stem_eed != str:
            return stem_eed
        
        stem_ing = re.sub(r'([aeiou][a-zA-Z]*)ing',r'\1',str)
        if stem_ing != str:
            return porter_1b_helper(stem_ing)
        
        stem_ed = re.sub(r'([aeiou][a-zA-Z]*)ed',r'\1',str)
        if stem_ed != str:
            return porter_1b_helper(stem_ed)

        return str
        
    '''
    porter 1a:
    - Replace sses by ss (e.g., stresses → stress).
    - Delete s if the preceding word part contains a vowel not immediately before the s (e.g., gaps → gap but gas → gas).
    - Replace ied or ies by i if preceded by more than one letter, otherwise by ie
    (e.g., ties → tie, cries → cri).
    - If suffix is us or ss do nothing (e.g., stress → stress).
    '''
    #attempt to apply a rule to the word, if it doesnt change the word, try the next largest rule
    for word in no_stop:
        stem_sses = re.sub(r'sses',"ss",word)
        if stem_sses != word:
            stem_list.append(porter_1b(stem_sses))
            continue
        
        stem_ie = re.sub(r'(ie)[s,d]',r'\1',word)
        if stem_ie != word:
            stem_list.append(porter_1b(stem_ie))
            continue

        if re.search(r'[ss,us]$',word) is not None:
            stem_list.append(porter_1b(word))
            continue 

        stem_i = re.sub(r'([a-zA-Z]{2,}i)e[s,d]',r'\1',word)
        if stem_i != word:
            stem_list.append(porter_1b(stem_i))
            continue
        
        stem_s = re.sub(r'([aeiou][a-zA-z]*)(?<![aeiou])s',r'\1',word)
        if stem_s != word:
            stem_list.append(porter_1b(stem_s))
            continue
        
        stem_list.append(porter_1b(word))
    
    #if processing part A
    if file == 'tokenization-input-part-A.txt':
        with open("tokenized-A.txt","w") as out:
            for word in stem_list:
                out.write(word + "\n")

    #if processing part B
    else:
        #make graph
        if should_graph is not None:
            words_collection = []
            words_vocab = []
            num_unique = 0
            unique_words = defaultdict(int)

            for i in range(len(stem_list)):
                if unique_words[stem_list[i]] == 0:
                    num_unique += 1
                unique_words[stem_list[i]] += 1
                words_collection.append(i)
                words_vocab.append(num_unique)
            
            plt.plot(words_collection,words_vocab)
            plt.xlabel('Words in Collection')
            plt.ylabel('Words in Vocabulary')
            plt.savefig('vocab_growth.pdf')
            plt.show()

        #make list of top 300 words
        word_freq = Counter(stem_list).most_common(300)
        with open("terms-B.txt","w") as out:
            for key,val in word_freq:
                out.write(key + " " + str(val) + "\n")

    


if __name__ == '__main__':
    #allows program to run with argument "graph" to create the graph needed for analysis
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = None
    main('tokenization-input-part-A.txt',arg)
    main('tokenization-input-part-B.txt',arg)

    
