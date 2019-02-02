from __future__ import division
from ROOT import ROOT, gROOT, TDirectory, TFile, gFile, TBranch, TLeaf, TTree
from ROOT import TText, TPaveLabel, TLatex, TGraphErrors, TLine, gPad
from ROOT import TH1, TH1F, TH2F, TChain, TCanvas, TLegend, gStyle
from array import array
import math
from timeit import default_timer as timer

start= timer()
LUMI             = 35900 #in pb-1 (2016)
xs                = { 'QCD_50To100': 246300000 , 'QCD_100To200': 28060000 , 'QCD_200To300': 1710000 , 'QCD_300To500': 351300 , 'QCD_500To700': 31630 , 'QCD_700To1000': 6802 , 'QCD_1000To1500': 1206 , 'QCD_1500To2000': 120.4 , 'QCD_2000ToInf': 25.25 , 'sgn': 3.782 }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
gStyle.SetOptStat(0)     
#path0      = '/home/brian/datas/beeworkdir/'
#path1      = '/home/brian/Desktop/'
#path0       = '/home/brian/scp/dust/forBDT/'
#path0       = '/home/brian/scp/dust/forbdtnew/'
#path1       = '/home/brian/scp/dust/forBDT/plots/'
#path1       = '/home/brian/scp/dust/forbdtnew/plots/'

#path0 = '/home/brian/scp/dust/n/'
#path1 = '/home/brian/scp/dust/n/plots/'
path0 = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_forLola/'
path1 = '/beegfs/desy/user/hezhiyua/2bBacked/skimmed/Skim/fromBrian_forLola/plots/'


versionName = 'TuneCUETP8M1_13TeV-madgraphMLM-pythia8-v1'

ct_dep           = 0 #1 for ct dependence comparison
cut_on           = 0 #1 to apply cuts
qcd_weight_on    = 1#1
normalization_on = 1#1#0#1

log_y            = 1 # log scale for y axis
histStyl         = 'HIST,E1,SAME'#'colz,SAME'#'HIST,E1,SAME' 
histFillColOn    = 1
critical_line    = 0 #1 #draw red line 

number_of_bin    = 100
num_of_jets      = 1
twoD             = 0 # 2D plot option: 0 --> 1D
life_time        = ['0','0p05','0p1','1','5','10','25','50','100','500','1000','2000','5000','10000']
life_time_float  = [0.001,0.05,0.1,1,5,10,25,50,100,500,1000,2000,5000,10000]
len_of_lt        = len(life_time)

if ct_dep == 0:
    channel = {
           
           'QCD: combind'                    :'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC_1j_skimed.root',
           'VBF: c#tau=500mm, m_{#pi}=40GeV' :'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-500_TuneCUETP8M1_13TeV-powheg-pythia8_PRIVATE-MC_1j_skimed.root',
                
           #'QCD_HT50To100GeV'                :'QCD_HT50to100_' +versionName+'_1j_skimed.root',
           #'QCD_HT100To200GeV'               :'QCD_HT100to200_'+versionName+'_1j_skimed.root',
           #'QCD_HT200To300GeV'               :'QCD_HT200to300_'+versionName+'_1j_skimed.root',
           #'QCD_HT300To500GeV'               :'QCD_HT300to500_'+versionName+'_1j_skimed.root',

           #'QCD_HT500To700GeV'               :'QCD_HT500to700_'  +versionName+'_1j_skimed.root',
           #'QCD_HT700To1000GeV'              :'QCD_HT700to1000_' +versionName+'_1j_skimed.root',
           #'QCD_HT1000To1500GeV'             :'QCD_HT1000to1500_'+versionName+'_1j_skimed.root',
           #'QCD_HT1500To2000GeV'             :'QCD_HT1500to2000_'+versionName+'_1j_skimed.root',
           #'QCD_HT2000ToInfGeV'              :'QCD_HT2000toInf_' +versionName+'_1j_skimed.root',
           
           #'t#bar{t}'                        :'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8.root',
           #'VBF-0mm-40GeV'                   :'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root',
           #'ZH-0mm-40GeV'                    :'ZH_HToSSTobbbb_ZToLL_MH-125_MS-40_ctauS-0_TuneCUETP8M1_13TeV-powheg-pythia8.root',
           #'H#rightarrowb#bar{b}'            :'VBFHToBB_M-125_13TeV_powheg_pythia8.root'
               }
    if qcd_weight_on == 1:
        channel_qcd = {
               'QCD_50To100' :'QCD_HT50to100_' +versionName+'_1j_skimed.root',
               'QCD_100To200':'QCD_HT100to200_'+versionName+'_1j_skimed.root',
               'QCD_200To300':'QCD_HT200to300_'+versionName+'_1j_skimed.root',
               'QCD_300To500':'QCD_HT300to500_'+versionName+'_1j_skimed.root',

               'QCD_500To700'  :'QCD_HT500to700_'  +versionName+'_1j_skimed.root',
               'QCD_700To1000' :'QCD_HT700to1000_' +versionName+'_1j_skimed.root',
               'QCD_1000To1500':'QCD_HT1000to1500_'+versionName+'_1j_skimed.root',
               'QCD_1500To2000':'QCD_HT1500to2000_'+versionName+'_1j_skimed.root',
               'QCD_2000ToInf' :'QCD_HT2000toInf_' +versionName+'_1j_skimed.root',
                       }   

