from ROOT import TFile, TTree

# The following name of the methods are pretty much self explanatory~

f1 = TFile('f2.root','read')

t1 = f1.Get('tree44')
b2 = t1.GetBranch('branch2')
b3 = t1.GetBranch('branch3')
bb = t1.GetBranch('branch')

l2 = b2.GetLeaf('leaf2')
l3 = b3.GetLeaf('leaf3')

ll  = bb.GetLeaf('l2')
lll = bb.GetLeaf('l3')

# showing that the three branches share the same number of entries
N   = t1.GetEntriesFast()
print N
print b2.GetEntries()
print b3.GetEntries()

for i in range(10):
    # before getting the value of a specific branch, the following function must be called to point to the right entry/event
    b2.GetEntry(i)
    b3.GetEntry(i)
    bb.GetEntry(i)
    print l2.GetValue()
    print ll.GetValue()
    print lll.GetValue()
    print l3.GetValue()
    


