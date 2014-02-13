# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Sarah Walters
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
from random import shuffle

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """    
    protein = ""
    
    for step in range(0, len(dna)/3):
        codon = dna[3*step : 3*(step+1)]
        for i in range(0, len(codons)):
            for c in codons[i]:
                if codon == c: protein += aa[i]
    return protein
        

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
    tests = [["ATGCCCGGTTTT","MPGF"], ["CGATGCTTCACT", "RCFT"], ["AGTCAGTCAGTC", "SQSV"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + coding_strand_to_AA(test[0])
        

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    rev_comp = ""
    for char in dna:
        rev_comp = lookup(char) + rev_comp
    return rev_comp
    
        
def lookup(char):
    return {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}.get(char, '') #.get throws out any non-ATGC letter
    
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
    tests = [["ATGCCC","TACGGG"], ["CGATGC", "GCTACG"], ["AGTCAG", "TCAGTC"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + get_reverse_complement(test[0])

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    stop = ["TAG", "TAA", "TGA"]
    for i in range(0, len(dna)/3):
        if dna[3*i : 3*(i+1)] in stop:
            return dna[0:3*i]
    return dna
    

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
    """ Unit tests for the get_complement function """
    tests = [["ATGGTGTAGATGTT","ATGGTG"], ["ATGTTTTAAGGCTC", "ATGTTT"], ["ATGTCTGTCGGCTC", "ATGTCTGTCGGCTC"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + rest_of_ORF(test[0])
    
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    proteins = []
    frame = 0
    while frame < len(dna)/3:
        if dna[3*frame:3*(frame+1)] == "ATG":
            protein = rest_of_ORF(dna[3*frame:])
            proteins.append(protein)
            frame += len(protein)/3
        frame += 1
    return proteins
            
     
def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """
    tests = [["CAGATGTGTATGTAGATGACG","['ATGTGTATG', 'ATGACG']"], ["ATGAAGTGAATG", "['ATGAAG', 'ATG']"], ["TGACTGACTGACTGAC", "[]"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + str(find_all_ORFs_oneframe(test[0]))


def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    frame1 = find_all_ORFs_oneframe(dna[0:])
    frame2 = find_all_ORFs_oneframe(dna[1:])
    frame3 = find_all_ORFs_oneframe(dna[2:])
    return frame1+frame2+frame3
    

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
    tests = [["ATGGTGTAGATGTT","['ATGGTG', 'ATGTT']"], ["ATGTTTTAAGGCTC", "['ATGTTT']"], ["ATGTCTGTCGGCTC", "['ATGTCTGTCGGCTC']"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + str(find_all_ORFs(test[0]))


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    return find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))
     
    
def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """
    tests = [["ATGCCCGGTTTT","['ATGCCCGGTTTT']"], ["ATGCATGCGCGT", "['ATGCATGCGCGT', 'ATGCGCGT', 'ATGCAT']"], ["AGTCAGTCAGTC", "[]"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + str(find_all_ORFs_both_strands(test[0]))


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""
    orfs = find_all_ORFs_both_strands(dna)
    longest = ''
    for orf in orfs:
        if len(orf) > len(longest): longest = orf
    return longest
    

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """
    tests = [["ATGCCCGGTTTT","ATGCCCGGTTTT"], ["ATGCATGCGCGT", "ATGCATGCGCGT"], ["AGTCAGTCAGTC", "(empty)"]]
    for test in tests:
        print "input: " + test[0] + ", expected output: " + test[1] + ", actual output: " + longest_ORF(test[0])
    

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    dnaList = list(dna)
    longest = ''
    
    for i in range (0, num_trials):
        shuffle(dnaList)
        shuffled = collapse(dnaList)
        tempLongest = longest_ORF(shuffled)
        if len(tempLongest) > len(longest): longest = tempLongest
        
    return len(longest) 


def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                   length specified.
    """
    orfs = find_all_ORFs_both_strands(dna)
    aboveThreshold = []
    for orf in orfs:
        if len(orf) > threshold:
            aboveThreshold.append(coding_strand_to_AA(orf))
    return aboveThreshold