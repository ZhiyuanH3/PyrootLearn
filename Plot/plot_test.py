#!/bin/env python

#SBATCH --partition=all
#SBATCH --job-name=mtp
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH -c 70
#SBATCH --output /home/hezhiyua/logs/mtp-%j.out
#SBATCH --error  /home/hezhiyua/logs/mtp-%j.err
#SBATCH --mail-type END
#SBATCH --mail-user zhiyuan.he@desy.de




import root_numpy as rnp
import pandas     as pd

import numpy as np
from   numpy import (array, dot, arccos, arcsin)
from   numpy.linalg import norm
import matplotlib.pyplot as plt
import scipy.interpolate
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
import ROOT
from   ROOT import TFile, TLorentzVector, TTree
from   array import array
import sys
from time import time as tm

import multiprocessing as mp


def periodic(phi, eta, e):
    X=[]
    Y=[]
    Z=[]
    eta_max=2.5
    phi_scale=-np.pi #minus to invert axis
    eta_scale=abs(phi_scale) 
    for i in range(0,len(phi)):
      if (np.abs(eta[i]) < eta_scale):
          Y.append(phi[i]/phi_scale)
          X.append(eta[i]/eta_scale)
          Z.append(e[i])
          Y.append((phi[i]+2.*np.pi)/phi_scale) #??
          X.append(eta[i]/eta_scale)
          Z.append(e[i])
          Y.append((phi[i]-2.*np.pi)/phi_scale) #?
          X.append(eta[i]/eta_scale)
          Z.append(e[i])
    xil, yil = np.linspace(-1, 1, 1*Npix), np.linspace(-3, 3, 3*Npix)
    rbf = scipy.interpolate.Rbf(X, Y, Z, function='linear')
    xi, yi = np.meshgrid(xil, yil)
    zi =  rbf(xi,yi)
    zi[zi < 0]= 0.
    zi[np.abs(xi) > eta_max/eta_scale]= 0.
    return xi, yi, zi





def periodic_v(row):
    e   = row['e']
    phi = row['phi'] 
    eta = row['eta']  

    eta_max=2.5
    phi_scale=-np.pi #minus to invert axis
    eta_scale=abs(phi_scale)
    # vectorization
    dfin        = pd.DataFrame()
    dfin['e']   = np.array(e)
    dfin['phi'] = np.array(phi)
    dfin['eta'] = np.array(eta)
    dfin['abs_eta'] = dfin['eta'].apply(np.abs)
    dfin        = dfin[ dfin['abs_eta'] < eta_scale ]
    
    dfout1       = pd.DataFrame()
    dfout2       = pd.DataFrame()
    dfout3       = pd.DataFrame()

    dfout1['X']  = dfin['eta'].apply(lambda x: x/float(eta_scale))
    dfout1['Y']  = dfin['phi'].apply(lambda x: x/float(phi_scale))
    dfout1['Z']  = dfin['e']#.apply(lambda x: x/float(eta_scale))

    dfout2['X']  = dfin['eta'].apply(lambda x: x/float(eta_scale))
    dfout2['Y']  = dfin['phi'].apply(lambda x: (x+2.*np.pi)/float(phi_scale))
    dfout2['Z']  = dfin['e']#.apply(lambda x: x/float(eta_scale))

    dfout3['X']  = dfin['eta'].apply(lambda x: x/float(eta_scale))
    dfout3['Y']  = dfin['phi'].apply(lambda x: (x-2.*np.pi)/float(phi_scale))
    dfout3['Z']  = dfin['e']#.apply(lambda x: x/float(eta_scale))

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Need to find a way to merge these dataframes!!!!!!!!

    #X=[]
    #Y=[]
    #Z=[]
    #~~~~~~~~~~~~~debug:
    X=[1,2]
    Y=[7,3]
    Z=[6,9]

    """
    for i in range(0,len(phi)):
      if (np.abs(eta[i]) < eta_scale):
          Y.append(phi[i]/phi_scale)
          X.append(eta[i]/eta_scale)
          Z.append(e[i])
          Y.append((phi[i]+2.*np.pi)/phi_scale) #??
          X.append(eta[i]/eta_scale)
          Z.append(e[i])
          Y.append((phi[i]-2.*np.pi)/phi_scale) #?
          X.append(eta[i]/eta_scale)
          Z.append(e[i])
    """
    xil, yil = np.linspace(-1, 1, 1*Npix), np.linspace(-3, 3, 3*Npix)
    rbf = scipy.interpolate.Rbf(X, Y, Z, function='linear')
    xi, yi = np.meshgrid(xil, yil)
    zi =  rbf(xi,yi)
    zi[zi < 0]= 0.
    zi[np.abs(xi) > eta_max/eta_scale]= 0.

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Need to find a way to fetch these high dim arrays!!!!!!!!!    

    return 1, 2, 3#xi#, yi, zi









nnn    = 40#2
Npix   = int(nnn) 
imgpix = int(nnn)

path    = '/beegfs/desy/user/hezhiyua/backed/dustData/crab_folder_v2/'
pathOut = '/beegfs/desy/user/hezhiyua/backed/dustData/crab_folder_v2/test/'
Fname   = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC.root'