elif ct_dep == 1:
    channel = {}
    for lt in life_time:
        #channel['ct' + lt] = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-' + lt + '_TuneCUETP8M1_13TeV-powheg-pythia8'+'_1j_skimed'+'.root'

        channel['ct' + lt] = 'VBFH_HToSSTobbbb_MH-125_MS-40_ctauS-' + lt + '_TuneCUETP8M1_13TeV-powheg-pythia8'+'_Tranche2_PRIVATE-MC_1j_skimed'+'.root'

    channel['QCD'] = 'QCD_HT100to200_'+versionName+'_1j_skimed.root'
    legends = 'SGN(VBF)'
    legendb = 'BKG(QCD)'

#attr = ['dR_q1','dR_q2','dR_q3','dR_q4']
#attr = ['pt', 'eta', 'phi', 'CSV', 'chf', 'nhf', 'phf', 'elf', 'muf', 'chm', 'cm', 'nm']
#attr = ['pt']
#attr = ['mass']
#attr = ['FracCal','cHadEFrac']#['pt']
#attr = ['cHadEFrac']
#attr = ['cHadE','nHadE','cHadEFrac','nHadEFrac','nEmE','nEmEFrac','cEmE','cEmEFrac','cmuE','cmuEFrac','muE','muEFrac','eleE','eleEFrac','eleMulti','photonE','photonEFrac','photonMulti','cHadMulti','nHadMulti','npr','cMulti','nMulti','FracCal']
#attr_dict = {'pt':'p_{T}', 'eta':'#eta', 'phi':'#phi', 'CSV':'Combined Secondary Vertex(CSV)', 'chf':'Charged Hadron Energy Fraction', 'nhf':'Neutral Hadron Fraction', 'phf':'Photon Fraction', 'elf':'Electron Fraction', 'muf':'Muon Fraction', 'chm':'Charged Hadron Multiplicity', 'cm':'Charged Multiplicity', 'nm':'Neutral Multiplicity'}
attr_dict = {'pt':'p_{T}', 'eta':'#eta', 'phi':'#phi', 'cHadE':'cHadE', 'nHadE':'nHadE', 'cHadEFrac':'Charged Hadron Energy Fraction', 'nHadEFrac':'nHadEFrac', 'nEmE':'nEmE', 'nEmEFrac':'nEmEFrac', 'cEmE':'cEmE', 'cEmEFrac':'cEmEFrac', 'cmuE':'cmuE', 'cmuEFrac':'cmuEFrac', 'muE':'muE', 'muEFrac':'muEFrac', 'eleE':'eleE', 'eleEFrac':'eleEFrac', 'eleMulti':'eleMulti', 'photonE':'photonE', 'photonEFrac':'photonEFrac', 'photonMulti':'photonMulti', 'cHadMulti':'cHadMulti', 'npr':'npr', 'cMulti':'cMulti', 'nMulti':'nMulti','FracCal':'E_{EMCal} / E_{HCal}' }

