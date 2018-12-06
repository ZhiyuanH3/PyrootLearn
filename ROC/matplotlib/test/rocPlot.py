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



def plotBDTsum(in_dict, pth_out):
   
    
    for key_par, item_par in in_dict.iteritems():
        for key_cut, item_cut in item_par.iteritems():
            if   key_cut == 'Loose Cut':    k_c = 'lc'  
            elif key_cut == 'Hard Cut' :    k_c = 'hc' 
            for key_model, item_model in item_cut.iteritems():
               
                if key_model == 'full_kin1': continue
                #if i_trn == 40        : continue
                print key_model 
         
                x = item_model['test_var']
                y = item_model['(1/FPR)|cut_TPR'] 
                Label = ': (TPR=%.3f,FPR=%.5f)'%(1,1)     
                plt.subplots_adjust(hspace=0.4)
                fig = plt.figure(num=None, figsize=(16, 9), dpi=120, facecolor='w', edgecolor='k')
        
                ax = plt.subplot(121)
                ax.set_yscale('log')
                axes = plt.gca()
                #axes.set_xlim([0.02,0.54]) 
                #axes.set_ylim([0.000001,0.1])
                plt.plot(x, y, 'or', label=Label)#, color=color_t, marker=Marker)                
                plt.grid(True, which='both')
                plt.legend( loc=4 , prop={'size': 15} )
                plt.title('bdt_generalization_compare', fontsize=24)
                plt.ylabel('(1/FPR)|cut_TPR', fontsize=20)
                plt.xlabel('test_'+key_par, fontsize=20)
        
                plt.subplot(122)
                plt.subplots_adjust(left=0, wspace=0.06)
                plt.grid(True)
                plt.legend( loc=2 , prop={'size': 15} ) #9#12#15
                plt.title('R', fontsize=24)
                #plt.ylabel('False Positive Rate', fontsize=20)
                #plt.xlabel('True Positive Rate', fontsize=20)
        
                plt.close()
                outName = key_par+'_'+k_c+'_'+key_model
                           
                fig.savefig(pth_out + outName + '.png', bbox_inches='tight')












###########
#         #
# testing #
#         #
###########
if __name__ == '__main__':
 
    from plot_samples import fileName
    plot_on      =    1
    out_name     =    'test'
    path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/bdt_overview/'+'Selected1_2best_kin0/'   
    path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/bdt_overview/all/'
    path_out     =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/roc/'
    #path_dump    = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
    #name_dump    = 'roc.pkl'
    fileNameDict = fileName   


    def read_pkl(pth,tsti):
        with open(pth,'read') as ff:
            pkls         = pickle.load(ff)
            if   p_typ == 'mass': par_str = 'masses'
            elif p_typ == 'ctau': par_str = 'ctau'
            empty = 1
            for key, item in pkls[par_str].iteritems():
                if key == tsti: empty = 0
                else          : empty = 1
            if empty == 0:    feature  = pkls[par_str][tsti]
            else                  :    
                #feature = {}
                feature = 0 
                print '>>>>>>>>>>>>>>>>>>>>>> empty!!!!'
        return feature


    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx


    mass_list    = [20,30,40,50,60]
    ctau_list    = [100,500,1000,2000,5000] 

    cut_type     = ['Loose Cut','Hard Cut']#['LCL','HCL']#['LC','HC']
    par_type     = ['mass','ctau']
    inputs       = ['2best','full']
    kin_var      = ['kin0','kin1']#['no_kin','with_kin']

    combi_dict   = {}
    cc           = 0
    for i in inputs:
        for j in kin_var:
            tmp_list = []
            tmp_list.append(i)
            tmp_list.append(j)
            combi_dict[cc] = '_'.join(tmp_list)
            cc            += 1

    empty_log = []
    out_dict  = {}


    for p_typ in par_type:
        out_dict[p_typ]         = {}
        for ci in cut_type:
            out_dict[p_typ][ci] = {}
            for key, item in combi_dict.iteritems():
                out_dict[p_typ][ci][item]   = {}

                if   p_typ == 'mass':    par_list = mass_list
                elif p_typ == 'ctau':    par_list = ctau_list 
                for i_trn in par_list:
                    for i_tst in par_list:
                        if item == 'full_kin1': continue
                        if i_trn == 40        : continue

                        if   p_typ == 'mass':
                            file_to_look = 'res_'+'trn'+'_'+str(i_trn)+'GeV_500mm_'+'tst'+'_'+str(i_tst)+'GeV_500mm_Selected1_'+item+'_v0.pickle'
                        elif p_typ == 'ctau':    
                            file_to_look = 'res_'+'trn'+'_'+str(40)+'GeV_'+str(i_trn)+'mm_'+'tst'+'_'+str(40)+'GeV_'+str(i_tst)+'mm_Selected1_'+item+'_v0.pickle'
                        print file_to_look 
                        path_tot     = path + file_to_look
                        in_dict      = read_pkl(path_tot, i_tst)
                        if in_dict:
                            roc_dict = in_dict['roc']   

                            fpr_bdt = roc_dict['fpr']
		            tpr_bdt = roc_dict['tpr']
		            e_tpr_l = roc_dict['e_tpr_l']
		            e_fpr_l = roc_dict['e_fpr_l']
		            e_tpr_h = roc_dict['e_tpr_h']
		            e_fpr_h = roc_dict['e_fpr_h']
                                
                            cut_dict = in_dict['cut_based'] 
                            dicti    = cut_dict[ci] 
			    sgn_eff  = dicti['tpr']
			    fls_eff  = dicti['fpr']
			    tpr_e_l  = dicti['tpr_e_l']
			    fpr_e_l  = dicti['fpr_e_l']
			    tpr_e_h  = dicti['tpr_e_h']
			    fpr_e_h  = dicti['fpr_e_h']
    
			    tmp_tpr, indx = find_nearest(tpr_bdt, sgn_eff)
                            tmp_fpr       = fpr_bdt[indx]
                            if tmp_fpr != 0: 
                                inv_fpr       = 1/float(tmp_fpr) 
                            else           :
                                inv_fpr       = 0
			    out_dict[p_typ][ci][item]['test_var']        = i_tst
			    out_dict[p_typ][ci][item]['(1/FPR)|cut_TPR'] = inv_fpr

                        else      :
                            out_dict[p_typ][ci][item]['test var']        = 0
                            out_dict[p_typ][ci][item]['(1/FPR)|cut_TPR'] = 0
                            empty_log.append(file_to_look)
                                  
    path_out = './plot/'
    print empty_log
    print out_dict

    ####################################################################
    ####################################################################
    if plot_on:
        plotBDTsum(out_dict, path_out)

