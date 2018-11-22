# first create some data
import pandas as pd
import numpy  as np
import random 

n_event = 1000

#mean = 0.5
#stdd = 0.5
#gs   = random.gauss
#gs(mean,stdd)

uni = np.random.uniform

# create the dataframe and fill it with some random stuff
df1           = pd.DataFrame()
df1['prob']   = uni(0,1,n_event) 
df1['weight'] = 0.01 

df2           = pd.DataFrame()
df2['prob']   = uni(0,1,n_event) 
df2['weight'] = 0.5

print df2[:8]
# create list of tuples from the dataframe
tuple_list1 = list(df1.itertuples(index=False))
tuple_list2 = list(df2.itertuples(index=False))

# create the demanding recarray with field structure
array1 = np.array(tuple_list1, dtype=[('prob', float), ('weight', float)]) 
array2 = np.array(tuple_list2, dtype=[('prob', float), ('weight', float)])
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

# Or write directly into a ROOT file without using PyROOT
# this line is not necessary for this task (leave it here for completeness)
#array2root(array1, 'f3.root', 'tree44')
