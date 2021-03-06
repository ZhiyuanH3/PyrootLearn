from sklearn.externals import joblib
import pickle
import matplotlib
matplotlib.use('Agg') #prevent the plot from showing
from   matplotlib import pyplot as plt
import numpy as np




def plotROC(inDict):

    Colors      = ['red','green','blue','black','lime','goldenrod','slateblue','yellowgreen','navy','yellow']
    colors      = ['pink','lightgreen','paleturquoise','grey','greenyellow','wheat','plum','y','gold']
    hatchs      = ['xx', '///', '||', '\\', '++', '---', '.']
    i           = 0
    orderedList = []


    roc_series    = 1#0

    if roc_series == 1:
        for dsci, dicti  in inDict.iteritems():
            orderedList.append(dsci)
        orderedList = sorted(orderedList)

        for dsci in orderedList:
            tmp_dict = inDict[dsci]['roc'] 
            #auc_bdt = tmp_dict['aoc']
            auc_bdt = inDict[dsci]['aoc']
    
            self_cut_base = 1
            use_indp_roc  = 1
              
            if   use_indp_roc == 1: 
                fpr_bdt = tmp_dict['fpr']
                tpr_bdt = tmp_dict['tpr']
                e_tpr_l = tmp_dict['e_tpr_l']            
                e_fpr_l = tmp_dict['e_fpr_l']            
                e_tpr_h = tmp_dict['e_tpr_h']            
                e_fpr_h = tmp_dict['e_fpr_h']            
           
            elif use_indp_roc == 0:
                fpr_bdt = inDict[dsci]['fpr']
                tpr_bdt = inDict[dsci]['tpr']
            plt.plot(tpr_bdt, fpr_bdt, label=str(dsci)+", AOC=%.4f"%auc_bdt, color=Colors[i])
            #plt.fill_between(tpr_bdt, fpr_bdt-e_fpr_l, fpr_bdt+e_fpr_h, alpha=0.7, color=colors[i], hatch=hatchs[i])      
            plt.fill_between(tpr_bdt, fpr_bdt-e_fpr_l, fpr_bdt+e_fpr_h, facecolor='none', hatch=hatchs[i], edgecolor=colors[i]) 

            if self_cut_base == 1:
                CBdict = inDict[dsci]['cut_based']
                for dsci, dicti  in CBdict.iteritems():
                    if 'H' in dsci: Marker = 'x'#'v'
                    else          : Marker = '.'     
                    sgn_eff = dicti['tpr']
                    fls_eff = dicti['fpr']
                   
                    tpr_e_l = dicti['tpr_e_l']
                    fpr_e_l = dicti['fpr_e_l']
                    tpr_e_h = dicti['tpr_e_h']
                    fpr_e_h = dicti['fpr_e_h']

                    asym_e_x = [np.array([tpr_e_l]), np.array([tpr_e_h])]
                    asym_e_y = [np.array([fpr_e_l]), np.array([fpr_e_h])]  

                    Label = dsci+': (TPR=%.3f,FPR=%.5f)'%(sgn_eff,fls_eff) #.6     
                     
                    
                    if i == 0:    
                        color_t = 'brown'
                        plt.plot(sgn_eff, fls_eff, 'or', label=Label, color=color_t, marker=Marker)
                        plt.errorbar(sgn_eff, fls_eff, yerr=asym_e_y, fmt='none', color=color_t)    
                    
                    #plt.plot(sgn_eff, fls_eff, 'or', label=Label, color=colors[i], marker=Marker)
                    #plt.errorbar(sgn_eff, fls_eff, yerr=asym_e_y, fmt='none', color=colors[i])

                    #plt.plot(sgn_eff, fls_eff, 'or', label=None, color=colors[i], marker=Marker)
                    #plt.errorbar(sgn_eff, fls_eff, xerr=asym_e_x, yerr=asym_e_y, fmt='none', color=colors[i])


            i += 1




    if 0:
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
        axes.set_xlim([0.02,0.54])#([0.0001,0.54])#([0.02,0.54])#0.02,0.44 
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
 
    from plot_samples import fileName

    plot_on      =    1
    out_name     =    'test'
    path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Brian/train_on_selected_QCD/' 

    #path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/generalization_bdt/rs/'

    #path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/generalization_bdt/'
    #path_out     =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/roc/'
    path_out      =   '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Brian/train_on_selected_QCD/roc/'  
    #path_dump    = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
    #name_dump    = 'roc.pkl'
    fileNameDict = fileName   

    fileNameDict = {
                     #'tt': 'RS_trn_40GeV_500mm_tst_40GeV_5000mm_slct1_attr_full_kin1_v0.pkl',
                     #'tt': 'RS_trn_40GeV_500mm_tst_40GeV_500mm_slct1_attr_full_kin1_v0.pkl', 
                     #'tt': 'RS_trn_40GeV_5000mm_tst_40GeV_500mm_slct1_attr_full_kin1_v0.pkl',
                     #'tt': 'RS_trn_40GeV_500mm_tst_40GeV_1000mm_slct1_attr_full_kin1_v0.pkl', 
                     #'tt': 'RS_trn_50GeV_500mm_tst_40GeV_500mm_slct1_attr_full_kin1_v0.pkl', 
                     #'tt': 'RS_trn_40GeV_5000mm_tst_40GeV_500mm_slct1_attr_full_kin1_v0.pkl',
                     'tt': 'RS_trn_50GeV_5000mm_tst_40GeV_500mm_slct1_attr_full_kin0_v0.pkl',
                   }



    def read_pkl(pth):
        pkls = joblib.load(pth)
        return pkls['data']

   

    ####################################################################
    pklDict = {}
    
    pklDict['tt'] = read_pkl(path+fileNameDict['tt'])


    cutBaseDict = {}
    ####################################################################

    if plot_on:
        plotROC_main(path_out, out_name, cutBaseDict, pklDict)