####################################generating list with 10 Jets
def jet_list_gen(n):
    jl = []
    for ii in range(1,n+1): 
        #jl.append('Jet' + "%s" %ii)
        jl.append('Jet' + "%s" %ii + 's')
    return jl
####################################generating list with 10 Jets
jet = jet_list_gen(num_of_jets)

#++++++++++++++++++++++++++++cuts+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
########################################################################
def cut_dict_gen(cut_name):
    cut_dict = {}
    cut_dict['pt'] =  '(' + cut_name + 'pt' + '>' + '15' + ')' # + '&&' + '(' + cut_name + 'pt' + '>' + '70' + ')' + '&&' + '(' + cut_name + 'pt' + '<' + '75' + ')'  
    cut_dict['eta'] = '(' + cut_name + 'eta' + '<' + '2.4' + ')' + '&&' + '(' + cut_name + 'eta' + '>' + '-2.4' + ')'
    cut_dict['dR'] = '(' + cut_name + 'dR_q1' + '<' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q2'+ '>=' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q3'+ '>=' + '0.4' + ')' + '&&' + '(' + cut_name + 'dR_q4'+ '>=' + '0.4' + ')'
    cut_dict['chf'] = ''
    #cut_dict['GenBquark'] = '(GenBquark1.pt>15)&&(GenBquark1.eta<2.4)&&(GenBquark1.eta>-2.4)' 
    return cut_dict
########################################################################
###################################################################################################
def cutting_gen(pref):
    for i in jet:
        cuts = cut_dict_gen( pref + i + '.'  )
    cuttings_sgn = cuts['pt'] + '&&' + cuts['eta'] + '&&' + cuts['dR']  #+ '&&' + cut_dict['GenBquark']
    cuttings_bkg = cuts['pt'] + '&&' + cuts['eta'] 
    return cuttings_bkg, cuttings_sgn
###################################################################################################
cutting_bkg, cutting_sgn = cutting_gen('')
if cut_on == 0:
    cutting_bkg, cutting_sgn = '', ''

###################################################################################################
def cut_tex_gen(cut):
    inf = float(88888888)
    cut_str = cut.replace('(','').replace(')','').replace('&&','&').replace('<=','#leq').replace('phi','#phi').replace('eta','#eta').replace('>=','#geq') 
    cut_str = cut_str.replace('Jet1.','').replace('GenBquark','Gbq').replace('pt','p_{T}').replace('dR_','#DeltaR-')
    cut_str_list = cut_str.split('&')
    bound = {}
    for ct in cut_str_list:       
        if '#leq' in ct:             
            at, n = ct.split('#leq')
        elif '#geq' in ct:          
            at, n = ct.split('#geq')
        elif '<' in ct:            
            at, n = ct.split('<')
        elif '>' in ct:            
            at, n = ct.split('>')  
        bound[at] = {}
        bound[at]['LB'] = []
        bound[at]['UB'] = []
        bound[at]['syb'] = []
        bound[at]['B'] = []
    for ct in cut_str_list:    
        if '#leq' in ct: 
            syb = '#leq'
            at, num = ct.split('#leq')
        elif '#geq' in ct:
            syb = '#geq'
            at, num = ct.split('#geq')
        elif '<' in ct:
            syb = '<'
            at, num = ct.split('<')
        elif '>' in ct:
            syb = '>'
            at, num = ct.split('>')
                
        if syb not in bound[at]['syb']:
            bound[at]['syb'].append(syb)
        
        if syb == '#geq' or syb == '>':
            bound[at]['LB'].append( float(num) )
            bound[at]['UB'].append( inf )
        elif syb == '#leq' or syb == '<':    
            bound[at]['LB'].append( -inf ) 
            bound[at]['UB'].append( float(num) )                 
    ct_text = {}
    w = 0        
    for a in bound:    
        bound[a]['B'].append( max(bound[a]['LB']) ) 
        bound[a]['B'].append( min(bound[a]['UB']) )
        if -inf == float( min(bound[a]['B']) ):
            bb = a + ' ' + bound[a]['syb'][0] + ' ' + str( max(bound[a]['B']) )
        elif inf is float( max(bound[a]['B']) ):    
            bb = a + ' ' + bound[a]['syb'][0] + ' ' + str( min(bound[a]['B']) )
        else:
            if '>' in bound[a]['syb']: 
                bb = str( min(bound[a]['B']) ) + ' < ' + a 
                if '<' in bound[a]['syb']:    
                    bb = bb + ' < ' + str( max(bound[a]['B']) )
                else:    
                    bb = bb + ' #leq ' + str( max(bound[a]['B']) )
            else:
                bb = str( min(bound[a]['B']) ) + ' #leq ' + a
                if '<' in bound[a]['syb']:    
                    bb = bb + ' < ' + str( max(bound[a]['B']) )           
                else:    
                    bb = bb + ' #leq ' + str( max(bound[a]['B']) )                            
        ct_text[a] = TLatex(.77, .51 - 0.04*w, bb)  
        ct_text[a].SetNDC()
        ct_text[a].SetTextSize(0.03)
        w += 1
    return ct_text    
