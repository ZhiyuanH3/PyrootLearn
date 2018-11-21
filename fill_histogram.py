from ROOT import TFile, TTree, TChain, TH1F
import time

# specify the tree/tuple name of interest
c1  = TChain('treename')
c2  = TChain('tree44')

# add root file to the chain
# after defining(by adding trees to it) the tchain behaves like a ttree object(Draw() can be used etc.)
c1.Add('f1.root')
c2.Add('f2.root')

# histogram with 100 bins x axis runs from -10 to 10
h1  = TH1F('h1', 'Title of the h1', 100, -10, 10)

# set uncertainty of the histogram
# this should be done right after the histogram has been defined
h1.Sumw2()

# specify in the first entry what variable you want to plot(in our case: leaf0)
# by '>>' we tell the tchain to project the tree to the histogram 
# the last entry specifies the weight of the events from this variable
c1.Draw('leaf0 >> h1','0.2')

# pause the program to be able to see the plot
#time.sleep(3)
#c2.Draw('l3    >> h1','0.4')
#time.sleep(3)

c2.Draw('l3    >> +h1','0.4')
time.sleep(20)




