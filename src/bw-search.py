#!/usr/bin/env python3
import sys
import numpy as np

debug = False

# ex : python3 src/bw-search.py ../data/cmv.fasta.idx ATT 
#global params
countOnly = False

def clearBinaryString(string) :
    string = str(string)
    if string[:2] == "b\'" and string[-1] == "\'":
        string = string[2:-1]
    return string

def main(infile, q) :
    index = 0
    totalCount = 0
    compressed = False
    #readFile

    #check if compression
    
    if (infile.split('.')[-1] == 'idxc') :
        compressed = True
        #remplacer par flag header[0] ?

    if compressed == True : 
        infile = open(infile, "rb")
        infos = []
        for line in infile:
            line = line.rstrip()
            infos.append([line])
        infile.close

        header = clearBinaryString(infos[0][0])
        header = np.fromstring(header, dtype=int, sep=' ')
        indexes = clearBinaryString(infos[1][0])
        indexes = np.fromstring(indexes, dtype=int, sep=',')
        sequence = [s for s in line]
        res = []
        for seq in sequence :
            #if seq[:2] == "0b" : 
            seq = bin(int(seq))[2:].zfill(8)[::-1]
            for j in range(len(seq)) :
                if j%2 == 0 :
                    value = "" + seq[j+1] + seq[j]
                    if value == "00" :
                        res.append('A')
                    elif value == "01" :
                        res.append('C')
                    elif value == "10" :
                        res.append('G')
                    elif value == "11" :
                        res.append('T')
        sequence = res[:header[1]]
        sequence += ['$']
        sequence += res[header[1]::]
        if header[2] != 0 :
            sequence = sequence[:-(header[2])]

    else : 
        infile = open(infile, "r")
        infos = []
        for line in infile:
            line = line.rstrip()
            infos.append([line])
        infile.close

        header = infos[0]
        indexes = np.fromstring(infos[1][0], dtype=int, sep=',')
        sequence = infos[2][0]
        sequence = [sequence[j] for j in range(len(sequence))]
        header = np.fromstring(header[0], dtype=int, sep=' ')
    
    f = header[-1]

    subsequence = sequence.copy()

    for i in range(len(sequence) - 1) :
        subsequence.sort()
        for i in range(len(subsequence)) :
            subsequence[i] = sequence[i] + subsequence[i]

    sequence = []
    for i in range(len(subsequence)) :
        if i%f == 0 :
            index = indexes[0]
            indexes = indexes[1::]
        else :
            index = len(subsequence) - len(subsequence[i].split("$")[0])
        sequence.append([subsequence[i], index])

    indexes = [seq[1] for seq in sequence]
    res = []
    sequence.sort()
    sequence = sequence[0][0]
    for j in range(len(sequence)) :
        if sequence[:len(q)] == q :
            if countOnly == False :
                res.append((len(sequence) - j - 1))
            else :
                totalCount += 1
        sequence = sequence[-1] + sequence[:-1]

    if countOnly == True :
        print(totalCount)
    else :
        for elt in indexes :
            if elt in res :
                print(elt)

# ----------- MAIN FUNCTION ----------- 
if __name__ == "__main__" :
    countOnly = False
    argv = sys.argv

    options = []
    input = []

    #argc/argv parser
    for arg in argv :
        if "bw-search.py" in arg :
            continue
        elif "--" in arg :
            options.append(arg)
        else :
            input.append(arg)

    # global options params
    if "--count-only" in options :
        countOnly = True
    
    if (len(input)) < 2 :
        raise Exception("ERROR : default case, please add arguments : \n \t infile, q")

    main(infile=input[0], q=input[1])
