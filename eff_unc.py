# first create some data
import pandas as pd
import numpy  as np
import random 
from   sklearn.externals   import joblib

n_scan  = 100#1000
n_bins  = 250#126#1000
bin_i   = 0
bin_f   = 1
pth     = '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/'

load_s = joblib.load(pth+'/dumps/s.pkl')
load_b = joblib.load(pth+'/dumps/b.pkl')
#print load_s

from ROOT import TGraphAsymmErrors as GAE
from ROOT import TH1F, TChain
from time import sleep as slp

# if you want to use the GetCumulative() of a histogram and set its error: do not call the Sumw2() of it
h_after_selection  = TH1F('h_after_selection' , 'hist_after_selection' , n_bins, bin_i, bin_f)
#h_after_selection.Sumw2()
h_before_selection = TH1F('h_before_selection', 'hist_before_selection', n_bins, bin_i, bin_f)
#h_before_selection.Sumw2()

h_true_positive    = TH1F('h_true_positive' , 'True_Positives' , n_bins, bin_i, bin_f)
h_true             = TH1F('h_true'          , 'Trues'          , n_bins, bin_i, bin_f)
# see if reversing the bin_min and bin_max will cause the histogram axis to reverse(__no!)
#h_true          = TH1F('h_true'          ,'Trues'          , n_bins, bin_f, bin_i)


print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>filling histogram...'
#cc           = 0
tot_weight_s = 0
for index, row in load_s.iterrows():
    tot_weight_s += row['weight']
    #if cc == n_scan: break
    h_true_positive.Fill(row['signal'], row['weight'])
    #cc += 1

# cc is just there for testing purposes 
cc           = 0
tot_weight_b = 0
for index, row in load_b.iterrows():
    tot_weight_b += row['weight']
    if cc == n_scan: break
    h_after_selection.Fill(row['signal'], row['weight'])
    cc += 1

#h_after_selection.Draw('HIST')
#h_true_positive.Draw()
#slp(44)


print 'Total weights b: ', tot_weight_b
print 'Total weights s: ', tot_weight_s
for i in range(n_bins):
    h_before_selection.SetBinContent(i+1, tot_weight_b) 
    h_true.SetBinContent(i+1, tot_weight_s)

#h_before_selection.Draw()
#slp(3)

# this part should have been the best way, but we need the 'reverse' version of the cumulation
#############################################################
"""
h_after_selection_cum  = h_after_selection.GetCumulative()
h_after_selection_cum.Sumw2()
h_true_positive_cum    = h_true_positive.GetCumulative()
h_true_positive_cum.Sumw2()
"""
#############################################################
#h_after_selection_cum.Draw('HIST')
#h_true_positive_cum.Draw()
#slp(44)




#xaxis     = h_after_selection_cum.GetXaxis()
#binCenter = xaxis.GetBinCenter(1) 
#print binCenter

h_c_b = TH1F('h_c_b' , 'hist_after_selection_cum_rev' , n_bins, bin_i, bin_f)
h_c_b.Sumw2()

h_c_s = TH1F('h_c_s' , 'hist_true_positives_cum_rev' , n_bins, bin_i, bin_f)
h_c_s.Sumw2()

#xaxis     = h_before_selection.GetXaxis()
#xaxis     = h_c_b.GetXaxis()
#binCenter = xaxis.GetBinCenter(1)
#print binCenter

cum = 0
for j in range(n_bins):
    bin_cont_j = h_after_selection.GetBinContent(j+1)
    cum       += bin_cont_j
    bin_cont   = tot_weight_b - cum
    h_c_b.SetBinContent(j+1, bin_cont)

cum = 0
for j in range(n_bins):
    bin_cont_j = h_true_positive.GetBinContent(j+1)
    cum       += bin_cont_j
    bin_cont   = tot_weight_s - cum
    h_c_s.SetBinContent(j+1, bin_cont)






g_efficiency = GAE()
g_tpr        = GAE()

g_efficiency.Divide(h_c_b, h_before_selection, "cl=0.683 b(1,1) mode")
#g_efficiency.Divide(h_after_selection_cum, h_before_selection, "cl=0.683 b(1,1) mode")
g_tpr.Divide(h_c_s, h_true, "cl=0.683 b(1,1) mode")


g_efficiency.SetTitle('efficiency')
g_efficiency.SetFillColor(5)
g_efficiency.SetMarkerStyle(21)
g_efficiency.SetMarkerColor(4)
#g_efficiency.Draw('ALP')
#g_efficiency.Draw('3A')a
#slp(33)

