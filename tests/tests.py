import unittest
import os

dataPath = "../../data/"
bwBuild = "../src/bw-build.py"
def createLineSimple(fastaFile, compress=False) :
    data = dataPath + fastaFile
    cmdString = "python3 " + bwBuild + " " + data + " " + "test" + fastaFile + ".idx"
    if compress == True :
        cmdString += "c --compress"
    os.system(cmdString)

class TestStringMethods(unittest.TestCase):
    print("TESTS : bv-build.py")
    def test_upper(self):
        #a = os.system('python3 ../src/bw-build.py ../../data/gfp.fasta/')
        #print(a)
        res = createLineSimple(gfp.fasta)
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()