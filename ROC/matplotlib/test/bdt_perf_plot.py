from sklearn.externals import joblib
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
    Colors      = ['red','green','blue','black','lime','goldenrod','slateblue','yellowgreen','navy','yellow']
    for key_par, item_par in in_dict.iteritems():
        if   key_par == 'mass':
            unit    = 'GeV'
            x_ticks = [20,30,40,50,60] 
        elif key_par == 'ctau':
            unit = 'mm'
            x_ticks = [100,500,1000,2000,5000]
        for key_cut, item_cut in item_par.iteritems():
            if   'loose' in key_cut:    key_cut_str = 'Loose Cut'
            elif 'hard'  in key_cut:    key_cut_str = 'Hard Cut'

            for key_model, item_model in item_cut.iteritems():
             
                if   'kin0' in key_model:    key_model_str = key_model.replace('_kin0', '')
                elif 'kin1' in key_model:    key_model_str = key_model.replace('_kin1', ' Kin.')
                plt.subplots_adjust(hspace=0.4)
                fig      = plt.figure(num=None, figsize=(16, 9), dpi=120, facecolor='w', edgecolor='k')
                ax = plt.subplot(121)
                ax.set_yscale('log')
                if key_par == 'ctau':    ax.set_xscale('log')
                axes = plt.gca()
                #axes.set_xlim([2,4]) 
                #axes.set_ylim([1,1])
                Label_cut    = key_cut_str
                c = 0
                for key_trn, item_trn in item_model.iteritems():
                    x        = item_trn['test_var']
                    y        = item_trn['(1/FPR)|cut_TPR'] 
                    y_eh     = item_trn['(1/FPR)|cut_TPR--eh']
                    y_el     = item_trn['(1/FPR)|cut_TPR--el']
                    y_cut    = item_trn['(1/FPR)_cut']
                    y_cut_eh = item_trn['(1/FPR)_cut_eh']
                    y_cut_el = item_trn['(1/FPR)_cut_el']
                   
                    asym_e_y     = [y_el, y_eh]
                    asym_e_y_cut = [y_cut_el, y_cut_eh]

                    Marker       = 'x'
                    Label        = 'Trained on '+str(key_trn)+unit+'('+key_model_str+')'     
                    color_t  = Colors[c] 
                    plt.plot(x, y, 'or', label=Label, color=color_t)                
                    plt.errorbar(x, y, yerr=asym_e_y, fmt='-o', color=color_t, alpha=0.5)
                    c += 1

                plt.plot(x, y_cut, 'or', label=Label_cut, color='brown', marker=Marker)                
                plt.errorbar(x, y_cut, yerr=asym_e_y_cut, fmt='none', color='brown', alpha=0.5)

                plt.grid(True, which='both')
                plt.legend( loc=1 , prop={'size': 12} )
                plt.title('BDT Generalization Compare', fontsize=24)
                plt.ylabel('1/FPR at '+key_cut_str+' TPR', fontsize=20)
                plt.xlabel('Test_'+key_par+'('+unit+')', fontsize=20)
                plt.xticks(x_ticks, x_ticks)         

                outName = key_par+'_'+key_cut+'_'+key_model
                fig.savefig(pth_out + outName + '.png', bbox_inches='tight')    
                plt.close()





