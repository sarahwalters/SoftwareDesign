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


def endRhymes(N): # N is matrix describing how many sets and number of matches per set
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
    
    
if __name__ == "__main__":
    filename = 'twoCities.txt'
    build_wts()
    build_stw()
    
    endPatterns = []
    endQuery = '01001'
    for i in range(len(endQuery)):
        if endQuery[i:] in stw:
            endPatterns += stw[endQuery[i:]]
    build_rhymeCollection(endPatterns)
    print endRhymes([3, 2])