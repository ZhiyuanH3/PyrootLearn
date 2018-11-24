from time import sleep as slp


#######################
# Import ROC Position #
#######################
from sklearn.externals import joblib


path_dump = '/beegfs/desy/user/hezhiyua/2bBacked/roc_data/'
name_dump = 'roc.pkl'

roc_dict = {}

roc_dict = joblib.load(path_dump+name_dump)

############
# Draw ROC #
############
from array import array
from ROOT  import gROOT, TPad, TCanvas
from ROOT  import TGraphAsymmErrors as GAE

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

x   = roc_dict['tpr']
y   = roc_dict['fpr']
exl = roc_dict['e_tpr_l']
eyl = roc_dict['e_fpr_l']
exh = roc_dict['e_tpr_h']
eyh = roc_dict['e_fpr_h']

#n_bins = roc_dict['param']['n_bins']
n_bins = 1000

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
slp(12)

c1.Print('roc.png')
c1.Update()


