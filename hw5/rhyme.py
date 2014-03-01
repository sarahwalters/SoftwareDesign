# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 21:49:55 2014

@author: swalters
"""

from nltk.corpus import cmudict

d = cmudict.dict()

def stresses(word):
    pSet = []
    sylSets = allSyllables(word)
    for sylSet in sylSets:
        p = ''
        for syl in sylSet:
            if '1' in syl or '2' in syl:
                p += '1'
            elif '0' in syl:
                p += '0'
        pSet.append(p)
    return pSet
                

def isRhyme(word1, word2, n, t): # n = number of syllables to rhyme, t = threshold. t = 0 yields exact rhymes.
    rhymePart1 = rhymePart(word1, n)
    rhymePart2 = rhymePart(word2, n)
    for p1 in rhymePart1:
        for p2 in rhymePart2:
            if levenshtein_distance(p1, p2) <= t:
                return True
    return False    
   
   
def rhymePart(word, n): # check for too-big n
    allSyls = allSyllables(word)
    bigEnough = []
    toRhyme = []
    
    for sylSet in allSyls:
        if len(sylSet) >= n:
            bigEnough.append(sylSet)
    
    for sylSet in bigEnough:
        rhymePart = ''
        for i in range(1, n+1):
            rhymePart = sylSet[-i] + rhymePart
            while rhymePart[0] not in ['A', 'E', 'I', 'O', 'U']:
                rhymePart = rhymePart[1:]
            toRhyme.append(rhymePart)
    return toRhyme
    

def allSyllables(word):
    s = []
    if word in d:
        pronunciations = d[word]
        for p in pronunciations:
            s.append(getSyllables(p))
    return s


def getSyllables(pronunciation):
    length = len(pronunciation)
    syllables = [] # for storing list of syllables as they are built
    current = '' # for storing current syllable as it is built
    
    i = 0 # while loop allows for multiple steps per loop
    while i < length:
        # establish current phoneme ph0, next phoneme ph1, and next next phoneme ph2
        ph0 = pronunciation[i]
        
        if length - i > 1: ph1 = pronunciation[i+1]
        else: ph1 = ' ' # leave as just a blank space if no next phoneme (ie ph0 is last)
        
        if length - i > 2: ph2 = pronunciation[i+2]
        else: ph2 = ' ' # if ph1 is last
         
        # for testing
        """
        print 'ph0: ' + ph0
        print 'ph1: ' + ph1
        print 'ph2: ' + ph2
        print '--------'
        """
        
        current += ph0 # add ph0 to current syllable

        if isVowel(ph0):
            # check whether or not to add one following consonant (if at least 2 follow vowel ph0)
            # or multiple following consonants (if this vowel ph0 is the last one)
            if not isVowel(ph1) and not isVowel(ph2): # do two consonants follow ph0?
                current += ph1
                i += 1
                
                rest = pronunciation[i+1:] # check whether to add all remaining consonants
                addRest = True
                for ph in rest:
                    if isVowel(ph): # if there is another vowel
                        addRest = False
                if addRest == True:
                    for ph in rest: current += ph
            syllables.append(current)
            current = ''
        i += 1
    return syllables
    
    
def isVowel(phoneme):
    return phoneme[-1].isdigit()
    
    
levenshteinKnown = {('', ''):0} # memoized
def levenshtein_distance(s1, s2):
    comparison = (s1, s2)
    if comparison in levenshteinKnown:
        return levenshteinKnown[comparison]
    
    if len(s1) == 0:
        res = len(s2)
    elif len(s2) == 0:
        res = len(s1) 
    else:
        res = min([int(s1[0] != s2[0]) + levenshtein_distance(s1[1:],s2[1:]), 1+levenshtein_distance(s1[1:],s2), 1+levenshtein_distance(s1,s2[1:])])
    levenshteinKnown[(s1, s2)] = res
    return res