# first create some data
import pandas as pd
import numpy  as np
import random 
from   sklearn.externals   import joblib
from   time                import sleep as slp
from   time                import time

from ROOT import TGraphAsymmErrors as GAE
from ROOT import TH1F, TChain
from ROOT import TCanvas





n_scan  = 10000000
n_bins  = 1000#250#126#1000
bin_i   = 0
bin_f   = 1
pth     = '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/'

param           = {}
param['n_scan'] = n_scan 
param['n_bins'] = n_bins
param['bin_i']  = bin_i
param['bin_f']  = bin_f
#param['']       =
#param['']       =

#load_s = joblib.load(pth+'/dumps/s.pkl')
#load_b = joblib.load(pth+'/dumps/b.pkl')
#print load_s


bin_width = float(bin_f - bin_i)/n_bins
bin_value_dict = {}
for j in xrange(n_bins):
    bin_value_dict[j] = bin_i + (0.5+j)*bin_width
#print bin_value_dict

"""

# if you want to use the GetCumulative() of a histogram and set its error: do not call the Sumw2() of it
h_after_selection  = TH1F('h_after_selection' , 'hist_after_selection' , n_bins, bin_i, bin_f)
#h_after_selection.Sumw2()
h_before_selection = TH1F('h_before_selection', 'hist_before_selection', n_bins, bin_i, bin_f)
#h_before_selection.Sumw2()

h_true_positive    = TH1F('h_true_positive' , 'True_Positives' , n_bins, bin_i, bin_f)
h_true             = TH1F('h_true'          , 'Trues'          , n_bins, bin_i, bin_f)
# see if reversing the bin_min and bin_max will cause the histogram axis to reverse(no)
#h_true          = TH1F('h_true'          ,'Trues'          , n_bins, bin_f, bin_i)

h_c_b = TH1F('h_c_b' , 'hist_after_selection_cum_rev' , n_bins, bin_i, bin_f)
#h_c_b.Sumw2()
h_c_s = TH1F('h_c_s' , 'hist_true_positives_cum_rev'  , n_bins, bin_i, bin_f)
#h_c_s.Sumw2()



print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>filling histogram...'
zeitA = time()
#cc           = 0
tot_weight_s = 0
for index, row in load_s.iterrows():
    tmp_weight    = row['weight']
    tmp_signal    = row['signal']
    tot_weight_s += tmp_weight#row['weight']
    for k in xrange(n_bins):
        h_true.Fill(bin_value_dict[k], tmp_weight)#row['weight'])
        if bin_value_dict[k] - 0.5*bin_width <= tmp_signal and bin_value_dict[k] + 0.5*bin_width > tmp_signal:
            for kk in xrange(k):
                h_c_s.Fill(bin_value_dict[kk], tmp_weight)
    #if cc == n_scan: break
    #cc += 1

# cc is just there for testing purposes 
cc           = 0
tot_weight_b = 0
for index, row in load_b.iterrows():
    tmp_weight    = row['weight']
    tmp_signal    = row['signal']
    tot_weight_b += tmp_weight#row['weight']
    for k in xrange(n_bins):
        h_before_selection.Fill(bin_value_dict[k], tmp_weight)#row['weight'])
        if bin_value_dict[k] - 0.5*bin_width <= tmp_signal and bin_value_dict[k] + 0.5*bin_width > tmp_signal:
            for kk in xrange(k):
                h_c_b.Fill(bin_value_dict[kk], tmp_weight)  

    if cc == n_scan: break
    cc += 1
zeitB = time()
print 'Time taken for filling histogram(for #events: ' + str(n_scan) + '): ', str(zeitB-zeitA)


"""





import math




"""
#Approch with Fill
h_c_b                 = TH1F('h_c_b' ,'h_c_b', 1, 1, 10)
h_c_b.Sumw2()
h_before_selection    = TH1F('h_before_selection', 'h_before_selection', 1, 1, 10)
h_c_b.Sumw2()

#h_c_b.Fill(2,0.3)
h_c_b.Fill(7,0.7)
h_c_b.Fill(8,0.4)

h_before_selection.Fill(2,0.3)
h_before_selection.Fill(7,0.7)
h_before_selection.Fill(3,0.1)
h_before_selection.Fill(9,0.6)
h_before_selection.Fill(8,0.4)



"""
#Approch with setbincontent
h_c_b                 = TH1F('h_c_b' ,'h_c_b', 1, 1, 10)
#h_c_b.Sumw2()
h_before_selection    = TH1F('h_before_selection', 'h_before_selection', 1, 1, 10)
#h_c_b.Sumw2()

#h_c_b.SetBinContent(1, 0.3)
h_c_b.SetBinContent(1, 0.7+0.4)
#h_c_b.SetBinError(1, math.sqrt(0.3*0.3+0.7*0.7))


h_before_selection.SetBinContent(1, 0.3+0.1+0.7+0.6+0.4)
#h_before_selection.SetBinContent(2, 0.7+0.6+0.3+0.1)
h_before_selection.SetBinError(1, math.sqrt(0.3*0.3+0.7*0.7+0.1*0.1+0.6*0.6+0.4*0.4))
#h_before_selection.SetBinError(2, math.sqrt(0.3*0.3+0.7*0.7+0.1*0.1+0.6*0.6))
#h_before_selection.SetBinError(1, math.sqrt(0.3*0.3+0.7*0.7+0.1*0.1+0.6*0.6))
#"""