entries = 200



fin   = TFile(path + Fname)
tin   = fin.Get('ntuple/tree')


tm1 = tm()
s_cut = 1000#None#100
arr_energy   = rnp.tree2array(tin, ['PFCandidates.energy'], stop=s_cut)
arr_phi      = rnp.tree2array(tin, ['PFCandidates.phi'], stop=s_cut)
arr_eta      = rnp.tree2array(tin, ['PFCandidates.eta'], stop=s_cut)
arr_jetindex = rnp.tree2array(tin, ['PFCandidates.jetIndex'], stop=s_cut)

#e_npar = np.array(arr_energy)
e_df     = pd.DataFrame(arr_energy) 
phi_df   = pd.DataFrame(arr_phi)
eta_df   = pd.DataFrame(arr_eta)

#print e_npar
#print arr_energy[3]
print e_df.loc[3,'PFCandidates.energy'][3]
df        = pd.DataFrame()
df_o      = pd.DataFrame()
df['e']   = e_df
df['phi'] = phi_df
df['eta'] = eta_df
df['bool'] = df['e'].apply(len) != 0
df = df[ df['bool'] ]
#df['x']   = np.vectorize(periodic)(df['phi'],df['eta'],df['e'])
df['x'], df['y'], df['z'] = zip( *df.apply(periodic_v, axis=1) )
#df['x'] = df.apply(periodic_v, axis=1) 




tm2 = tm()
print str(tm2 - tm1)+'sec'

exit()














def worker(jentry):
    fin   = TFile(path + Fname)
    tin   = fin.Get('ntuple/tree')
    b1    = tin.GetBranch('PFCandidates')

    phi = []
    eta = []
    e   = []
    ientry = tin.GetEntry(jentry)
    b1.GetEntry(jentry)

    energy1   = b1.FindBranch('PFCandidates.energy')
    phi1      = b1.FindBranch('PFCandidates.phi')
    eta1      = b1.FindBranch('PFCandidates.eta')
    jetindex1 = b1.FindBranch('PFCandidates.jetIndex')

    n_depth = 100
    for num in range(0,n_depth): 
        if energy1.GetValue(num,1) == 0.: continue
        if eta1.GetValue(num,1) == 0.: continue
        if phi1.GetValue(num,1) == 0.: continue
        phi.append(phi1.GetValue(num,1))
        eta.append(eta1.GetValue(num,1))
        e.append(energy1.GetValue(num,1))
    if len(e) == 0: return#continue
    
    xi, yi, zi = periodic(phi, eta, e)
    #q.put(np.max(e))
    return np.max(e)






L={}
def split_job(n_task, L, n_cpu=12):
    sub_range = int(n_task/float(n_cpu))
    res       = n_task - sub_range*n_cpu
    for i in range(n_cpu):
        L[i]            = {}
        L[i]['result']  = []
        if i == n_cpu - res:
            cut_i = i   
            cut = cut_i * sub_range 
        if i >= n_cpu - res:    L[i]['range']  = range(cut + (i-cut_i)*(1+sub_range), cut + (i-cut_i+1)*(1+sub_range)) 
        else               :    L[i]['range']  = range(i*sub_range, (i+1)*sub_range) 


def sub_loop(func, return_dict, ind, sub_range):
    tmp_list = []
    for jj in sub_range:
        tmp_list.append( func(jj) )  
    return_dict[ind] = tmp_list


"""
q=mp.Queue()

n_cpus = 12
record = []
split_job(100, L, n_cpus)

for j in xrange(n_cpus):
    process = mp.Process(target=sub_loop, args=(worker, L[j]['result'], L[j]['range'])  )
    process.start()
    record.append(process)
for p in record:
    p.join()
LL=[]
while not q.empty():
    LL.append(q.get())
"""
#pool = mp.Pool(12)
#pool.map(worker,range(10))

#"""
tm1 = tm()
n_cpus = 12#20#70#12
split_job(entries, L, n_cpus)
out_list = []
with mp.Manager() as manager:
    Dict = manager.dict()
    processes = []
    for i in range(n_cpus): 
        process = mp.Process(target=sub_loop, args=(worker, Dict, i, L[i]['range'])  )
        process.start()
        processes.append(process)
    """
    for p in processes:
        slp(0.4)
        p.is_alive()
    """
    for p in processes:
        p.join()
    for i in Dict.values():
        out_list += i
print out_list
tm2 = tm()
print str(tm2 - tm1)+'sec'
#"""

"""
tm1 = tm()
n_cpus = 12
split_job(100, L, n_cpus)
dd = {}
print L
for i in range(n_cpus): 
    sub_loop(worker, dd, i, L[i]['range'])
print dd
tm2 = tm()
print str(tm2 - tm1)+'sec' 
"""

#"""
tm1 = tm()
LLL=[]
for i in xrange(entries):
    LLL.append( worker(i) )
print LLL
tm2 = tm()
print str(tm2 - tm1)+'sec'
#"""



print LLL == out_list






