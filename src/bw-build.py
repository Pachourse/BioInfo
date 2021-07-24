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
    #   .idxc -> compressé
    #   .idx -> non compressé

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

    # ajout $ au début de la sequence
    originalSequence = "$" + originalSequence

    if compression == False :

        # read sequence form file (line 2 to end)
        # add $ at start
        arrayRes = []

        sequence = originalSequence
        for j in originalSequence : 
            arrayRes.append(sequence)
            sequence = sequence[-1] + sequence
            sequence = sequence[:-1]
        
        # verif matrice carré 
        np.size(arrayRes) == len(originalSequence)
        if np.size(arrayRes) != len(originalSequence) :
            raise Exception("ERROR : la matrice n'est pas carrée")

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
        
        # TEMPORARY PRINT, NEED TO WRITE IN FILE
        header = "0 0 0 " + str(f)

        indexes = ""
        i = 0
        for elt in indexArray :
            if i != 0 :
                indexes += ','
            i += 1
            indexes += str(elt)
        
        #write in file outfile
        outfile = open(outfile, 'w')
        outfile.writelines(header)
        outfile.writelines("\n")
        outfile.writelines(indexes)
        outfile.writelines("\n")
        outfile.writelines(res)
        outfile.close()

    if compression == True :
        print("WARNING : il faut implémenter la compression")


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