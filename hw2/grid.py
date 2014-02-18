# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 13:39:51 2014

@problem: Think Python exercise 3.5
@author: swalters
"""

def make_row(c1, c2, w, r):
    # make building block (eg + - - - - )
    block = c1
    for i in range (0, w): block = block + c2
    # add blocks together
    x = ''
    for i in range (0, r): x = x + block
    # add last character
    return x + c1

def print_grid(rows, cols, w, h):
    # make all rows except the last
    for i in range (0, cols):
        # one row with + and -
        print make_row('+ ', '- ', w, rows)
        # cols rows with | and space
        for i in range (0, h): print make_row('| ', '  ', w, rows)
    # make the last row
    print make_row('+ ', '- ', w, rows)

print_grid(4, 4, 4, 4) # (rows, columns, box width, box height)

'''
Great generalization; wonderful work!
'''