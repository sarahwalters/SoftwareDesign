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

### build functions
def build_wts():
    counts = get_word_count_dict(filename)

    countSum = 0
    for key in counts:
        countSum += counts[key]

    for key in counts:
        wts[key] = stresses(key)
    return wts


def build_stw():
    for word in wts:
        stresses = wts[word]
        for stress in stresses:
            if stress in stw:
                if word not in stw[stress]:
                    stw[stress].append(word)
            else:
                stw[stress] = [word]
    return stw
    
    
def build_rhymeCollection(wordList):
    for word in wordList:
        rhymed = False
        for key in rhymes:
            if isRhyme(key, word, 1, 0):
                rhymes[key].append(word)
                rhymed = True
        if rhymed == False:
            rhymes[word] = [word]


def rhymeSets(N): # N is matrix describing how many sets and number of matches per set
    allRhymes = []
    for s in range(len(N)):
        thisRhyme = []
        n = N[s] # number of matches for this particular set
        keyChoice = choice(rhymes.keys())
        counter = 0
        while len(rhymes[keyChoice]) < n and counter < 10:
            keyChoice = choice(rhymes.keys())
            counter += 1
        if counter == 10:
            return 'Element ' + str(s) + ' in query too large'
        for i in range(n):
            wordChoice = choice(rhymes[keyChoice])
            while wordChoice in thisRhyme:
                wordChoice = choice(rhymes[keyChoice])
            thisRhyme.append(wordChoice)
        allRhymes.append(thisRhyme)
    return allRhymes

def endRhymes(N, endQuery):    
    endPatterns = []
    for i in range(len(endQuery)):
        if endQuery[i:] in stw:
            endPatterns += stw[endQuery[i:]]
    build_rhymeCollection(endPatterns)
    return rhymeSets(N)
    

def limerick(endRhymes):
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
    print lines[0]
    print lines[1]
    print lines[3]
    print lines[4]
    print lines[2]
            
        

if __name__ == "__main__":
    filename = 'twoCities.txt'
    build_wts()
    build_stw()
    
    x = endRhymes([3, 2], '01001')
    limerick(x)