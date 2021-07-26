import sys
import os
import numpy as np

debug = False

# ex : python3 src/bw-search.py ../data/cmv.fasta.idx ATT 
#global params
countOnly = False

def main(infile, q) :
    index = 0
    totalCount = 0
    #readFile
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
    # #decodage_sequence
    subsequence = sequence.copy()

    for i in range(len(sequence) - 1) :
        subsequence.sort()
        for i in range(len(subsequence)) :
            subsequence[i] = sequence[i] + subsequence[i]
    
    # REVOIR DEPUIS ICI --------------------------------------------------------------------------------------------------------------
    #subsequence.sort()
    sequence = []
    for i in range(len(subsequence)) :
        if i%6 == 0 :
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