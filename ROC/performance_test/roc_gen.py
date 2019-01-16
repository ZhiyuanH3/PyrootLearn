import pandas          as pd
import numpy           as np
#import root_numpy      as rnp
import multiprocessing as mp
import random 
from   sklearn.externals import joblib
from   time              import sleep             as slp
from   time              import time
from   ROOT              import TGraphAsymmErrors as GAE
from   ROOT              import TH1F, TChain
from   ROOT              import TCanvas
from   ROOT              import Double


def SetBin(load,n_bins,bin_list):
    df                  = load.copy()
    df['w2']            = df['weight'].copy().apply( np.square )
    group_w             = df.groupby(  pd.cut(df['signal'], bin_list)  )
    df_g_w_s            =  ( group_w.sum() ).copy()
    df1                 = df_g_w_s[['weight']].copy()
    df1.fillna(0,inplace=True)
    df1['w2']           = df1['weight'].apply( np.square )
    df2                 = df1.iloc[::-1]
    df2.loc[:, 'recum'] = df2['weight'].cumsum()
    df2.loc[:, 'rc_w2'] = df2['w2'].cumsum()
    df3                 = df2.iloc[::-1]
    df1['recum']        = df3['recum']
    df1['rc_w2_sq']     = df3['rc_w2'].apply( np.sqrt )
    w_s                 = df1['weight'].sum()
    sqr_s_w2            = np.sqrt( df['w2'].sum() )

    xl, yl, hl, ll = [], [], [], []
    for i in xrange(n_bins):
        h_post = TH1F('h_post', 'h_post', 1, bin_list[i], bin_list[i+1])
        h_pre  = TH1F('h_pre' , 'h_pre' , 1, bin_list[i], bin_list[i+1])
        h_post.SetBinContent(1, df1.recum.iloc[i])
        h_post.SetBinError(1  , df1.rc_w2_sq.iloc[i])
        h_pre.SetBinContent(1 , w_s)
        h_pre.SetBinError(1   , sqr_s_w2) 

        g_eff  = GAE()
        g_eff.Divide(h_post, h_pre, "cl=0.683 b(1,1) mode")

        x      = Double()
        y      = Double()

        g_eff.GetPoint(0,x,y)

        xl.append(x)
        yl.append(y)

        buffer_l   = g_eff.GetEYlow()
        buffer_l.SetSize(1)
        arr_l      = np.array(buffer_l, copy=True)

        buffer_h   = g_eff.GetEYhigh()
        buffer_h.SetSize(1)
        arr_h      = np.array(buffer_h, copy=True)

        hl.append(np.array(arr_h)[0])
        ll.append(np.array(arr_l)[0])

        h_post.Delete()
        h_pre.Delete()

    #print xl
    #print yl
    #print hl
    #print ll
    out_dict       = {}
    out_dict['x']  = xl
    out_dict['y']  = yl
    out_dict['eh'] = hl
    out_dict['el'] = ll

    return out_dict


def ROC_GEN(load_s, load_b):
    #n_scan  = 10000000
    n_bins  = 1000
    bin_i   = 0
    bin_f   = 1
    
    param           = {}
    #param['n_scan'] = n_scan 
    param['n_bins'] = n_bins
    param['bin_i']  = bin_i
    param['bin_f']  = bin_f
    
    bin_width = float(bin_f - bin_i)/n_bins
    bin_value_dict = {}
    for j in xrange(n_bins):
        bin_value_dict[j] = bin_i + (0.5+j)*bin_width
    #print bin_value_dict
    
    bin_list = []
    for i in xrange(n_bins):
        bin_list.append( 0+i*bin_width )
    bin_list.append(1)
    #print bin_list
    
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>filling histogram...'
    zeitA = time()
    
    tp_dict = SetBin(load_s, n_bins, bin_list)
    fp_dict = SetBin(load_b, n_bins, bin_list)
    
    zeitB = time()
    print 'Time taken for filling histogram: ', str(zeitB-zeitA)

    #######################
    # Export ROC Position #
    #######################
    roc_dict              = {}
    roc_dict['param']     = param
    roc_dict['tpr']       = np.array(tp_dict['y'])
    roc_dict['fpr']       = np.array(fp_dict['y'])
    roc_dict['e_tpr_l']   = np.array(tp_dict['el'])
    roc_dict['e_fpr_l']   = np.array(fp_dict['el'])
    roc_dict['e_tpr_h']   = np.array(tp_dict['eh'])
    roc_dict['e_fpr_h']   = np.array(fp_dict['eh'])
    roc_dict['threshold'] = bin_value_dict
    #roc_dict['raw'] =
    """
    path_dump = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
    name_dump = 'roc.pkl'    
    joblib.dump(roc_dict, path_dump+name_dump)
    """

    return roc_dict
    

if __name__ == '__main__':

    pth    = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_forLola/h5/2d/out/first_test2/'+'dumps/'
    #pth     = '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/'

    def read_h5(Name):
        input_filename = pth+Name
        store          = pd.HDFStore(input_filename)
        tb             = store.select('table')#              ,
        #                              start = i_start      ,
        #                              stop  = i_start + batch_size)
    
        #stb         = tb.iloc[:, :-3]
        #stb         = np.array(stb)
        return tb

    load_s = read_h5('s.h5')
    load_b = read_h5('b.h5')

    #load_s = joblib.load(pth+'/dumps/s.pkl')
    #load_b = joblib.load(pth+'/dumps/b.pkl')

    #import pickle
    #with open(pth+'/dumps/s.pkl','r') as fs:
    #    load_s = pickle.load(fs)
    #with open(pth+'/dumps/b.pkl','r') as fb:
    #    load_b = pickle.load(fb)

    #load_s = pd.read_pickle(pth+'/dumps/s.pkl')
    #load_b = pd.read_pickle(pth+'/dumps/b.pkl')

    

    roc_dict = ROC_GEN(load_s, load_b)    


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
    
    x   = np.array(roc_dict['tpr'])
    y   = np.array(roc_dict['fpr'])
    exl = np.array(roc_dict['e_tpr_l'])
    eyl = np.array(roc_dict['e_fpr_l'])
    exh = np.array(roc_dict['e_tpr_h'])
    eyh = np.array(roc_dict['e_fpr_h'])
    
    # somehow if you call one of the variables before the Draw() method the graph won't work properly
    n_bins = roc_dict['param']['n_bins']
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
    y_lim_min = 0.00001
    y_lim_max = 0.5
    gr.GetXaxis().SetRangeUser(0,0.5)
    gr.GetYaxis().SetRangeUser(y_lim_min,y_lim_max)
    gr_c.GetXaxis().SetRangeUser(0,0.5)
    gr_c.GetXaxis().SetRangeUser(y_lim_min,y_lim_max)
    
    gr_c.SetLineColor(4)
    
    gr.Draw('SAME 3A')
    gr_c.Draw('SAME XLP')
    
    c1.cd(2)
    gr_s.Draw('SAME 3A')
    gr_sc.Draw('SAME XLP')
    #slp(2)
    
    c1.Print('roc.png')
    c1.Update()
    
    
