from ROOT import TFile, TTree

# The following name of the methods are pretty much self explanatory~

f1 = TFile('f2.root','read')

t1 = f1.Get('tree44')
#b2 = t1.GetBranch('branch')
#b3 = t1.GetBranch('branch')
bb = t1.GetBranch('branch_name')

#l2 = b2.GetLeaf('v2')
#l3 = b3.GetLeaf('v3')

ll  = bb.GetLeaf('v2')
lll = bb.GetLeaf('v3')

# showing that the three branches share the same number of entries
N   = t1.GetEntriesFast()
print N
#print b2.GetEntries()
#print b3.GetEntries()

for i in range(10):
    # before getting the value of a specific branch, the following function must be called to point to the right entry/event
    #b2.GetEntry(i)
    #b3.GetEntry(i)
    bb.GetEntry(i)
    #print l2.GetValue()
    #print l3.GetValue()
    print ll.GetValue()
    print lll.GetValue()
   
    


