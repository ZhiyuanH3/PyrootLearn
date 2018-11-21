# first create some data
import pandas as pd
import numpy  as np




#you need the 'root_numpy' package installed 
from root_numpy import array2tree, array2root

# the following few lines can be found in the documentation of root_numpy
# Rename the fields
array.dtype.names = ('x', 'y', 'sqrt_y', 'landau_x', 'cos_x_sin_y')

# Convert the NumPy array into a TTree
tree = array2tree(array, name='tree')

# Or write directly into a ROOT file without using PyROOT
# this line is not necessary for this task (leave it here for completeness)
#array2root(array, 'selected_tree.root', 'tree')
