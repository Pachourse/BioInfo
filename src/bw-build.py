import sys

def main(infile, outfile, f, compression) :
    print(infile, outfile, f, compression)
    return 1


if __name__ == "__main__" :
    argv = sys.argv
    print(len(argv))
    if len(argv) == 2 and argv[1] == "--h" :
        print("this is help menu")
    elif len(argv) == 5 :
        if argv[4] == "--compression" :
            print("A")
            main(infile=argv[1], outfile=argv[2], f=argv[3], compression=True)
        else :
            main(infile=argv[1], outfile=argv[2], f=argv[3], compression=False)
    elif len(argv) == 4 :
        main(infile=argv[1], outfile=argv[2], f=argv[3], compression=False)
    else : 
        print("Please : add argv arguments")