# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:02:04 2014

@author: pruvolo
"""

from os import path

def load_seq(fasta_file):
    """ Reads a FASTA file and returns the DNA sequence as a string.

    fasta_file: the path to the FASTA file containing the DNA sequence
    returns: the DNA sequence as a string
    """
    retval = ""
    f = open(fasta_file)
    lines = f.readlines()
    for l in lines[2:]:
        retval += l[0:-1]
    f.close()
    return retval
    
    
def load_salmonella_genome():
    f = open(path.join('.','data','salmonella_all_proteins'))
    lines = f.readlines()
    retval = []
    gene = []
    is_amino_acid_seq = False
    
    for line in lines:
        if line[5:].find("CDS") == 0:
            coords = line[21:-1]
            if len(gene) != 0:
                retval.append(gene)
            gene = [coords]
        elif line[21:].find("/protein_id") == 0:
            gene.append(line[34:-2])
        elif line[21:].find("/translation") == 0:
            if line[-2] != '"':
                amino_acid_seq = line[35:-1]
                is_amino_acid_seq = True
            else:
                amino_acid_seq = line[35:-2]
                gene.append(amino_acid_seq)
        elif is_amino_acid_seq:
            if line[-2] != '"':
                amino_acid_seq += line[21:-1]
            else:
                amino_acid_seq += line[21:-2]
                is_amino_acid_seq = False
                gene.append(amino_acid_seq)
    f.close()
    return retval
    
def search_genome_simple(query):
    genome = load_salmonella_genome()
    matchNames = []
    for entry in genome:
         if len(entry) == 3 and query in entry[2]:
            matchNames.append(entry[1])
    return matchNames
    
    
def search_genome_levenshtein(query, threshold):
    genome = load_salmonella_genome()
    matchNames = []
    for entry in genome:
        if len(entry) == 3 and computeLevenshtein(query, entry[2]) <= threshold:
                matchNames.append(entry[1])
    return matchNames
    
    
def search_genome_levenshtein_unit_tests():
    print "CAD01154.1: MNRISTTTITTITITTGNGAG"
    print "Running unit tests with threshold 1..."
    tests = [["MNRSTTTITTITITTGNGAG","CAD01154.1"], ["MNRIQSTTTITTITITTGNGAG", "CAD01154.1"], ["MNRQSTTTITTITITTGNGAG", "CAD01154.1"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + str(search_genome_levenshtein(test[0], 1))


def search_genome_levenshtein_substrings(query, threshold, substrLen):
    genome = load_salmonella_genome()
    matchNames = []
    for entry in genome:
        if len(entry) == 3:
            peptide = entry[2]
            for i in range(len(peptide)-substrLen+1):
                if computeLevenshtein(query, peptide[i:i+substrLen])[-1][-1] <= threshold:
                    matchNames.append(entry[1])
                    break
    return matchNames


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