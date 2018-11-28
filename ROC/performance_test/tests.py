# first create some data
import pandas as pd
import numpy  as np
#import random 
from   sklearn.externals   import joblib
from   time                import sleep as slp
from   time                import time

n_scan  = 10000000
n_bins  = 10#100
bin_i   = 0
bin_f   = 1
pth     = '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/'
#pth     = '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/bdt_overview/dumps/trained_on/40_500mm/test_on/40_500mm/'
draw    = 1

param           = {}
param['n_scan'] = n_scan 
param['n_bins'] = n_bins
param['bin_i']  = bin_i
param['bin_f']  = bin_f
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Loading data...'
load_s = joblib.load(pth+'/dumps/s.pkl')
#load_b = joblib.load(pth+'/dumps/b.pkl')
#print len(load_b)

# Calculate the bin vector:
bin_width = float(bin_f - bin_i)/n_bins
bin_value_dict = {}
for j in xrange(n_bins):
    bin_value_dict[j] = bin_i + (0.5+j)*bin_width

bin_list = []
#for key, val in bin_value_dict.iteritems():
#    bin_list.append(val)
for i in xrange(n_bins):
    bin_list.append( 0+i*bin_width )
bin_list.append(1)
print bin_list

#print bin_value_dict




from ROOT import TGraphAsymmErrors as GAE
from ROOT import TH1F, TChain
from ROOT import TCanvas
from ROOT import Double
import           root_numpy      as rnp
import           multiprocessing as mp
# if you want to use the GetCumulative() of a histogram and set its error: do not call the Sumw2() of it
h_after_selection  = TH1F('h_after_selection' , 'hist_after_selection' , n_bins, bin_i, bin_f)
#h_after_selection.Sumw2()
h_before_selection = TH1F('h_before_selection', 'hist_before_selection', n_bins, bin_i, bin_f)
#h_before_selection.Sumw2()

h_true_positive    = TH1F('h_true_positive' , 'True_Positives' , n_bins, bin_i, bin_f)
h_true             = TH1F('h_true'          , 'Trues'          , n_bins, bin_i, bin_f)
h_true.Sumw2()
# see if reversing the bin_min and bin_max will cause the histogram axis to reverse(no)
#h_true          = TH1F('h_true'          ,'Trues'          , n_bins, bin_f, bin_i)

h_c_b = TH1F('h_c_b' , 'hist_after_selection_cum_rev' , n_bins, bin_i, bin_f)
#h_c_b.Sumw2()
h_c_s = TH1F('h_c_s' , 'hist_true_positives_cum_rev'  , n_bins, bin_i, bin_f)
h_c_s.Sumw2()





