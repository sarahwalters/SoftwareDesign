# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 21:49:55 2014

@author: swalters
"""

from nltk.corpus import cmudict # word-to-phoneme lookup
d = cmudict.dict()

### stress/rhyme methods
def stresses(word):
    ''' produces list of binary strings describing all phonetic stress patterns of word
        input: word (string)
        output: list of strings consisting of 1's and 0's
    '''
    pSet = []
    sylSets = allSyllables(word)
    for sylSet in sylSets:
        p = ''
        for syl in sylSet:
            if '1' in syl or '2' in syl: # in cmudict phonemes, 1 correlates to primary stress, 2 to secondary,
                p += '1' # (label both primary and secondary stress as stressed)
            elif '0' in syl: # and 0 to unstressed
                p += '0'# (label unstressed as such)
        pSet.append(p)
    return pSet
                

def isRhyme(word1, word2, n, t): 
    ''' checks whether two words rhyme to n syllables with matching threshold t (t=0 checks exact rhyme)
        inputs: word1, word2 (strings), n, t (ints)
        output: boolean
    '''
    rhymePart1 = rhymePart(word1, n)
    rhymePart2 = rhymePart(word2, n)
    for p1 in rhymePart1: # rhymePart1 and rhymePart2 are lists - iterate to check for matching elements
        for p2 in rhymePart2:
            if levenshtein_distance(p1, p2) <= t: return True # allows for some degree of slant rhyme if t != 0
    return False
   
   
def rhymePart(word, n):
    ''' returns the part of a word which would match the equivalent part for a rhyming word
        --> the nth vowel from the end and everything after it
        input: word (string) and n (int), number of syllables to consider
        output: list of possible strings to rhyme (same thing for various pronunciations)
    '''
    allSyls = allSyllables(word)
    bigEnough = []
    toRhyme = []
    
    for sylSet in allSyls:
        if len(sylSet) >= n:  # to avoid indexing errors later
            bigEnough.append(sylSet)
    '''
    I think above loop needs either more documentation or a different approach.
    Look into Python's built-in filter function for cleaner code. Using filter will tell 
    the audience that you're filtering the original list (allSyls) to only the data you 
    care about, which are only the syllables that are long enough, given n. I was confused by
    what you meant by "big enough" until I saw the second `for` loop.
    '''
    
    for sylSet in bigEnough:
        part = ''
        for i in range(1, n+1):
            part = sylSet[-i] + part
            while part[0] not in ['A', 'E', 'I', 'O', 'U']: # only keep first char if not consonant
                part = part[1:]
            toRhyme.append(part)
    return toRhyme
    
    
levenshteinKnown = {('', ''):0} # for memoization
def levenshtein_distance(s1, s2):
    ''' recursively computes edit distance between two strings
        input: s1, s2 (strings)
        output: edit distance between them (int)
    '''
    
    # What if known levenshtein includes (s2, s1) but not (s1, s2)?
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


### syllable methods
def allSyllables(word):
    s = []
    if word in d:
        pronunciations = d[word]
        for p in pronunciations:
            s.append(getSyllables(p))
    return s


def getSyllables(pronunciation):
    ''' splits a set of phonemes into syllables
        input: pronunciation (list of phoneme strings)
        output: list of syllables
    '''
    length = len(pronunciation)
    syllables = []
    current = ''
    
    i = 0 # use while loop for multiple steps/loop
    while i < length:
        # establish current phoneme ph0, next phoneme ph1, and next next phoneme ph2
        ph0 = pronunciation[i]
        
        if length - i > 1: ph1 = pronunciation[i+1]
        else: ph1 = ' ' # single space if no next phoneme (ie ph0 is last phoneme)
        
        if length - i > 2: ph2 = pronunciation[i+2]
        else: ph2 = ' ' # if ph1 is last phoneme
        
        current += ph0

        if isVowel(ph0):
            # add exactly one following consonant if at least 2 consonants follow vowel ph0
            # also add all remaining consonants if vowel ph0 is the last vowel
            
            # do two consonants follow ph0?
            if not isVowel(ph1) and not isVowel(ph2): 
                current += ph1
                i += 1
                
                # is ph0 the last vowel?
                rest = pronunciation[i+1:]
                addRest = True
                for ph in rest:
                    if isVowel(ph):
                        addRest = False # because there is another vowel
                if addRest == True:
                    for ph in rest: current += ph
                    # or just: current += "".join(rest)
                    
            # syllable finished; move to the next
            syllables.append(current.strip())
            current = '' 
        i += 1
    return syllables

'''
Awesome documentation on the above function. It would have been hard to follow
your code without them.
'''
    
def isVowel(phoneme):
    ''' checks whether phoneme is in cmudict set of vowels
        input: phoneme (string)
        output: boolean
    '''
    return phoneme[-1].isdigit() # format of all cmudict vowel phonemes