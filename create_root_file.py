from ROOT  import TFile, TTree
from array import array
import            random as rd

############
# version1 #
############
f1 = TFile('f1.root','recreate') # 'new'
t1 = TTree('tree44','tree_title')

aLength        = 1
num_of_entries = 10000

# define the array to store variables of the events
v0 = array('f',[0])
v1 = array('f',[0])
#ab2 = array('f',[0]*aLength)

# before you fill the tree, the location and structure of the branch from the tree should be specified
b0 = t1.Branch('variable0',v0,'v0[1]/F')
b1 = t1.Branch('variable1',v1,'v1[1]/F')
#b2 = t1.Branch('branch2',ab2,'ab1[10]/F')

# The filling process: one event at a time
for i in range(num_of_entries):
    v1[0] = i*3
    v0[0] = rd.gauss(1,2)
    #ab2[i] = i*i
    t1.Fill()

f1.Write()
f1.Close()


############
# version2 #
############
from ROOT import gROOT
# specify the structure of the leaf at the beginning: this could be write in a separate file
gROOT.ProcessLine('struct testStruct {Int_t v2; Int_t v3;};');
# import the structure we just defined
from ROOT import testStruct
# instantiate the structure we defined 
tS = testStruct()

f2 = TFile('f2.root','recreate') # new
t2 = TTree('tree44','tree_title')

#v2 = array('f',[0])
#v3 = array('f',[0])

#b2 = t2.Branch('branch2',v2,'v2[1]/F')
#b3 = t2.Branch('branch3',v3,'v3[1]/F')

# the string at the end of the line should exactly match the structure of the object
t2.Branch('branch_name', tS, 'v2/I:v3/I' )

for i in range(num_of_entries):
    #v2[0] = i*2
    #v3[0] = i*3
    # bring out the leaf as feature of the object
    tS.v2 = int(i*2) 
    # remember to match the type of the variable to the structure string you defined(I means integer) 
    tS.v3 = int( rd.gauss(3,4) ) #int(i*3)

    t2.Fill()

f2.Write()
f2.Close()