g_tpr.SetTitle('True Positive Rate')
g_tpr.SetFillColor(5)
g_tpr.SetMarkerStyle(21)
g_tpr.SetMarkerColor(4)
#g_tpr.Draw('ALP')
#g_tpr.Draw('3A')a
#slp(33)





from ROOT import Double

g_size   = g_efficiency.GetN()
g_size_s = g_tpr.GetN()


x  = Double()
y  = Double()


x_s  = Double()
y_s  = Double()

arr_x = np.zeros(g_size)
arr_y = np.zeros(g_size)

arr_x_s = np.zeros(g_size_s)
arr_y_s = np.zeros(g_size_s)

for i in range( g_size ):
    g_efficiency.GetPoint(i,x,y)
    arr_x[i] = x 
    arr_y[i] = y
#print arr_y

for i in range( g_size_s ):
    g_tpr.GetPoint(i,x_s,y_s)
    arr_x_s[i] = x_s 
    arr_y_s[i] = y_s

# GetEYhigh() work as the following 3 ways(presumably the 'copy' version works most consistently):
#----------------------------------------------V1
#buffer_l = g_efficiency.GetEYlow()
#arr_l    = np.ndarray(g_size, 'd', buffer_l)
#----------------------------------------------V2
#buffer_h   = g_efficiency.GetEYhigh()
#arr_h      = np.frombuffer(buffer_h, count=g_size)
#----------------------------------------------V3
buffer_l   = g_efficiency.GetEYlow()
buffer_l.SetSize(g_size)
arr_l      = np.array(buffer_l, copy=True)

buffer_h   = g_efficiency.GetEYhigh()
buffer_h.SetSize(g_size)
arr_h      = np.array(buffer_h, copy=True)
#print len(arr_h)
#print len(arr_l)


buffer_l_s   = g_tpr.GetEYlow()
buffer_l_s.SetSize(g_size_s)
arr_l_s      = np.array(buffer_l_s, copy=True)

buffer_h_s   = g_tpr.GetEYhigh()
buffer_h_s.SetSize(g_size_s)
arr_h_s      = np.array(buffer_h_s, copy=True)
print len(arr_h)
print len(arr_l)















from ROOT import TCanvas
from ROOT import TVectorT
from array import array

c1 = TCanvas('c1', 'Graph with asymmetric error bars', 200, 10, 700, 500)
c1.SetFillColor(42) 
c1.SetGrid() 
c1.GetFrame().SetFillColor(21) 
c1.GetFrame().SetBorderSize(12) 
n = 10 

"""
x=TVectorT('double')
y=TVectorT('double')
exl=TVectorT('double')
eyl=TVectorT('double')
exh=TVectorT('double')
eyh=TVectorT('double')
"""

x=array('d')
y=array('d')
exl=array('d')
eyl=array('d')
exh=array('d')
eyh=array('d')

x.append(0.1)
y.append(0.1)
exl.append(0.1)
eyl.append(0.1)
exh.append(0.1)
eyh.append(0.1)

"""
x   = np.array([-0.22, 0.05, 0.25, 0.35, 0.5, 0.61,0.7,0.85,0.89,0.95] )
y   = np.array([1,2.9,5.6,7.4,9,9.6,8.7,6.3,4.5,1] )
exl = np.array([.05,.1,.07,.07,.04,.05,.06,.07,.08,.05] )
eyl = np.array([.8,.7,.6,.5,.4,.4,.5,.6,.7,.8] )
exh = np.array([.02,.08,.05,.05,.03,.03,.04,.05,.06,.03] )
eyh = np.array([.6,.5,.4,.3,.2,.2,.3,.4,.5,.6] )
"""

"""
x   = [-0.22, 0.05, 0.25, 0.35, 0.5, 0.61,0.7,0.85,0.89,0.95] 
y   = [1,2.9,5.6,7.4,9,9.6,8.7,6.3,4.5,1] 
exl = [.05,.1,.07,.07,.04,.05,.06,.07,.08,.05] 
eyl = [.8,.7,.6,.5,.4,.4,.5,.6,.7,.8] 
exh = [.02,.08,.05,.05,.03,.03,.04,.05,.06,.03] 
eyh = [.6,.5,.4,.3,.2,.2,.3,.4,.5,.6] 
"""

gr           = GAE(x,y,exl,exh,eyl,eyh) 
gr.SetTitle('TGraphAsymmErrors') 
gr.SetMarkerColor(4) 
gr.SetMarkerStyle(21) 
gr.Draw("ALP")








 
