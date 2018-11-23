# first create some data
import pandas as pd
import numpy  as np
import random 

n_event = 1000

# create the dataframe and fill it with some random stuff
df1           = pd.DataFrame()
df1['n']      = np.array([1,2,2,3,3,3,4,4,4,4])
df1['weight'] = 0.1 

df2           = pd.DataFrame()
df2['n']      = np.array([1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4])
df2['weight'] = 0.5

df3           = pd.DataFrame()
df3['n']      = np.array([1,1,1,2,2,3,3,3,4])
df3['weight'] = 0.2


print df1[:8]
print df2[:8]
# create list of tuples from the dataframe
tuple_list1 = list(df1.itertuples(index=False))
tuple_list2 = list(df2.itertuples(index=False))
tuple_list3 = list(df3.itertuples(index=False))

# create the demanding recarray with field structure
array1 = np.array(tuple_list1, dtype=[('n', float), ('weight', float)]) 
array2 = np.array(tuple_list2, dtype=[('n', float), ('weight', float)])
array3 = np.array(tuple_list3, dtype=[('n', float), ('weight', float)])
#print array2


#you need the 'root_numpy' package installed 
from root_numpy import array2tree, array2root

# the following few lines can be found in the documentation of root_numpy
# Rename the fields

#array1.dtype.names = ('prob', 'weight')
#array2.dtype.names = ('prob', 'weight')

# Convert the NumPy array into a TTree
tree1 = array2tree(array1, name='tree44')
tree2 = array2tree(array2, name='tree44')
tree3 = array2tree(array3, name='tree44')
# Or write directly into a ROOT file without using PyROOT
array2root(array1, 'eff1.root', 'tree44')
array2root(array3, 'eff2.root', 'tree44')







from ROOT import TGraphAsymmErrors as GAE
from ROOT import TH1F, TChain
import time

#tree1.Draw('n')
#time.sleep(4)
#tree2.Draw('n')
#time.sleep(4)

#h_after_selection  = TH1F('h_after_selection','h_after_selection',100,0,1)
h_after_selection  = TH1F('h_after_selection','h after selection',4,1,5)
#h_after_selection.Sumw2()
#h_before_selection = TH1F('h before selection','h before selection',100,0,1)
h_before_selection = TH1F('h_before_selection','h before selection',4,1,5)
#h_before_selection.Sumw2()

#print tree1.GetWeight()
tree1.SetWeight(0.9)
tree3.SetWeight(0.1)
tree2.SetWeight(1.0)
#print tree1.GetWeight()

"""
c1 = TChain('tree44')
c1.Add('eff1.root')
c1.Add('eff2.root')
print c1.GetWeight()
c1.Project('h_after_selection','n')
"""

tree1.Project('h_after_selection' , 'n')
tree3.Project('h_after_selection' , 'n')
tree2.Project('h_before_selection', 'n')

#h_after_selection.Scale()

#h_after_selection.Draw()
#time.sleep(4)

h_after_selection_cum  = h_after_selection.GetCumulative()
h_after_selection_cum.Sumw2()
h_after_selection_cum.Draw()
time.sleep(11)


"""
h_efficiency = h_after_selection
h_efficiency.Divide(h_after_selection,h_before_selection,1.0,1.0,"B")
#h_efficiency = h_before_selection
#h_efficiency.Divide(h_before_selection,h_after_selection,1.0,1.0,"B")
h_efficiency.Draw()
time.sleep(11)
"""



g_efficiency = GAE()
g_efficiency.Divide(h_after_selection_cum, h_before_selection, "cl=0.683 b(1,1) mode")

#from tools import DrawErrorBand
#DrawErrorBand(g_efficiency)

#"""
g_efficiency.SetTitle('efficiency')
g_efficiency.SetFillColor(5)

g_efficiency.SetMarkerStyle(21)
g_efficiency.SetMarkerColor(4)

#g_efficiency.Draw('ALP')
#g_efficiency.Draw('3A')
#"""


time.sleep(111)