###########
#         #
# testing #
#         #
###########
if __name__ == '__main__':
 
    from plot_samples import fileName
    plot_on      =    1
    out_name     =    'test'
    #path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/bdt_overview/'+'Selected1_2best_kin0/'   
    path         =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/result/Lisa/generalization_bdt/rs/'
    path_out     =    '/beegfs/desy/user/hezhiyua/LLP/bdt_output/roc/'
   
    fileNameDict = fileName   


    def read_pkl(pth):
        pkls = joblib.load(pth)        
        return pkls['data']


    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx


    mass_list    = [20,30,40,50,60]
    ctau_list    = [100,500,1000,2000,5000] 

    cut_type     = ['loose_cut','hard_cut']
    par_type     = ['mass','ctau']
    inputs       = ['2best','full']
    kin_var      = ['kin0','kin1']

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

    if 1:
        for p_typ in par_type:
            out_dict[p_typ]         = {}
            for ci in cut_type:
                out_dict[p_typ][ci] = {}
                for key, item in combi_dict.iteritems():
                    out_dict[p_typ][ci][item]   = {}
    
                    if   p_typ == 'mass':    par_list = mass_list
                    elif p_typ == 'ctau':    par_list = ctau_list 
                    for i_trn in par_list:
                        out_dict[p_typ][ci][item][i_trn]                        = {} 
                        out_dict[p_typ][ci][item][i_trn]['test_var']            = []
                        out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR']     = []
                        out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR--eh'] = []                         
                        out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR--el'] = []
                        out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut']         = []
                        out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut_eh']      = []
                        out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut_el']      = []
    
                        for i_tst in par_list:
    
                            if   p_typ == 'mass':
                                file_to_look = 'RS_'+'trn'+'_'+str(i_trn)+'GeV_500mm_'+'tst'+'_'+str(i_tst)+'GeV_500mm_slct1_attr_'+item+'_v0.pkl'
                            elif p_typ == 'ctau':    
                                file_to_look = 'RS_'+'trn'+'_'+str(40)+'GeV_'+str(i_trn)+'mm_'+'tst'+'_'+str(40)+'GeV_'+str(i_tst)+'mm_slct1_attr_'+item+'_v0.pkl'
                            print file_to_look 
                            path_tot     = path + file_to_look
                            in_dict      = read_pkl(path_tot)
                            if in_dict:
                                roc_dict = in_dict['roc']   
    
                                fpr_bdt = roc_dict['fpr']
		                tpr_bdt = roc_dict['tpr']
		                #e_tpr_l = roc_dict['e_tpr_l']
		                e_fpr_l = roc_dict['e_fpr_l']
		                #e_tpr_h = roc_dict['e_tpr_h']
		                e_fpr_h = roc_dict['e_fpr_h']
                                    
                                cut_dict = in_dict['cut_based'] 
                                dicti    = cut_dict[ci] 
			        sgn_eff  = dicti['tpr']
			        fls_eff  = dicti['fpr']
			        #tpr_e_l  = dicti['tpr_e_l']
			        fpr_e_l  = dicti['fpr_e_l']
			        #tpr_e_h  = dicti['tpr_e_h']
			        fpr_e_h  = dicti['fpr_e_h']
        
			        tmp_tpr, indx = find_nearest(tpr_bdt, sgn_eff)
                                tmp_fpr       = fpr_bdt[indx]
                                if tmp_fpr != 0: 
                                    inv_fpr       = 1/float(tmp_fpr) 
                                    inv_fpr_eh    = e_fpr_l[indx]/float( tmp_fpr*(tmp_fpr-e_fpr_l[indx]) )
                                    inv_fpr_el    = e_fpr_h[indx]/float( tmp_fpr*(tmp_fpr+e_fpr_h[indx]) ) 
                                else           :
                                    print '>>>>>>>>>>>>>>>>>>>> Zero devision!'
                                    inv_fpr       = 0
                                    inv_fpr_eh    = 0
                                    inv_fpr_el    = 0

                                if fls_eff != 0:
                                    inv_fpr_cut    = 1/float(fls_eff)
                                    inv_fpr_cut_eh = fpr_e_l/float( fls_eff*(fls_eff-fpr_e_l) )
                                    inv_fpr_cut_el = fpr_e_h/float( fls_eff*(fls_eff+fpr_e_h) )    
                                else           :
                                    print '>>>>>>>>>>>>>>>>>>>> Zero devision(cut_based point)!'
                                    inv_fpr_cut    = 0
                                    inv_fpr_cut_eh = 0
                                    inv_fpr_cut_el = 0

			        out_dict[p_typ][ci][item][i_trn]['test_var'].append( i_tst )
			        out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR'].append( inv_fpr )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR--eh'].append( inv_fpr_eh )    
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR--el'].append( inv_fpr_el )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut'].append( inv_fpr_cut )       
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut_eh'].append( inv_fpr_cut_eh )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut_el'].append( inv_fpr_cut_el )

                            else      :
                                print '>>>>>>>>>>>>>>>>>>>> no in_dict!!'
                                out_dict[p_typ][ci][item][i_trn]['test var'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR--eh'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)|cut_TPR--el'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut_eh'].append( 0 )
                                out_dict[p_typ][ci][item][i_trn]['(1/FPR)_cut_el'].append( 0 )


                                empty_log.append(file_to_look)
     

    path_out = './plot/'
    joblib.dump(out_dict,path_out+'o.pkl')
                             
   
    print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Empty_log:', empty_log
    #print out_dict

    ####################################################################
    ####################################################################
    if plot_on:
        plotBDTsum(out_dict, path_out)

