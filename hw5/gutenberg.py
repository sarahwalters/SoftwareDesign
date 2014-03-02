# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:07:24 2014

@author: swalters
"""

import re

def openFile(filename):
    ''' opens file, gets text, closes file
        input: filename (string), of format 'name.txt'
        output: all text in filename (string)
    '''
    f = open(filename, 'r')
    fulltext = f.read()
    f.close()
    return fulltext


def clean(gutenbergText):
    ''' strips Project Gutenberg boilerplate from the text of a book
        input: gutenbergText (string), from Project Gutenberg book
        output: substring of gutenbergText which is the body of the book
    '''
    startIndex = gutenbergText.find(' ***') # always at the end of introductory boilerplate
    endIndex = gutenbergText.find('End of the Project Gutenberg') # at beginning of ending boilerplate
    return gutenbergText[startIndex+4:endIndex] # startIndex is space before three asterisks


def get_words_from_book(filename): 
    ''' produces sequential list of words in a book
        input: filename (string) in format 'name.txt'
        output: words in cleaned text (list)
    '''
    text = clean(openFile(filename))
    wordList = []
    for word in re.findall('[a-zA-Z\'\-]+', text): # match all alphabetical chars and apostrophe, hyphen
        wordList.append(word)
    return wordList


def get_word_count_dict(filename):
    ''' describes a text by how many times each word it uses occurs
        input: filename (string) in format 'name.txt'
        output: dictionary which maps from word to number of occurrences
    '''
    words = get_words_from_book(filename)
    analysis = {}
    for word in words:            
        if word.lower() in analysis:
            analysis[word.lower()] += 1
        else:
            analysis[word.lower()] = 1
    return analysis