###################################################################################################
if cut_on == 0:
    cut_text = {}
    cut_text['no cut'] = TLatex(.77, .51 - 0.04*0, '') 
    cut_text['no cut'].SetNDC()
    cut_text['no cut'].SetTextSize(0.03)
elif cut_on == 1:
    cut_text = cut_tex_gen(cutting_sgn) 

print('---------cut:')
print(cutting_sgn)

entry = {'entries': ''}
#++++++++++++++++++++++++++++cuts+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Settings~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

############################################################
def file_dict_gen(path,chann,forqcd=0):
    fd = {}
    for cc in chann:  
        if forqcd == 1:
            fd[cc] = TFile(path + chann[cc],"UPDATE")
        elif forqcd == 0:    
            fd[cc] = TFile(path + chann[cc],"r")
    return fd
############################################################
file_dict = file_dict_gen(path0,channel)

########################################
def file_str_dict_gen(path,chann):
    fd = {}
    for cc in chann:
             fd[cc] = path + chann[cc]
    return fd
########################################
file_str_dict_qcd = file_str_dict_gen(path0,channel_qcd)
file_dict_qcd = file_dict_gen(path0,channel_qcd,forqcd=1)

##weight tree#######################################################
if qcd_weight_on == 1:
    chn_qcd = TChain('tree44')
    qcd_entries = 0
    weight_dict = {}

    xs_tot  = 0
    for i in xs:
            xs_tot += xs[i]

    for cc in channel_qcd:
        treee   = file_dict_qcd[cc].Get('tree44')
        nevents = treee.GetEntries('Jet1s.pt')
        print 'events'
        print nevents
        #weight  = xs[cc] / float(nevents*(xs['QCD_50To100']+xs['QCD_100To200']+xs['QCD_200To300']+xs['QCD_300To500'])) #LUMI * xs[cc] / float(nevents) #(xs['QCD_50To100']+xs['QCD_100To200']+xs['QCD_200To300']+xs['QCD_300To500'])
        
        
        weight  = xs[cc] / float( xs_tot )     
        
        if   '50To100'  in cc:
            weight_dict['QCD_HT50To100GeV']  = weight
        elif '100To200' in cc:
            weight_dict['QCD_HT100To200GeV'] = weight 
        elif '200To300' in cc:
            weight_dict['QCD_HT200To300GeV'] = weight
        elif '300To500' in cc:
            weight_dict['QCD_HT300To500GeV'] = weight

        elif '500To700' in cc:
            weight_dict['QCD_HT500To700GeV']   = weight 
        elif '700To1000' in cc:
            weight_dict['QCD_HT700To1000GeV']  = weight
        elif '1000To1500' in cc:
            weight_dict['QCD_HT1000To1500GeV'] = weight   
        elif '1500To2000' in cc:
            weight_dict['QCD_HT1500To2000GeV'] = weight 
        elif '2000ToInf' in cc:
            weight_dict['QCD_HT2000ToInfGeV']  = weight     
        #weight_dict[cc] = weight
        treee.SetWeight(weight)
        treee.AutoSave()
        qcd_entries = qcd_entries + nevents
        file_dict_qcd[cc].Close()
    for cc in channel_qcd:
        chn_qcd.Add( path0 + channel_qcd[cc] )
