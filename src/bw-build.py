import sys

debug = False

#global params
compression = False

def main(infile, outfile, f) :
    if debug == True :
        print("compression : ", compression)
        print(infile, outfile, f)
    return 0


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
    if "--compression" in options :
        compression = True
    
    if (len(input)) < 3 :
        raise Exception("ERROR : default case, please add arguments : \n \t infile, outflie and f argument")

    if debug == True :
        print("options : ", options)
        print('input : ', input)

    main(infile=input[0], outfile=input[1], f=input[2])