if 1:
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Filling histogram...'
    zeitA = time()
    #df_b        = load_b.copy()[:n_scan]
    #df_b['bin'] = df_b['signal']
    #print df_b
    #group_w = df_b.groupby(  pd.cut(df_b['bin'], [0,0.5,1])  ).sum()
    #print group_w
    
    df_s        = load_s.copy()
    df_s['bins'] = df_s['signal']
    #print df_s
    group_w = df_s.groupby(  pd.cut(df_s['bins'], bin_list)  )
    g_w = df_s.groupby(  pd.cut(df_s['bins'], bin_list)  ).agg(['count','sum'])
    print g_w
    print group_w.groups
    df_g_w_s_w =  ( group_w.sum() )['weight'].copy()[:]
    df_g_w_s   =  ( group_w.sum() ).copy()
    
    print group_w.aggregate(np.sum)[:]
    print df_g_w_s_w[5:].sum()
    
    
    def get_index(row):
        return row.name
    
    
    
    #df_g_w_s['b'] = df_g_w_s.name
    #df_g_w_s.reset_index(drop=False)
    
    
    #dfx = df_g_w_s[['weight','signal']]
    #print dfx
    dfx = df_g_w_s[['weight']].copy()
    dfx.fillna(0,inplace=True)
    dfx['ii'] = range(len(dfx))
    dfx['w2'] = dfx['weight'].apply(lambda x: x*x)
    print dfx
    
    dfy = dfx.iloc[::-1]
    print dfy
    
    #dfy['recum'] = dfy['weight'].cumsum()
    dfy.loc[:, 'recum'] = dfy['weight'].cumsum()
    dfy.loc[:, 'rc_w2'] = dfy['w2'].cumsum()
    print dfy
    
    dfz = dfy.iloc[::-1]
    dfx['recum'] = dfz['recum']
    dfx['rc_w2_sq'] = dfz['rc_w2'].apply(lambda x: np.sqrt(x))
    
    w_s = dfx['weight'].sum()
    w2_s = dfx['w2'].sum()
    dfx['ws'] = w_s
    dfx['w2s'] = w2_s
    
    
    print dfx
    
    #dfx['be']  = dfx[]
    
    #df_g_w_s['i'] = df_g_w_s.apply(lambda row: row.name, axis=1)
    #print df_g_w_s
    
    print dfx.recum.iloc[5]
    
    
    
    h1 = TH1F('h1','h1',n_bins,0,1)
    h2 = TH1F('h2','h2',n_bins,0,1)
    #rnp.fill_hist(h_1, dfx.recum, dfx.weight)
    for ii in xrange(n_bins):
        i = ii+1
        #print i
        h1.SetBinContent(i,dfx.recum.iloc[ii])
        h1.SetBinError(i,dfx.rc_w2_sq.iloc[ii])
    
        h2.SetBinContent(i,dfx.ws.iloc[ii])
        h1.SetBinError(i,dfx.w2s.iloc[ii])
    
    #g_fpr = GAE()
    g_tpr = GAE()
    #g_fpr.Divide(h_c_b, h_before_selection, "cl=0.683 b(1,1) mode")
    g_tpr.Divide(h1, h2         , "cl=0.683 b(1,1) mode")
    
    g_size   = g_tpr.GetN()
    
    #x        = Double()
    #y        = Double()
    x_s      = Double()
    y_s      = Double()
    
    #arr_x    = np.zeros(g_size)
    #arr_y    = np.zeros(g_size)
    arr_x_s  = np.zeros(g_size)
    arr_y_s  = np.zeros(g_size)
    
    for i in xrange( g_size ):
        #g_fpr.GetPoint(i,x,y)
        #arr_x[i]   = x
        #arr_y[i]   = y
    
        g_tpr.GetPoint(i,x_s,y_s)
        arr_x_s[i] = x_s
        arr_y_s[i] = y_s

    print '!!!!'    
    print arr_x_s
    print arr_y_s


    #buffer_l   = g_fpr.GetEYlow()
    #buffer_l.SetSize(g_size)
    #arr_l      = np.array(buffer_l, copy=True)
    
    #buffer_h   = g_fpr.GetEYhigh()
    #buffer_h.SetSize(g_size)
    #arr_h      = np.array(buffer_h, copy=True)
    #print arr_h
    #print arr_l
    
    buffer_l_s   = g_tpr.GetEYlow()
    buffer_l_s.SetSize(g_size)
    arr_l_s      = np.array(buffer_l_s, copy=True)
    
    buffer_h_s   = g_tpr.GetEYhigh()
    buffer_h_s.SetSize(g_size)
    arr_h_s      = np.array(buffer_h_s, copy=True)
    print arr_h_s
    print arr_l_s
    
    
    
    
    
    exit()
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    


print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Filling histogram (for tpr)...'
zeitA = time()
for index, row in load_s.iterrows():
    tmp_weight    = row['weight']
    tmp_signal    = row['signal']
# somehow slowest 
#for i in load_s.index:
#    tmp_weight = load_s.loc[i,'weight']
#    tmp_signal = load_s.loc[i,'signal']
    for k in xrange(n_bins):
        h_true.Fill(bin_value_dict[k], tmp_weight)
        if bin_value_dict[k] - 0.5*bin_width <= tmp_signal and bin_value_dict[k] + 0.5*bin_width > tmp_signal:
            for kk in xrange(k):
                h_c_s.Fill(bin_value_dict[kk], tmp_weight)



g_tpr = GAE()
#g_fpr.Divide(h_c_b, h_before_selection, "cl=0.683 b(1,1) mode")
g_tpr.Divide(h_c_s, h_true         , "cl=0.683 b(1,1) mode")

g_size   = g_tpr.GetN()

#x        = Double()
#y        = Double()
x_s      = Double()
y_s      = Double()

#arr_x    = np.zeros(g_size)
#arr_y    = np.zeros(g_size)
arr_x_s  = np.zeros(g_size)
arr_y_s  = np.zeros(g_size)

for i in xrange( g_size ):
    #g_fpr.GetPoint(i,x,y)
    #arr_x[i]   = x
    #arr_y[i]   = y

    g_tpr.GetPoint(i,x_s,y_s)
    arr_x_s[i] = x_s
    arr_y_s[i] = y_s

