from ROOT import TCanvas
from array import array

# debugging
#"""
c1 = TCanvas('c1', 'Graph with asymmetric error bars', 200, 10, 700, 500)
c1.SetFillColor(42)
c1.SetGrid()
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
n = 10

x   = array('f')
y   = array('f')
exl = array('f')
eyl = array('f')
exh = array('f')
eyh = array('f')

#print type(x)

x   = np.array([-0.22, 0.05, 0.25, 0.35, 0.5, 0.61,0.7,0.85,0.89,0.95] )
y   = np.array([1,2.9,5.6,7.4,9,9.6,8.7,6.3,4.5,1] )
exl = np.array([.05,.1,.07,.07,.04,.05,.06,.07,.08,.05] )
eyl = np.array([.8,.7,.6,.5,.4,.4,.5,.6,.7,.8] )
exh = np.array([.02,.08,.05,.05,.03,.03,.04,.05,.06,.03] )
eyh = np.array([.6,.5,.4,.3,.2,.2,.3,.4,.5,.6] )

#print type(x)

gr           = GAE(n,x,y,exl,exh,eyl,eyh)
gr.SetTitle('TGraphAsymmErrors')
gr.SetMarkerColor(4)
gr.SetMarkerStyle(21)
gr.Draw("ALP")
slp(35)
#"""















#"""
c1 = TCanvas('c1', 'Graph with asymmetric error bars', 200, 10, 700, 500)
c1.SetFillColor(42)
c1.SetGrid()
c1.GetFrame().SetFillColor(21)
c1.GetFrame().SetBorderSize(12)
#"""
x   = array('d')
y   = array('d')
exl = array('d')
eyl = array('d')
exh = array('d')
eyh = array('d')
#"""

x   = array('f')
y   = array('f')
exl = array('f')
eyl = array('f')
exh = array('f')
eyh = array('f')


print len(arr_y_s)
print len(arr_y)
print len(arr_l_s)
print len(arr_l)
print len(arr_h_s)
print len(arr_h)
#'''
for i in xrange(10):#(n_bins):
    x.append(arr_y_s[i])
    y.append(arr_y[i])
    exl.append(arr_l_s[i])
    eyl.append(arr_l[i])
    exh.append(arr_h_s[i])
    eyh.append(arr_h[i])
    #print arr_y_s[i]
#'''
print type(arr_y)
print type( list(arr_y) )
#"""
x   = np.array(arr_y_s)
y   = np.array(arr_y)
exl = np.array(arr_l_s)
eyl = np.array(arr_l)
exh = np.array(arr_h_s)
eyh = np.array(arr_h)
#"""


#"""
x   = array('d', [float(xx) for xx in list(arr_y_s)] )
y   = array('d', [float(xx) for xx in list(arr_y  )] )
exl = array('d', [float(xx) for xx in list(arr_l_s)] )
eyl = array('d', [float(xx) for xx in list(arr_l  )] )
exh = array('d', [float(xx) for xx in list(arr_h_s)] )
eyh = array('d', [float(xx) for xx in list(arr_h  )] )
#"""

#'''
x   = array('d', [1.,2.,3.] )
y   = array('d', [1.,2.,3.] )
exl = array('d', [1.,2.,3.] )
eyl = array('d', [1.,2.,3.] )
exh = array('d', [1.,2.,3.] )
eyh = array('d', [1.,2.,3.] )
#'''

#'''
x   = np.array([0.3])
y   = np.array([0.3])
exl = np.array([0.3])
eyl = np.array([0.3])
exh = np.array([0.3])
eyh = np.array([0.3])
#'''


#print x
#print type(x)

#gr = GAE(n_bins,x,y,exl,exh,eyl,eyh) 
gr = GAE(1,x,y,exl,exh,eyl,eyh)
#gr.SetTitle('ROC') 
gr.SetMarkerColor(4)
gr.SetMarkerStyle(21)
#gr.Draw("ALP")
#slp(22)
#"""

