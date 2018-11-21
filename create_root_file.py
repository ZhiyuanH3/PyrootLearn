from ROOT  import TFile, TTree
from array import array
import            random as rd

############
# version1 #
############
f1 = TFile('f1.root','recreate') #'new'
t1 = TTree('treename','treetitle')

aLength = 1

#define the array to store the events
leaf0 = array('f',[0])
leaf1 = array('f',[0])
#ab2 = array('f',[0]*aLength)

#before you fill the tree, the location and structure of the branch from the tree should be specified
b0 = t1.Branch('branch0',leaf0,'leaf0[1]/F')
b1 = t1.Branch('branch1',leaf1,'leaf1[1]/F')
#b2 = t1.Branch('branch2',ab2,'ab1[10]/F')

#The filling process: one event at a time
for i in range(10000):
    leaf1[0] = i*3
    leaf0[0] = rd.gauss(1,2)
    #ab2[i] = i*i
    t1.Fill()

f1.Write()
f1.Close()


############
# version2 #
############
from ROOT import gROOT
#specify the structure of the leaf at the beginning: this could be write in a separate file
gROOT.ProcessLine('struct testStruct {Int_t l2; Int_t l3;};');
#import the structure we just defined
from ROOT import testStruct
#instantiate the structure we defined 
tS = testStruct()

f2 = TFile('f2.root','recreate') #new
t2 = TTree('tree44','tree_title')

leaf2 = array('f',[0])
leaf3 = array('f',[0])

b2 = t2.Branch('branch2',leaf2,'leaf2[1]/F')
b3 = t2.Branch('branch3',leaf3,'leaf3[1]/F')

#the string at the end of the line should exactly match the structure of the object
t2.Branch('branch', tS, 'l2/I:l3/I' )

for i in range(10):
    leaf2[0] = i*2
    leaf3[0] = i*3
    #bring out the leaf as feature of the object
    tS.l2 = int(i*2) 
    tS.l3 = int(i*3)

    t2.Fill()

f2.Write()
f2.Close()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~f2

