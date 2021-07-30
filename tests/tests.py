#!/usr/bin/env python3
import unittest
import subprocess
import os

dataPath = "../data/"
bwBuild = "src/bw-build.py"
bwSearch = "src/bw-search.py"
def createLineSimple(fastaFile, f, compress=False) :
    data = dataPath + fastaFile
    cmdString = "python3 " + bwBuild + " " + data + " " + "test" + fastaFile + ".idx"
    if compress == True :
        cmdString += "c --compress"
    cmdString += " " + str(f)
    res = os.system(cmdString)
    if compress == False :
        res = os.system("diff " + "../data/" + fastaFile + ".idx" + " " + "test" + fastaFile + ".idx")
        os.system("rm test" + fastaFile + ".idx")
        if res == 0 :
            return True
    else :
        os.system("python3 tests/check_compressed_sequence.py ../data/" + fastaFile + ".idxc > res1.txt")
        os.system("python3 tests/check_compressed_sequence.py test" + fastaFile + ".idxc > res2.txt")
        res = os.system("diff res1.txt res2.txt")
        os.system("rm res1.txt")
        os.system("rm res2.txt")
        os.system("rm test" + fastaFile + ".idxc")
        if res == 0 :
            return True
    return False


class TestPartOne(unittest.TestCase):
    # PART 1 : cmv files
    def test01a(self):
        res = createLineSimple(fastaFile="cmv.fasta", f=6)
        self.assertEqual(res, True)

    def test01b(self):
        res = createLineSimple(fastaFile="cmv.fasta", f=5, compress=True)
        self.assertEqual(res, True)

    def test02a(self):
        res = createLineSimple(fastaFile="calreticulin.fasta", f=15)
        self.assertEqual(res, True)

    def test02b(self):
        res = createLineSimple(fastaFile="calreticulin.fasta", f=15, compress=True)
        self.assertEqual(res, True)

    def test03a(self):
        print("TEST 03A")
        res = createLineSimple(fastaFile="gfp.fasta", f=1)
        self.assertEqual(res, True)

    def test03b(self):
        print("TEST 03B")
        res = createLineSimple(fastaFile="gfp.fasta", f=33, compress=True)
        self.assertEqual(res, True)
    
    # def test05a(self):
    #     res = createLineSimple(fastaFile="rtn4.fasta.idx", f=72, compress=True)
    #     self.assertEqual(res, True)
    
    def test06a(self):
        res = createLineSimple(fastaFile="gfp.fasta", f=18, compress=True)
        self.assertEqual(res, True)


def checkSecondPart(fastaFile, sequence,  onlyCount=False) :
    compressedFile = dataPath + fastaFile + ".idxc"
    uncompressedFile = dataPath + fastaFile + ".idx"
    if onlyCount == False :
        cmdString = "python3 " + bwSearch + " " + compressedFile + " " + sequence + " " + " > compressedRes "
        os.system(cmdString)
        cmdString = "python3 " + bwSearch + " " + uncompressedFile + " " + sequence + " " + " > uncompressedRes "
        os.system(cmdString)
        res = os.system("diff compressedRes uncompressedRes")
        os.system("rm compressedRes")
        os.system("rm uncompressedRes")
        if res == 0 :
            return True
        else :
            return False
    else :
        cmdString = "python3 " + bwSearch + " " + compressedFile + " " + sequence + " " + " --count-only " 
        outputa = subprocess.check_output(cmdString, shell=True)
        outputa = outputa.decode('ascii').rstrip()
        cmdString = "python3 " + bwSearch + " " + uncompressedFile + " " + sequence + " " + " --count-only "
        outputb = subprocess.check_output(cmdString, shell=True)
        outputb = outputb.decode('ascii').rstrip()
        if outputa == outputb :
            print(outputa)
            return int(outputa)
        return False

class TestPartTwo(unittest.TestCase):
    # PART 2 : cmv files
    def test11a(self):
        res = checkSecondPart(fastaFile="cmv.fasta", sequence="ATT")
        self.assertEqual(res, True)

    def test11b(self):
        res = checkSecondPart(fastaFile="cmv.fasta", sequence="ATT", onlyCount=True)
        self.assertEqual(res, 4)

    # PART 2 : cmv files
    def test12a(self):
        res = checkSecondPart(fastaFile="cmv.fasta", sequence="TGTGTGAT")
        self.assertEqual(res, True)

    def test12b(self):
        res = checkSecondPart(fastaFile="cmv.fasta", sequence="TGTGTGAT", onlyCount=True)
        self.assertEqual(res, 0)

if __name__ == '__main__':
    unittest.main()