g_efficiency = GAE()
#g_tpr        = GAE()

g_efficiency.Divide(h_c_b, h_before_selection, "cl=0.683 b(1,1) mode")
#g_tpr.Divide(h_c_s       , h_true            , "cl=0.683 b(1,1) mode")

# for debugging:
'''
g_efficiency.SetTitle('efficiency')
g_efficiency.SetFillColor(5)
g_efficiency.SetMarkerStyle(21)
g_efficiency.SetMarkerColor(4)
#g_efficiency.Draw('ALP')
#g_efficiency.Draw('ALPE1')
#g_efficiency.Draw('3A')a
#slp(33)

g_tpr.SetTitle('True Positive Rate')
g_tpr.SetFillColor(5)
g_tpr.SetMarkerStyle(21)
g_tpr.SetMarkerColor(4)
#g_tpr.Draw('ALP')
#g_tpr.Draw('3A')a
#slp(33)
'''



from ROOT import Double

g_size   = g_efficiency.GetN()
#g_size_s = g_tpr.GetN()

#print g_size
#print g_size_s

x        = Double()
y        = Double()

#x_s      = Double()
#y_s      = Double()

arr_x    = np.zeros(g_size)
arr_y    = np.zeros(g_size)

#arr_x_s  = np.zeros(g_size_s)
#arr_y_s  = np.zeros(g_size_s)

for i in xrange( g_size ):
    g_efficiency.GetPoint(i,x,y)
    arr_x[i] = x 
    arr_y[i] = y
#print arr_y
# if g_size is always equal to g_size_s we can put these loops together
#for i in xrange( g_size_s ):
#    g_tpr.GetPoint(i,x_s,y_s)
#    arr_x_s[i] = x_s 
#    arr_y_s[i] = y_s

# GetEYhigh() work as the following 3 ways(presumably the 'copy' version works most consistently):
#----------------------------------------------V1
#buffer_l = g_efficiency.GetEYlow()
#arr_l    = np.ndarray(g_size, 'f', buffer_l)
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
#print arr_h
#print arr_l
"""
buffer_l_s   = g_tpr.GetEYlow()
buffer_l_s.SetSize(g_size_s)
arr_l_s      = np.array(buffer_l_s, copy=True)

buffer_h_s   = g_tpr.GetEYhigh()
buffer_h_s.SetSize(g_size_s)
arr_h_s      = np.array(buffer_h_s, copy=True)
"""


print 'arr_h'
print arr_h
#print len(arr_l)




exit()


































#######################
# Export ROC Position #
#######################
from sklearn.externals import joblib

roc_dict              = {}
roc_dict['param']     = param
roc_dict['tpr']       = np.array(arr_y_s)
roc_dict['fpr']       = np.array(arr_y)
roc_dict['e_tpr_l']   = np.array(arr_l_s)
roc_dict['e_fpr_l']   = np.array(arr_l)
roc_dict['e_tpr_h']   = np.array(arr_h_s)
roc_dict['e_fpr_h']   = np.array(arr_h)
roc_dict['threshold'] = bin_value_dict
#roc_dict['raw'] =

path_dump = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
name_dump = 'roc.pkl'

joblib.dump(roc_dict, path_dump+name_dump)



############
# Draw ROC #
############
from array import array
from ROOT  import gROOT
from ROOT  import TPad

c1 = TCanvas('c1', 'Graph with asymmetric error band', 200, 10, 700, 500)
c1.Divide(2, 1, 0.)
p1 = c1.cd(1)
p2 = c1.cd(2)

p1.SetLogy()
p1.SetGrid()
p1.SetFillColor(19)

p2.SetGrid()
p2.SetFillColor(19)

#c1.GetFrame().SetFillColor(21)
#c1.GetFrame().SetBorderSize(12)

gROOT.SetBatch(1)

x   = array('f')
y   = array('f')
exl = array('f')
eyl = array('f')
exh = array('f')
eyh = array('f')

x   = np.array(arr_y_s)
y   = np.array(arr_y)
exl = np.array(arr_l_s)
eyl = np.array(arr_l)
exh = np.array(arr_h_s)
eyh = np.array(arr_h)

# somehow if you call one of the variables before the Draw() method the graph won't work properly
gr    = GAE(n_bins,x,y,exl,exh,eyl,eyh)
gr_s  = GAE(n_bins,x,y,exl,exh,eyl,eyh)

gr_c  = gr.Clone()
gr_sc = gr_s.Clone()
 
gr.SetTitle('ROC(zoomed in)') 
#gr.SetMarkerColor(8)
#gr.SetMarkerStyle(21)
gr.SetFillColor(632-9) 
gr_s.SetTitle('ROC')
gr_s.SetFillColor(632-9)
gr_sc.SetLineColor(4)

c1.cd(1)
gr.GetXaxis().SetRangeUser(0,0.5)
gr.GetYaxis().SetRangeUser(0.00001,0.01)
gr_c.GetXaxis().SetRangeUser(0,0.5)
gr_c.GetXaxis().SetRangeUser(0.00001,0.01)

gr_c.SetLineColor(4)

gr.Draw('SAME 3A')
gr_c.Draw('SAME XLP')

c1.cd(2)
gr_s.Draw('SAME 3A')
gr_sc.Draw('SAME XLP')
#slp(2)

c1.Print('roc.png')
c1.Update()