##weight tree#######################################################
print chn_qcd

plotrange = {}
tree = {}
hist = {}
if ct_dep == 0:    
    ##############################
    for cc in channel:
        hist[cc] = {}
    ##############################
elif ct_dep == 1:     
    mean ={}        #dictionary to hold all mean values
    errors ={}      #dictionary to hold all errors
    entries_after_cut = {}
    yy ={}          #dictionary to hold all arrays of y values for TGraph
    ey ={}          #dictionary to hold all arrays of errors for TGraph
    ##############################
    for cc in channel:
        hist[cc] = {}
        mean[cc] ={}
        errors[cc] ={}
        entries_after_cut[cc] ={}
    ##############################
    entries_after_cut['QCD'] = {}
    entries_after_cut['sgn'] = {}
    yy['QCD'] ={} 
    yy['sgn'] ={}       
    ey['QCD'] ={} 
    ey['sgn'] ={} 
    #######################################
    x = array( 'd' )        # array to plot for TGraph
    ex = array( 'd' )
    for ll in life_time_float:
        x.append( ll )
        ex.append( 0.0  )
    #######################################

####################################################################################################################
def write_1(var,sample,cuts):
    for s in attr:
        if   'combind'   in sample:
            color1 = 30#3       #880+1 #400+3	6 8 634 1
        elif 'HT50'  in sample:#'H#rightarrowb#bar{b}' in sample:   
            color1 = 17                 #800+10 860
        elif 'HT100' in sample:#'VBF' in sample:
            color1 = 4
        elif 'HT200' in sample:#'ZH' in sample:
            color1 = 6
        elif 'HT300' in sample:#
            color1 = 9

        elif 'HT500' in sample:#
            color1 = 10
        elif 'HT700' in sample:#
            color1 = 51
        elif 'HT1000' in sample:#
            color1 = 99
        elif 'HT1500' in sample:#
            color1 = 33
        elif 'HT2000' in sample:#
            color1 = 2
        


        elif 'VBF'   in sample:#
            color1 = 38#2

        elif 't#bar{t}' in sample:
            color1 = 2  

        if s == 'pt':
            h_par = [number_of_bin,0,1400] #300
        elif s == 'eta':
            h_par = [number_of_bin,-2.5,2.5]
        elif s == 'phi':
            h_par = [number_of_bin,-math.pi,math.pi]
        elif s == 'CSV':
            h_par = [number_of_bin,0,1]
        elif s == 'chf':
            h_par = [number_of_bin,0,1]
        elif s == 'nhf':
            h_par = [number_of_bin,0,1]
        elif s == 'phf':
            h_par = [number_of_bin,0,1]
        elif s == 'elf':
            h_par = [number_of_bin,0,1]
        elif s == 'muf':
            h_par = [number_of_bin,0,1]
        elif s == 'chm':
            h_par = [number_of_bin,0,100]
        elif s == 'chm':
            h_par = [number_of_bin,0,100]
        elif s == 'cm':
            h_par = [number_of_bin,0,100]
        elif s == 'nm':
            h_par = [number_of_bin,0,100]
        elif s == 'dR_q1':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'dR_q2':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'dR_q3':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'dR_q4':
            h_par = [number_of_bin,-1.1,3*math.pi]
        elif s == 'nPV':
            h_par = [number_of_bin,0,80]

        elif s == 'cHadE':
            h_par = [number_of_bin,0,200]
        elif s == 'nHadE':
            h_par = [number_of_bin,0,200]
        elif s == 'cHadEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'nHadEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'nEmE':
            h_par = [number_of_bin,0,200]
        elif s == 'nEmEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'cEmE':
            h_par = [number_of_bin,0,200]
        elif s == 'cEmEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'cmuE':
            h_par = [number_of_bin,0,200]
        elif s == 'cmuEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'muE':
            h_par = [number_of_bin,0,200]
        elif s == 'muEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'eleE':
            h_par = [number_of_bin,0,200]
        elif s == 'eleEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'eleMulti':
            h_par = [5,0,5]
        elif s == 'photonE':
            h_par = [number_of_bin,0,200]
        elif s == 'photonEFrac':
            h_par = [number_of_bin,0,1]
        elif s == 'photonMulti':
            h_par = [60,0,60]
        elif s == 'cHadMulti':
            h_par = [50,0,50]
        elif s == 'nHadMulti':
            h_par = [50,0,50]
        elif s == 'npr':
            h_par = [90,0,90]
        elif s == 'cMulti':
            h_par = [50,0,50]
        elif s == 'nMulti':
            h_par = [60,0,60]
        elif s == 'FracCal':
            h_par = [number_of_bin,0,150] #400
           
        tree[sample] = file_dict[sample].Get('tree44') #ntuple/tree
        
        if   twoD == 0:
            hist[sample][s] = TH1F(sample+s, '; %s; events' %s , h_par[0], h_par[1], h_par[2])
        elif twoD == 1:
            hist[sample][s] = TH2F(sample+s, '; %s; events' %s , h_par[0], h_par[1], h_par[2] , number_of_bin, 0, 300)
        print( 'loading TTree:' )    
        
        print( tree[sample] )
        hist[sample][s].Sumw2()

        if   twoD == 0:
            if qcd_weight_on == 1:
                if 'combind' in sample:
                    chn_qcd.Project(sample+s, var + '.' + s, cuts )
                else:
                    tree[sample].Project(sample+s, var + '.' + s, cuts )
            elif qcd_weight_on == 0:
                tree[sample].Project(sample+s, var + '.' + s, cuts ) 
        elif twoD == 1:
            tree[sample].Project(sample+s, var + '.' + s + ':' + var + '.' + 'pt', cuts ) 
        
        normalizationFactor = float(hist[sample][s].Integral())
        if normalizationFactor != 0: 
            normalizationFactor = 1 / normalizationFactor

            if 'HT' in sample:
                normalizationFactor = weight_dict[sample] 
            if normalization_on == 1:
                hist[sample][s].Scale( normalizationFactor ) #hist[sample][s].Scale(1)
        else:
            print("zero denominator!")
        
        if qcd_weight_on == 0:
            entr = tree[sample].GetEntries(cuts)
        else:
            entr = qcd_entries
        if   ct_dep == 0:
            entry['entries'] = '[entries:' + str(entr) + ']'
            hist[sample][s].SetLineColor(color1)
            hist[sample][s].SetLineWidth(3)
            hist[sample][s].SetTitle( attr_dict[s] )

            #hist[sample][s].SetTitleSize(0.4,'t')  
            plotrange[s] =  max( plotrange[s] , hist[sample][s].GetMaximum() + hist[sample][s].GetRMS() * normalizationFactor )
            print( 'Entries:' )  			
            print( hist[sample][s].GetEntries() )
        elif ct_dep == 1:
            entries_after_cut[sample][s] = tree[sample].GetEntries( cuts ) # to be optimized
            errors[sample][s]            = hist[sample][s].GetStdDev() #saving errors of the histogram
            #errors[sample][s]           = hist[sample][s].GetRMS()
            mean[sample][s]              = hist[sample][s].GetMean()     #saving means of the histogram
            plotrange[s]                 =  max( plotrange[s] , mean[sample][s] + hist[sample][s].GetRMS() )
