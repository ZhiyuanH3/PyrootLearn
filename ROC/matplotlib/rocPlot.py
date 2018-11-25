from sklearn.externals import joblib
import pickle
import matplotlib
matplotlib.use('Agg') #prevent the plot from showing
from   matplotlib import pyplot as plt
import numpy as np




def plotROC(inDict):

    Colors      = ['red','green','blue','black','lime','goldenrod','slateblue','yellowgreen','navy','yellow']
    colors      = ['pink','lightgreen','paleturquoise','grey','greenyellow','wheat','plum','y','gold']
    i           = 0
    orderedList = []


    roc_series    = 0

    if roc_series == 1:
        for dsci, dicti  in inDict.iteritems():
            orderedList.append(dsci)
        orderedList = sorted(orderedList)
        for dsci in orderedList:
    
            #auc_bdt = inDict[dsci]['aoc']
            auc_bdt = inDict['aoc']
    
            self_cut_base = 1
            use_indp_roc  = 0
              
            if   use_indp_roc == 1: 
                fpr_bdt = inDict['fpr']
                tpr_bdt = inDict['tpr']
                e_tpr_l = inDict['e_tpr_l']            
                e_fpr_l = inDict['e_fpr_l']            
                e_tpr_h = inDict['e_tpr_h']            
                e_fpr_h = inDict['e_fpr_h']            
           
            elif use_indp_roc == 0:
                fpr_bdt = inDict[dsci]['fpr']
                tpr_bdt = inDict[dsci]['tpr']
            plt.plot(tpr_bdt, fpr_bdt, label=dsci+", AOC=%.4f"%auc_bdt, color=colors[i])
    
            if self_cut_base == 1:
                CBdict = inDict[dsci]['cut_base']
                for dsci, dicti  in CBdict.iteritems():
                    if 'H' in dsci: Marker = 'v'
                    else          : Marker = '.'     
                    sgn_eff = dicti[0]
                    fls_eff = dicti[1] 
                    plt.plot(sgn_eff, fls_eff, 'or', label=dsci+': (TPR=%.3f,FPR=%.5f)'%(sgn_eff,fls_eff), color=colors[i], marker=Marker)
            i += 1

    ########################################################################
    # Baysian Uncertainty
    fpr     = np.asarray( inDict['fpr'] )
    tpr     = np.asarray( inDict['tpr'] )
    e_fpr_l = np.asarray( inDict['e_fpr_l'] )
    e_fpr_h = np.asarray( inDict['e_fpr_h'] )
    aoc     = np.asarray( inDict['aoc'] )

    plt.plot(tpr, fpr, label='mass=50GeV'+", AOC=%.4f"%aoc, color='red')
    plt.fill_between(tpr, fpr-e_fpr_l, fpr+e_fpr_h, alpha=0.3, color='green')
    CBdict  = inDict['cut_base']
    for dsci, dicti  in CBdict.iteritems():
        if 'H' in dsci: Marker = 'v'
        else          : Marker = '.'
        sgn_eff = dicti[0]
        fls_eff = dicti[1]
        plt.plot(sgn_eff, fls_eff, 'or', label=dsci+': (TPR=%.3f,FPR=%.5f)'%(sgn_eff,fls_eff), color='blue', marker=Marker)



def plotCuts(inDict):
    colors = ['red','green','blue']
    i = 0
    for dsci, dicti  in inDict.iteritems():
        sgn_eff = dicti[0]
        fls_eff = dicti[1]
        plt.plot(sgn_eff, fls_eff, 'or', label=dsci+': (TPR=%.3f,FPR=%.5f)'%(sgn_eff,fls_eff), color=colors[i])
        i += 1

def plotROC_main(pathOut,outName,cutBase_dict,pkl_dict):
    if 1:
        plt.subplots_adjust(hspace=0.4)
        fig = plt.figure(num=None, figsize=(16, 9), dpi=120, facecolor='w', edgecolor='k')

        ax = plt.subplot(121)
        #ax.set_yscale("log", nonposx='clip')
        ax.set_yscale('log')
        #ax.set_xscale('log')
        axes = plt.gca()
        axes.set_xlim([0.02,0.54])#0.02,0.44 
        axes.set_ylim([0.000001,0.1])#0.0001
        plotROC(pkl_dict)
        #plotCuts(cutBase_dict)
        plt.grid(True, which='both')
        #plt.legend( loc=4 , prop={'size': 15} )
        plt.title('ROC (zoomed in)', fontsize=24)
        plt.ylabel('False Positive Rate', fontsize=20)
        plt.xlabel('True Positive Rate', fontsize=20)

        plt.subplot(122)
        plt.subplots_adjust(left=0, wspace=0.06)
        plotROC(pkl_dict)
        #plotCuts(cutBase_dict)
        #plt.plot([0, 1], [0, 1], color='navy', lw=1, linestyle='--')
        plt.grid(True)
        plt.legend( loc=2 , prop={'size': 15} ) #9#12#15
        plt.title('ROC', fontsize=24)
        #plt.ylabel('False Positive Rate', fontsize=20)
        plt.xlabel('True Positive Rate', fontsize=20)

        #plt.ioff()
        plt.close()
        #plt.show(block=False)

        fig.savefig(pathOut + outName + '.png', bbox_inches='tight')
#########################################################################################









###########
#         #
# testing #
#         #
###########
if __name__ == '__main__':
 
    plot_on      =    1
    out_name     =    'test'
    #path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/'
    #path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/temp/forCompare/'
    path_out     =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/roc/'
    path_dump    = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
    name_dump    = 'roc.pkl'

    fileNameDict = {
                     'BDT()'       : 'result_with_pt_mass_energy_v1_withSelection.pickle',
                     'bdt'         : 'result_v1_withSelection.pickle' 
                   }
   
    cutBaseDict  = {
                      'Loose Cut': [0.127,0.00364],#[0.1955307262569827 , 0.003643577798535045],
                      'Hard Cut' : [0.101,0.00061]#[0.15642458100558612, 0.0006177645800627758]
                   }
    
    ####################################################################
    roc_dict             = joblib.load(path_dump+name_dump)
    roc_dict['cut_base'] = cutBaseDict
    roc_dict['aoc']      = 0.8934
    pklDict              = roc_dict
    '''
    pklDict  = {}
    pklDict['50'] = {}
    pklDict['50']['tpr']
    pklDict['50']['fpr']
    pklDict['50']['']
    '''
    ####################################################################

    if plot_on:
        plotROC_main(path_out, out_name, cutBaseDict, pklDict)

