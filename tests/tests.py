import unittest
import os

dataPath = "../data/"
bwBuild = "src/bw-build.py"
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
        res = createLineSimple(fastaFile="gfp.fasta", f=1)
        self.assertEqual(res, True)

    def test03b(self):
        res = createLineSimple(fastaFile="gfp.fasta", f=33, compress=True)
        self.assertEqual(res, True)
    
    def test04a(self):
        res = createLineSimple(fastaFile="gfp.fasta", f=33, compress=True)
        self.assertEqual(res, True)

    def test04b(self):
        res = createLineSimple(fastaFile="gfp.fasta", f=33, compress=True)
        self.assertEqual(res, True)
    
    def test05a(self):
        res = createLineSimple(fastaFile="rtn4.fasta.idx", f=72, compress=True)
        self.assertEqual(res, True)
    
    def test06a(self):
        res = createLineSimple(fastaFile="gfp.fasta", f=18, compress=True)
        self.assertEqual(res, True)

if __name__ == '__main__':
    unittest.main()