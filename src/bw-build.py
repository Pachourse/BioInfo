#!/usr/bin/env python3
import sys
import os
import numpy as np

debug = False

#global params
compression = False

def main(infile, outfile, f) :
    f = int(f)
    # debug
    if debug == True :
        print("compression : ", compression)
        print(infile, outfile, f)
    # si compression : Faux -> c=0, n=0, p=0
    # exemples : 
    #   .idxc -> compresse
    #   .idx -> non compresse

    #lecture du fichier d'input
    infile = open(infile, "r")
    data = infile.readlines()
    infile.close()
    originalSequence = ""
    data[1:]

    for index, line in enumerate(data) :
        if index != 0 :
            #suppression \n \t 
            line = line.rstrip()
            originalSequence += line

    # ajout $ au debut de la sequence
    originalSequence = "$" + originalSequence


    # read sequence form file (line 2 to end)
    # add $ at start
    arrayRes = []

    sequence = originalSequence
    for j in originalSequence : 
        arrayRes.append(sequence)
        sequence = sequence[-1] + sequence
        sequence = sequence[:-1]
        
    # verif matrice carre 
    np.size(arrayRes) == len(originalSequence)
    if np.size(arrayRes) != len(originalSequence) :
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
        indexArray.append(len(originalSequence) - i[1])
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

    if compression == False :   
        # TEMPORARY PRINT, NEED TO WRITE IN FILE
        header = "0 0 0 " + str(f)
        #write in file outfile
        outfile = open(outfile, 'w')
        outfile.write(header)
        outfile.write("\n")
        outfile.write(indexes)
        outfile.writelines(res)


    if compression == True :
        # adaptation pour compression
        # suppression du & de la string
        res = res.split('$')
        sepPos = len(res[0])
        res = res[0] + res[1]
        addedA = 0

        while len(res) % 4 != 0 :
            res += "A"
            addedA += 1
            if addedA >= 4 :
                # error case
                raise Exception("ERROR : too much added A, error in sequence string")
        
        # temporary print ---> move to file
        # WARN : cast text to hexa numbers
        header = "1 " + str(sepPos) + " " + str(addedA) + " " + str(f) + "\n"

        # CAST
        binRes = []
        for value in res :
            if value == 'A' :
                binRes.append('00')
            elif value == 'C' :
                binRes.append('01')
            elif value == 'G' :
                binRes.append('10')
            elif value == 'T' :
                binRes.append('11')
        
        res = ""
        for value in binRes :
            res += value[::-1]

        j = 0
        binRes = []
        while j <= len(res) - 8 :
            value = res[j:j+8]
            binRes.append(int(value[::-1], 2))
            j += 8

        outfile = open(outfile, 'wb')
        outfile.write(header.encode())
        outfile.write(indexes.encode())
        count = 0
        #for j in binRes :
        #    res = j.to_bytes(1, "big")
        #    outfile.write(res)
        outfile.write(bytes(binRes))
        outfile.close()

# ----------- MAIN FUNCTION ----------- 
if __name__ == "__main__" :
    compression = False
    argv = sys.argv

    options = []
    input = []

    #argc/argv parser
    for arg in argv :
        if "bw-build.py" in arg :
            continue
        elif "--" in arg :
            options.append(arg)
        else :
            input.append(arg)

    # global options params
    if "--compress" in options :
        compression = True
    
    if (len(input)) < 3 :
        raise Exception("ERROR : default case, please add arguments : \n \t infile, outflie and f argument")

    if debug == True :
        print("options : ", options)
        print('input : ', input)

    main(infile=input[0], outfile=input[1], f=input[2])