print '!!!!!!!!'
print arr_x_s
print arr_y_s
#buffer_l   = g_fpr.GetEYlow()
#buffer_l.SetSize(g_size)
#arr_l      = np.array(buffer_l, copy=True)

#buffer_h   = g_fpr.GetEYhigh()
#buffer_h.SetSize(g_size)
#arr_h      = np.array(buffer_h, copy=True)
#print arr_h
#print arr_l

buffer_l_s   = g_tpr.GetEYlow()
buffer_l_s.SetSize(g_size)
arr_l_s      = np.array(buffer_l_s, copy=True)

buffer_h_s   = g_tpr.GetEYhigh()
buffer_h_s.SetSize(g_size)
arr_h_s      = np.array(buffer_h_s, copy=True)
print arr_h_s
print arr_l_s




exit()













g_fpr = GAE()
g_tpr = GAE()
g_fpr.Divide(h_c_b, h_before_selection, "cl=0.683 b(1,1) mode")
g_tpr.Divide(h_c_s, h_true            , "cl=0.683 b(1,1) mode")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> for debugging:
'''
g_fpr.SetTitle('efficiency(fpr)')
g_fpr.SetFillColor(5)
g_fpr.SetMarkerStyle(21)
g_fpr.SetMarkerColor(4)
#g_fpr.Draw('ALP')
#g_fpr.Draw('ALPE1')
#g_fpr.Draw('3A')a
#slp(33)
g_tpr.SetTitle('True Positive Rate')
g_tpr.SetFillColor(5)
g_tpr.SetMarkerStyle(21)
g_tpr.SetMarkerColor(4)
#g_tpr.Draw('ALP')
#g_tpr.Draw('3A')a
#slp(33)
'''

g_size   = g_fpr.GetN()

x        = Double()
y        = Double()
x_s      = Double()
y_s      = Double()

arr_x    = np.zeros(g_size)
arr_y    = np.zeros(g_size)
arr_x_s  = np.zeros(g_size)
arr_y_s  = np.zeros(g_size)

for i in xrange( g_size ):
    g_fpr.GetPoint(i,x,y)
    arr_x[i]   = x 
    arr_y[i]   = y

    g_tpr.GetPoint(i,x_s,y_s)
    arr_x_s[i] = x_s 
    arr_y_s[i] = y_s

buffer_l   = g_fpr.GetEYlow()
buffer_l.SetSize(g_size)
arr_l      = np.array(buffer_l, copy=True)

buffer_h   = g_fpr.GetEYhigh()
buffer_h.SetSize(g_size)
arr_h      = np.array(buffer_h, copy=True)
#print arr_h
#print arr_l

buffer_l_s   = g_tpr.GetEYlow()
buffer_l_s.SetSize(g_size)
arr_l_s      = np.array(buffer_l_s, copy=True)

buffer_h_s   = g_tpr.GetEYhigh()
buffer_h_s.SetSize(g_size)
arr_h_s      = np.array(buffer_h_s, copy=True)
print len(arr_h)
print len(arr_l)



#######################
# Calculate AOC       #
#######################

'''
x   = np.array(arr_y_s)
y   = np.array(arr_y)
exl = np.array(arr_l_s)
eyl = np.array(arr_l)
exh = np.array(arr_h_s)
eyh = np.array(arr_h)
'''



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

roc_dict['cut_based'] = {}
roc_dict['cut_based']['lc'] = LC_dict
roc_dict['cut_based']['hc'] = HC_dict
#roc_dict['aoc']       = aoc
#roc_dict['aoc_l']       = aoc_l
#roc_dict['aoc_h']       = aoc_h

#raw_data           = {}
#raw_data['load_s'] = load_s
#raw_data['load_b'] = load_b
#roc_dict['raw'] = raw_data

path_dump = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
name_dump = 'roc.pkl'

joblib.dump(roc_dict, path_dump+name_dump)


