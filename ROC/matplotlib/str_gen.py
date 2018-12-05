
inputs   = "full"#"2best"
kin      = 1#0
if kin:    kin_str  = "+kin."
else  :    kin_str  = ""
#tstl_str = 

lt_list = [100,500,1000,2000,5000]
m_list  = [20,30,40,50,60]


"""
for tstl_str in lt_list:
    print "fileName = {"
    print "             'BDT("+inputs+kin_str+")--trained on 100' : 'res_trn_40GeV_100mm_tst_40GeV_"+str(tstl_str)+"mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 500' : 'res_trn_40GeV_500mm_tst_40GeV_"+str(tstl_str)+"mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 1000': 'res_trn_40GeV_1000mm_tst_40GeV_"+str(tstl_str)+"mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 2000': 'res_trn_40GeV_2000mm_tst_40GeV_"+str(tstl_str)+"mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 5000': 'res_trn_40GeV_5000mm_tst_40GeV_"+str(tstl_str)+"mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "           }"
"""

for tstm_str in m_list:
    print "fileName = {"
    print "             'BDT("+inputs+kin_str+")--trained on 20' : 'res_trn_20GeV_500mm_tst_"+str(tstm_str)+"GeV_500mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 30' : 'res_trn_30GeV_500mm_tst_"+str(tstm_str)+"GeV_500mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 40': 'res_trn_40GeV_500mm_tst_"+str(tstm_str)+"GeV_500mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 50': 'res_trn_50GeV_500mm_tst_"+str(tstm_str)+"GeV_500mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "             'BDT("+inputs+kin_str+")--trained on 60': 'res_trn_60GeV_500mm_tst_"+str(tstm_str)+"GeV_500mm_Selected1_"+inputs+"_kin"+str(kin)+"_v0.pickle',"
    print "           }"