####################################################################################################################

###########################################################################
def write_2(sample):
    #for cc in channel:
    for s in attr:
        yy[sample][s] = array( 'd' )     #declaring the yy array
        ey[sample][s] = array( 'd' )     #declaring the ey array    
        for ll in enumerate(life_time):
            if sample == 'QCD':
                yy[sample][s].append( mean['QCD'][s] )
                ey[sample][s].append( errors['QCD'][s] )
            else:
                yy[sample][s].append( mean['ct'+ll[1]][s] )
                ey[sample][s].append( errors['ct'+ll[1]][s] )
###########################################################################

##########################################################
def plot_2(var,cuts):
    for s in attr:
        c1 = TCanvas("c1", "Signals", 1200, 800)

        if log_y == 1: 
            c1.SetLogy()

        c1.SetTopMargin(0.08)#0.12
        c1.SetBottomMargin(0.11)#0.12
        c1.SetLeftMargin(0.14)
        c1.SetRightMargin(0.14)#0.24
        c1.cd()
        #c1.SetGrid()
        gStyle.SetTitleFontSize(0.04)
        if ct_dep == 0:
            if s in ('elf','muf','cm','nm','chm'): 
                c1.SetLogx()
            for cc in channel:
                #hist[cc][s].SetMaximum(0.44)
                if   'combind' in cc:     
                    fc = 30
                    #hist[cc][s].SetFillStyle()#3005)
                elif 'VBF'      in cc:   
                    fc = 38    
                    hist[cc][s].SetFillStyle(3444)
                elif 'HT50'     in cc:  
                    fc = 7
                    hist[cc][s].SetFillStyle(3001)                  
                elif 'HT100'    in cc: 
                    fc = 4
                    hist[cc][s].SetFillStyle(3002) 
                elif 'HT200'    in cc: 
                    fc = 6
                    hist[cc][s].SetFillStyle(3003) 
                elif 'HT300'    in cc: 
                    fc = 9
                    hist[cc][s].SetFillStyle(3004) 
                
                if histFillColOn == 1:
                    pass
                    #hist[cc][s].SetFillColor(fc) 
                
                hist[cc][s].Draw(histStyl) 
            #legend = TLegend(0.76, 0.56, 0.99, 0.88)
            legend = TLegend(0.60, 0.9-0.04*2, 0.85, 0.9) #x_left y_bottom x_right y_top
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)#1001
            legend.SetFillColor(0)
            #legend.SetHeader( entry['entries'] )
            for cc in channel:
                legend.AddEntry(hist[cc][s],cc)
            legend.Draw()
            for ct in cut_text:
                cut_text[ct].Draw()
            
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Line for critical value
            if   s == 'chm':
                l = TLine(11.4,0.0,11.4,0.084) 
            elif s == 'cHadEFrac':
                l = TLine(0.38,0.0,0.38,0.027)
            elif s == 'FracCal':
                l = TLine(30,0.0,30,0.44)
            #l.SetLineColor(2)
            #l.SetLineWidth(3)
            if critical_line == 1: 
                l.SetLineColor(46)#4,2
                l.SetLineWidth(3)
                l.Draw('same')

            c1.Print(path1 + s + var + cuts.replace('(','_').replace(')','_').replace('&&','_').replace('>','LG').replace('<','LS').replace('=','EQ').replace('.','P').replace('-','N').replace('Jet','J').replace('GenBquark','GBQ') + ".pdf")
            
        elif ct_dep == 1:
            eac0 = str( entries_after_cut['ct0'][s] )
            c1.SetLogx()
            #gr = TGraph( len_of_lt , x , yy['sgn'][s] )
            gr = TGraphErrors( len_of_lt , x , yy['sgn'][s] , ex , ey['sgn'][s] )
            gr.SetMarkerSize(1.5)
            gr.SetMarkerStyle(1)
            gr.GetYaxis().SetTitleOffset(1.6)
            gr.SetLineColor(4)
            gr.SetLineWidth(4)
            gr.SetTitle('mean ' + s )
            gr.GetXaxis().SetTitle('decaying length (mm)')
            gr.GetYaxis().SetTitle('mean normalized number of events')
            gr.GetXaxis().SetTitleOffset(1.4)
            gr.SetMaximum( plotrange[s] * 1.12 )
            gr.SetName('sgn')
            gr.Draw('ACP')  # '' sets up the scattering style
            gr1 = TGraphErrors( len_of_lt , x , yy['QCD'][s] , ex , ey['QCD'][s] )
            gr1.SetMarkerSize(1.0)
            gr1.SetMarkerStyle(1)
            gr.GetYaxis().SetTitleOffset(1.6)
            gr1.SetLineColor(2)
            gr1.SetLineWidth(2)
            gr1.SetName('QCD')
            #gr1.SetTitle('averaged ' + s)
            #gr1.GetXaxis().SetTitle('decaying length (mm)')
            #gr1.GetYaxis().SetTitle('mean frequency')
            gr1.Draw('CP')  # '' sets up the scattering style
            legend = TLegend(0.76, 0.56, 0.99, 0.88)
            legend.SetHeader( 'Entries: ' + eac0 )
            legend.AddEntry('QCD', legendb, 'l')
            legend.AddEntry('sgn', legends, 'l')
            legend.Draw()
            for ct in cut_text:
                cut_text[ct].Draw()
            c1.Print(path1 + 'mean_' + s + var + cuts.replace('(','_').replace(')','_').replace('&&','_').replace('>','LG').replace('<','LS').replace('=','EQ').replace('.','P').replace('-','N').replace('Jet','J').replace('GenBquark','GBQ') + ".pdf")
        c1.Update()
        c1.Close() 
        print('|||||||||||||||||||||||||||||||||||||||||||||||||||')        
