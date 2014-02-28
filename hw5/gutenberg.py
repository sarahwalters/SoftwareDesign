# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:07:24 2014

@author: swalters
"""

import re

def openFile(filename):
    f = open(filename, 'r')
    fulltext = f.read()
    f.close()
    return fulltext
    
def clean(text):
    startIndex = text.find(' ***')
    endIndex = text.find('End of the Project Gutenberg')
    return text[startIndex+4:endIndex]

def get_words_from_book(filename): # file must be from Project Gutenberg, filename must have .txt extension
    text = clean(openFile(filename))
    wordList = []
    for word in re.findall('[\w\']+', text):
        wordList.append(word)
    return wordList

def get_word_count_dict(filename):
    words = get_words_from_book(filename)
    analysis = {}
    for word in words:
        if word[0] == '_':
            word = word[1:]
        if len(word) > 0 and word[-1] == '_':
            word = word[:-1]
        if word.lower() in analysis:
            analysis[word.lower()] += 1
        else:
            analysis[word.lower()] = 1
    return analysis