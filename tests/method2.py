#!/bin/python3
import time
import sys
import os
import numpy as np

import resource 

methode1 = False

#sequence = "AGTAAAGGAGAAGAACTTTTCACTGGAGTTGTGACAATTCTTGTTGAATTAGATGGTGATGTTAATGGTCACAAATTTTCTGTTAGTGGAGAGGGTGAAGGTGATGCAACATACGGAAAACTTACCCTTAAATTTATTTGTACTACTGGAAAACTACCTGTTCCCTGGCCAACACTTGTTACTACTTTGACTTATGGTGTTCAATGTTTTTCAAGATACCCAGATCACATGAAACGGCACGACTTTTTCAAGAGTGCAATGCCCGAAGGTTATGTACAAGAAAGAACTATTTTTTTCAAAGATGACGGTAACTACAAGACACGTGCTGAAGTTAAGTTTGAAGGTGATACCCTTGTTAATAGAATCGAGTTAAAAGGTATTGATTTTAAAGAAGATGGAAACATTCTTGGACACAAATTGGAATACAACTATAACTCACACAATGTATACATTATGGCAGACAAACAAAAGAATGGAATCAAAGTTAACTTCAAAATTAGACACAACATTGAAGATGGAAGTGTTCAACTAGCAGACCATTATCAACAAAATACTCCAATTGGCGATGGCCCTGTTCTTTTACCAGACAACCATTACCTGTCCACACAATCTGCTCTTTCTAAAGATCCCAACGAAAAGAGAGACCATATGGTGCTTCTTGAGTTTGTAACAGCTGCTGGTATTACACACGGTATGGATGAACTATACAAACACCATCACCATCACCATCACTAG" + "$"
infile = "../data/gfp.fasta"
infile = open(infile, "r")
data = infile.readlines()
infile.close()
sequence = ""
data[1:]

for index, line in enumerate(data) :
    if index != 0 :
        #suppression \n \t 
        line = line.rstrip()
        sequence += line

    # ajout $ au debut de la sequence
sequence += "$"

f = 5

if not methode1 :
    print("methode2")
    sequence = list(sequence)
    cutterLen = len(sequence) + 1
    res = []
    for j in range(len(sequence)) :
        if j%cutterLen == 0 :
            res.append(sequence[j:j+cutterLen])
    sequence = res
    res = []
    index = 1
    for subsequence in sequence :
        res = []
        for i in range(len(subsequence)) :
            if subsequence[i] == '$' :
                index = 0
            subsequence[i] = (subsequence[i], [index])
            index += 1

        # REVOIR CETTE PARTIE ICI
        for elt in range(len(subsequence)) :
            res.append(subsequence)
            subsequence = [subsequence[-1]] + subsequence[:-1]

    table = []
    for elt in res : 
        table.append([[i[0] for i in elt], [i[1] for i in elt]])

    for i in range(len(table)) :
        strA = ""
        table[i][0] =  strA.join(table[i][0])
        #table[i] = strA
        #print(table[i][0])

    table.sort(key=lambda x:x[0])
    for elt in table : 
        print(elt[0][-1], elt[1][-1])
else : 
    arrayRes = []

    for j in sequence : 
        arrayRes.append(sequence)
        sequence = sequence[-1] + sequence
        sequence = sequence[:-1]
        
    # verif matrice carre 
    np.size(arrayRes) == len(sequence)
    if np.size(arrayRes) != len(sequence) :
        raise Exception("ERROR : la matrice n'est pas carree")

    # tableau 2D avec index
    index = 1
    for j in range(len(arrayRes)) :
        arrayRes[j] = (arrayRes[j], index)
        index += 1

    # tri par ordre croissant
    arrayRes.sort()

    # ligne 2 : indexes i1, i2, ...
    indexArray = []
    for i in arrayRes :
        indexArray.append(len(sequence) - i[1])
    indexArray = indexArray[::f]

    # ligne 3 : sequence avec $
    res = ""
    for index_, line in enumerate(arrayRes) :
        res += line[0][-1]

    indexes = ""
    i = 0
    for elt in indexArray :
        if i != 0 :
            indexes += ','
        i += 1
        indexes += str(elt)
    indexes += "\n"

    print(indexes)
    for elt in arrayRes :
        print(elt[0][-1], elt[1])

if methode1 :
    print("methode1")
else :
    print("methode2")

#MEMORY STATS
memMb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0/1024.0
print ("mem : %5.1f MByte" % (memMb))