##########################################################

########################################################################
def clear_hist(sample):
    for s in attr:
        if gROOT.FindObject( sample+s ) != None:
            hh = gROOT.FindObject( sample+s ) #to find the histogram
            hh.Delete()    #to delete the histogram
########################################################################

########################################################################
def set_hist_yrange():
    os = 1.15
    for cc in channel:
        for s in attr:
            hist[cc][s].SetMaximum( plotrange[s] * os )

            hist[cc][s].GetYaxis().SetTitleOffset(1.4)#1.6
            hist[cc][s].GetYaxis().SetTitle('Events(normalized)')
            hist[cc][s].GetYaxis().SetTitleSize(0.04)
            #hist[cc][s].GetYaxis().SetLabelSize(0.05)
            hist[cc][s].GetXaxis().SetTitle( s )
            if   s == 'chf':
                hist[cc][s].GetXaxis().SetTitle( 'cHadEFrac' )
            elif s == 'chm':
                hist[cc][s].GetXaxis().SetTitle( 'cHadMulti' )
            hist[cc][s].GetXaxis().SetTitleSize(0.045)
            
            if   s == 'elf':
                hist[cc][s].SetAxisRange(0., 0.02,"Y")
            elif s == 'muf':
                hist[cc][s].SetAxisRange(0., 0.02,"Y")      
            elif s == 'chm':
                hist[cc][s].SetAxisRange(1, 45,"X") 
                hist[cc][s].SetAxisRange(0., 0.10,"Y")    
