# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:02:45 2014

@author: swalters
"""

from rhyme import isRhyme, stresses
from gutenberg import get_word_count_dict
from random import choice

filename = ''
wts = {} # maps from word to stress pattern
stw = {} # maps from stress pattern to words
rhymes = {}
    

### dictionary building functions
def build_wts():
    ''' builds a dictionary which maps from word to binary-format stress pattern(s)
        input: no parameters. Uses global variable filename
        output: no return. Sets global variable wts
    '''
    counts = get_word_count_dict(filename) # maps from word to num of appearances in filename
    for key in counts:
        keyStress = stresses(key)
        if len(keyStress) > 0 and len(keyStress[0]) > 0:
            wts[key] = keyStress # stresses('dictionary') produces '1010'


def build_stw():
    ''' combs through wts to build a dictionary which maps from stress pattern to words
        input: no parameters. Uses global variable wts
        output: no return. Sets global variable stw
    '''
    for word in wts:
        stresses = wts[word]
        for stress in stresses:
            if stress in stw:
                if word not in stw[stress]:
                    stw[stress].append(word)
            else:
                stw[stress] = [word]
    
    
def build_rhymes(wordList):
    ''' builds a dictionary which maps from representative word to all rhymes in wordList
        input: wordList (format ['word1', 'word2', 'word3', ...])
        output: no return. Sets global variable rhymes
    '''
    for word in wordList:
        rhymed = False
        for key in rhymes:
            if isRhyme(key, word, 1, 0): # only one-syllable (1) exact (0) rhymes for now
                rhymes[key].append(word)
                rhymed = True
        if rhymed == False:
            rhymes[word] = [word]


### functionality functions
def rhymeSets(N): # N is matrix describing how many sets and number of matches per set
    ''' produces a set of n rhyming words for each integer n in the list N
        input: N (list of integers)
        output: list of sets of rhyming words
    '''
    allRhymeSets = []
    for i in range(len(N)):
        thisRhymeSet = []
        n = N[i] # number of matches to find for this particular set
        
        # pick set of words to pull from
        counter = 0
        keyChoice = choice(rhymes.keys())
        while len(rhymes[keyChoice]) < n and counter < 10: # to prevent for looking forever for n which is bigger than any which exist
            keyChoice = choice(rhymes.keys())
            counter += 1
        if counter == 10:
            raise RuntimeError('Element ' + str(i) + ' in query is probably too large')
            
        # pull correct number of words from chosen set
        for i in range(n):
            wordChoice = choice(rhymes[keyChoice])
            while wordChoice in thisRhymeSet: # avoid duplicity 
                wordChoice = choice(rhymes[keyChoice])
            thisRhymeSet.append(wordChoice)
            
        allRhymeSets.append(thisRhymeSet)
        
    return allRhymeSets


def endRhymeSets(N, endQuery): 
    ''' exactly like rhymeSets, but chooses words which fit at the end of syllable pattern endQuery
        input: N (list of integers), endQuery (string of 1's and 0's)
        output: list of sets of rhyming words which have stress patterns matching end of endQuery
    '''
    endPatterns = []
    for i in range(len(endQuery)): # run through substrings of endQuery which end at the end
        if endQuery[i:] in stw: # use all which exist in stw for largest possible variety of words
            endPatterns += stw[endQuery[i:]]
    build_rhymes(endPatterns)
    return rhymeSets(N)
    

def poem(lines, endQuery):
    poemRes = ''
    
    # extract rhyme scheme
    rhymeScheme = {}
    for line in lines:
        if line[1] in rhymeScheme:
            rhymeScheme[line[1]] += 1
        else:
            rhymeScheme[line[1]] = 1

    # produce rhymes
    N = []
    for match in rhymeScheme:
        N.append(rhymeScheme[match])
    rhymeSets = endRhymeSets(N, endQuery)
    
    # replace numbers in rhymeScheme with sets of rhymes
    for schemeChar in rhymeScheme:
        for rhymeSet in rhymeSets:
            if len(rhymeSet) == rhymeScheme[schemeChar]:
                rhymeScheme[schemeChar] = rhymeSet
                rhymeSets.remove(rhymeSet)
            break
    
    # put rhymes into ends of lines
    for line in lines:
        word = rhymeScheme[line[1]].pop()
        stresses = wts[word]
        line[0] = line[0][:len(line[0])-len(stresses[0])] # not necessarily 0...mult prons  
        line[1] = word
        line.append('')
        while len(line[0]) > 0:
            keyChoice = choice(stw.keys())
            if line[0][0:len(keyChoice)] == keyChoice:
                word = choice(stw[keyChoice])
                stresses = wts[word]
                line[0] = line[0][len(stresses[0]):]
                line[2] = line[2] + ' ' + word
        line[2] = (line[2] + ' ' + line[1]).strip().capitalize()
        poemRes = poemRes + '\n' + line[2]
    return poemRes.strip()
    
def title(poem):
    pList = poem.split()
    word1 = choice(pList).capitalize()
    word2 = choice(pList).capitalize()
    while word2 == word1:
        word2 = choice(pList).capitalize()
    return word1 + ' ' + word2
     
def sonnet():
    print 'Composing poem...'
    s = '01'*5
    r = 'ABABCDCDEFEFGG'
    lines = []
    for char in r:
        lines.append([s, char])
    return poem(lines, s)
        

def limerick():
    print 'Composing poem...'
    l = '01001001'
    s = '01001'
    lines = []
    for i in range(2): lines.append([l, 'A'])
    for i in range(2): lines.append([s, 'B'])
    lines.append([l, 'A'])
    return poem(lines, s)
  
  
'''MAIN METHOD - EDIT THIS'''
if __name__ == "__main__":
    ################################
    '''CHANGE THIS FILENAME'''      
    filename = 'twoCities.txt'
    ################################
    
    # dictionary generation
    build_wts()
    build_stw()
    
    ################################
    '''CHOOSE ONE TYPE'''           
    #p = limerick()
    p = sonnet()
    ################################
    
    # output formatting
    print ''
    t = title(p)
    print t
    print '-'*len(t)
    print p
    print ' '*15 + "--Robot Frost, 'Poems Ipsum' 2014"