############
# Draw ROC #
############
if draw == 1:
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
    
    # for cut based points:
    x_c   = array('f')
    y_c   = array('f')
    exl_c = array('f')
    eyl_c = array('f')
    exh_c = array('f')
    eyh_c = array('f')

    x_c   = np.array(LC_dict['tpr'])
    y_c   = np.array(LC_dict['fpr'])
    exl_c = np.array(LC_dict['tpr_e_l'])
    eyl_c = np.array(LC_dict['fpr_e_l'])
    exh_c = np.array(LC_dict['tpr_e_h'])
    eyh_c = np.array(LC_dict['fpr_e_h'])


    # somehow if you call one of the variables before the Draw() method the graph won't work properly
    gr    = GAE(n_bins,x,y,exl,exh,eyl,eyh)
    gr_s  = GAE(n_bins,x,y,exl,exh,eyl,eyh)
    
    gr_LC = GAE(1,x_c,y_c,exl_c,exh_c,eyl_c,eyh_c) 

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
    
    gr_LC.GetXaxis().SetRangeUser(0,0.5)
    gr_LC.GetYaxis().SetRangeUser(0.00001,0.01)


    gr_c.SetLineColor(4)
    
    gr.Draw('SAME 3A')
    gr_c.Draw('SAME XLP')

    gr_LC.Draw('SAME A')    

    c1.cd(2)
    gr_s.Draw('SAME 3A')
    gr_sc.Draw('SAME XLP')
    slp(2)
    
    c1.Print('roc.png')
    c1.Update()















###########
#         #
# BackUps #
#         #
###########

#=================================================================================================
'''
import root_numpy as rnp

zeitA = time()

df_b        = load_b.copy()[:n_scan]
df_b['bin'] = df_b['signal']

#df_s        = load_s.copy()
#df_s['bin'] = df_s['signal']

#for k in xrange(n_bins):
#    mask_k_b = ( bin_value_dict[k] - 0.5*bin_width <= df_b['bin'] ) & ( bin_value_dict[k] + 0.5*bin_width > df_b['bin'] )
#    df_b['bin'][mask_k_b] = k
#    mask_k_s = ( bin_value_dict[k] - 0.5*bin_width <= df_s['bin'] ) & ( bin_value_dict[k] + 0.5*bin_width > df_s['bin'] )
#    df_s['bin'][mask_k_s] = k

df_list_pre_sel = []
df_list_pos_sel = []
for k in xrange(n_bins):
 
    mask_k_b = ( bin_value_dict[k] - 0.5*bin_width <= df_b['bin'] ) & ( bin_value_dict[k] + 0.5*bin_width > df_b['bin'] )
    df_b['bin'][mask_k_b] = k
    #mask_k_s = ( bin_value_dict[k] - 0.5*bin_width <= df_s['bin'] ) & ( bin_value_dict[k] + 0.5*bin_width > df_s['bin'] )
    #df_s['bin'][mask_k_s] = k

    mask_k = df_b.bin == k
    df_b_w_k = df_b.weight[mask_k]

    df_list_k_pre_sel = []
    df_list_k_pos_sel = []

    for kk in xrange(n_bins):
        df_tmp_kk_pre_sel           = pd.DataFrame()
        df_tmp_kk_pre_sel['weight'] = df_b_w_k
        df_tmp_kk_pre_sel['bin']    = bin_value_dict[kk]
        df_list_k_pre_sel.append(df_tmp_kk_pre_sel)
        if kk > k: continue
        df_tmp_kk_pos_sel           = pd.DataFrame()
        df_tmp_kk_pos_sel['weight'] = df_b_w_k
        df_tmp_kk_pos_sel['bin']    = bin_value_dict[kk]
        df_list_k_pos_sel.append(df_tmp_kk_pos_sel)

    df_tmp_k_pre_sel = pd.concat(df_list_k_pre_sel)
    df_tmp_k_pos_sel = pd.concat(df_list_k_pos_sel)
    
    df_list_pre_sel.append(df_tmp_k_pre_sel)
    df_list_pos_sel.append(df_tmp_k_pos_sel)    

df_before_selection = pd.concat(df_list_pre_sel)
df_after_selection  = pd.concat(df_list_pos_sel)

rnp.fill_hist(h_before_selection, df_before_selection.bin, df_before_selection.weight)
rnp.fill_hist(h_c_b             , df_after_selection.bin , df_after_selection.weight)

zeitB = time()
print 'Time taken for filling histogram(for #events: ' + str(n_scan) + '): ', str(zeitB-zeitA)
'''


# GetEYhigh() work as the following 3 ways(presumably the 'copy' version works most consistently):
#----------------------------------------------V1
#buffer_l = g_fpr.GetEYlow()
#arr_l    = np.ndarray(g_size, 'f', buffer_l)
#----------------------------------------------V2
#buffer_h   = g_fpr.GetEYhigh()
#arr_h      = np.frombuffer(buffer_h, count=g_size)
#----------------------------------------------V3
#=================================================================================================