########################################################################

########################################################################
def init_plotrange():
    for s in attr:
        plotrange[s] = 0           
########################################################################

#===========================================================================================
#===========================================================================================
init_plotrange()
if ct_dep == 0:
    for i in jet:    
        for cc in channel:
            
            if 'QCD' in cc:
                cutting = cutting_bkg
            else:
                cutting = cutting_sgn

            write_1(i,cc,cutting)

        set_hist_yrange()
        plot_2(i,cutting)

elif ct_dep == 1:
    for i in jet:
        for cc in channel:

            if 'QCD' in cc:
                cutting = cutting_bkg
            else:
                cutting = cutting_sgn

            write_1(i,cc,cutting)
        write_2('QCD')
        write_2('sgn')
        plot_2(i,cutting)

plotrange.clear()
for cc in channel:
    clear_hist(cc) 
    hist[cc].clear()
    tree.clear()

for cc in channel:
        file_dict[cc].Close()
#===========================================================================================
#===========================================================================================









end = timer() 
print("Time taken:", end-start) 
"""
###########################################################
def findDirName() 
    #file_dict['QCD']
    TIter next(file_dict['QCD'].GetListOfKeys())
    key = TKey
    while key = next():
        cl = TClass
        cl = gROOT.GetClass(key.GetClassName())
        if (cl.InheritsFrom("TDirectory")):
            dir = TDirectory
            dir = (TDirectory*)key.ReadObj()
            print( "Directory name: " + dir.GetName() )
###########################################################
"""



