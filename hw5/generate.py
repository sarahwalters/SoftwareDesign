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
        wts[key] = stresses(key) # stresses('dictionary') produces '1010'


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
    

def limerick(endRhymes):
    '''need to refactor/generalize and document'''
    mLong = '01001001'
    mShort = '01001'
    
    left = [mLong, mLong, mLong, mShort, mShort]
    lines = ['', '', '', '', '']
    ends = []
    
    ### ENDS OF LINES - RHYMING
    for i in range(0,3):
        word = endRhymes[0][i]
        stresses = wts[word]
        left[i] = left[i][:len(left[i])-len(stresses[0])] # not necessarily 0...mult prons
        ends.append(word)
    
    for i in range(3,5):
        word = endRhymes[1][i-3]
        stresses = wts[word]
        left[i] = left[i][:len(left[i])-len(stresses[0])] # once again, mult prons.
        ends.append(word)
    
    for i in range(5):
        while len(left[i]) > 0:
            keyChoice = choice(stw.keys())
            if left[i][0:len(keyChoice)] == keyChoice:
                word = choice(stw[keyChoice])
                stresses = wts[word]
                left[i] = left[i][len(stresses[0]):]
                if len(lines[i]) > 0:
                    lines[i] = lines[i] + ' ' + word
                else:
                    lines[i] = word
                    
    
    for i in range(5):
        lines[i] = lines[i] + ' ' + ends[i]
    print lines[0].capitalize()
    print lines[1].capitalize()
    print lines[3].capitalize()
    print lines[4].capitalize()
    print lines[2].capitalize()
            
        

if __name__ == "__main__":
    filename = 'twoCities.txt'
    build_wts()
    build_stw()
    
    x = endRhymeSets([3, 2], '01001')
    limerick(x)