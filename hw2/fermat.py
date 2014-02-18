# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 14:27:21 2014

@problem: Think Python exercise 5.3
@author: swalters
"""

def check_fermat(a, b, c, n):
    if n > 2 and a**n + b**n == c**n:
        print 'Holy smokes, Fermat was wrong!'
    else:
        print "No, that doesn't work."

# check_fermat(1, 2, 3, 4)

def run_fermat():
    a = raw_input('Enter a value for a: ')
    b = raw_input('Enter a value for b: ')
    c = raw_input('Enter a value for c: ')
    n = raw_input('Enter a value for n: ')
    check_fermat(int(a), int(b), int(c), int(n))
    
run_fermat()

'''
Perfect; no comments
'''