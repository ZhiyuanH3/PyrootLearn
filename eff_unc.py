# first create some data
import pandas as pd
import numpy  as np
import random 
from sklearn.externals   import joblib

n_event = 1000
n_scan  = 1000
n_bins  = 100
bin_i   = 0
bin_f   = 1
pth     = '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/'

#joblib.dump(smallerDF_s   ,pth+'/dumps/s.pkl'  )
#joblib.dump(smallerDF_b   ,pth+'/dumps/b.pkl'  )
#joblib.dump(sortedProbList,pth+'/dumps/spl.pkl')

#uni = np.random.uniform

load_s = joblib.load(pth+'/dumps/s.pkl')
load_b = joblib.load(pth+'/dumps/b.pkl')

print load_s






# create the dataframe and fill it with some random stuff
df1           = pd.DataFrame()
df1['n']      = np.array([1,2,2,3,3,3,4,4,4,4])#np.ones(n_event-500) * n_event#np.random.randint(0,100,n_event)
#df1['prob']   = uni(0,1,n_event) 
df1['weight'] = 0.8

df2           = pd.DataFrame()
df2['n']      = np.array([1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4])#np.ones(n_event) * n_event
#df2['prob']   = uni(0,1,n_event) 
df2['weight'] = 0.5

df3           = pd.DataFrame()
df3['n']      = np.array([1,1,1,1,2,2,2,3,3,4])
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
# this line is kind of not necessary for this task (leave it here for completeness)
array2root(array1, 'eff1.root', 'tree44')
array2root(array3, 'eff2.root', 'tree44')







from ROOT import TGraphAsymmErrors as GAE
from ROOT import TH1F, TChain
import time

#tree1.Draw('n')
#time.sleep(4)
#tree2.Draw('n')
#time.sleep(4)

h_after_selection  = TH1F('h_after_selection','h after selection',n_bins,bin_i,bin_f)
#h_after_selection  = TH1F('h_after_selection','h after selection',4,1,5)
#h_after_selection.Sumw2()
h_before_selection = TH1F('h_before_selection','h before selection',n_bins,bin_i,bin_f)
#h_before_selection = TH1F('h_before_selection','h before selection',4,1,5)
#h_before_selection.Sumw2()

#print tree1.GetWeight()
tree1.SetWeight(0.9)#(df1['weight'])
tree3.SetWeight(0.1)#(df3['weight'])
tree2.SetWeight(1.0)
#print tree1.GetWeight()

"""
c1 = TChain('tree44')
c1.Add('eff1.root')
c1.Add('eff2.root')
print c1.GetWeight()
c1.Project('h_after_selection','n')
"""

#tree1.Project('h_after_selection' , 'n')
#tree3.Project('h_after_selection' , 'n')
#tree2.Project('h_before_selection', 'n')

#h_after_selection.Scale()




"""
#>>>>>>>test:
for i in range( len(df1) ):
    h_after_selection.Fill(df1['n'][i], 0.5)

for i in range( len(df3) ):
    h_after_selection.Fill(df3['n'][i], 0.5)
"""




#for i in range( len(load_s) ):
#    h_after_selection.Fill(load_s['signal'][i], load_s['weight'][i])


print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>filling histogram...'
cc = 0
for index, row in load_b.iterrows():
    if cc == n_scan: break
    h_after_selection.Fill( row['signal'])
    cc += 1

#h_after_selection.Draw()
#time.sleep(4)
bin_width = (bin_f - bin_i) / float(n_bins)
bin_list = [ i*bin_width + bin_i for i in range(n_bins)]
    

for bin_i in bin_list:
    h_before_selection.SetBinContent(bin_i, n_scan)



















h_after_selection_cum  = h_after_selection.GetCumulative()
h_after_selection_cum.Sumw2()
#h_after_selection_cum.Draw()
#time.sleep(11)


"""
h_efficiency = h_after_selection
h_efficiency.Divide(h_after_selection,h_before_selection,1.0,1.0,"B")
#h_efficiency = h_before_selection
#h_efficiency.Divide(h_before_selection,h_after_selection,1.0,1.0,"B")
h_efficiency.Draw()
time.sleep(11)
"""



g_efficiency = GAE()#ROOT.TGraphAsymmErrors()
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







