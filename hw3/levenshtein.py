# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 21:52:43 2014

@author: swalters
"""

def computeLevenshtein(s1, s2):
    len1 = len(s1)
    len2 = len(s2)
    
    # initialize empty matrix
    matrix = [[0 for x in range(len1+1)] for x in range(len2+1)] 
    
    # initialize row 0
    for i in range(1, len1+1):
        matrix[0][i] = i
    
    # initialize column 0
    for i in range(1, len2+1):
        matrix[i][0] = i
     
    # levenshtein algorithm
    for row in range(1, len2+1):
        for col in range(1, len1+1):
            # get surrounding cells
            left = matrix[row][col-1]
            top = matrix[row-1][col]
            diag = matrix[row-1][col-1]
            
            # corresponding letters match
            if s1[col-1] == s2[row-1]:
                matrix[row][col] = diag
            # or don't match
            else:
                matrix[row][col] = min(left, top, diag) + 1          
    return matrix
    

def bestAlignment(s1, s2):
    m = computeLevenshtein(s1, s2)
    cRow = 1
    cCol = 1
    #while cRow < len(s2) and cCol < len(s1):
    right = m[cRow][cCol+1]
    bottom = m[cRow+1][cCol]
    diag = m[cRow+1][cCol+1]
    moves = [right, bottom, diag]
    move = moves.index(min(right, bottom, diag))
    print move