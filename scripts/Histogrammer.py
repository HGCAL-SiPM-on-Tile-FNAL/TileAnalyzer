import ROOT
from ROOT import TFile, TTree, TList
import sys
import os
import argparse
import math
import ast
import glob
from array import array
from  ConfigParser import * 

def meanandstdv(test_list):
    mean = sum(test_list) / len(test_list) 
    variance = sum([((x - mean) ** 2) for x in test_list]) / len(test_list) 
    res = variance ** 0.5
    return float(mean),float(res)

def Fill_Histograms(inputfile,outputfile,expvalues,module_ring):
    #Create outputfile    
    tmp = ROOT.TFile.Open(outputfile,'RECREATE')
    #----------------Create your histograms in here --------------------------

    #Calibrated value vs specs (target)
    h_dtop_ms_tar          = ROOT.TH1F("h_dtop_ms_tar","h_dtop_ms_tar",80,-0.8, 0.8)
    h_dbot_ms_tar          = ROOT.TH1F("h_dbot_ms_tar","h_dbot_ms_tar",80,-0.8, 0.8)
    h_drgt_ms_tar          = ROOT.TH1F("h_drgt_ms_tar","h_drgt_ms_tar",80,-0.8, 0.8)
    h_dlft_ms_tar          = ROOT.TH1F("h_dlft_ms_tar","h_dlft_ms_tar",80,-0.8, 0.8)
    h_dhgt_ms_tar          = ROOT.TH1F("h_dhgt_ms_tar","h_dhgt_ms_tar",80,-0.8, 0.8)
    h_dwth_ms_tar          = ROOT.TH1F("h_dwth_ms_tar","h_dwth_ms_tar",80,-0.8, 0.8)
    h_drgt_dlft_ms_tar     = ROOT.TH2F("h_drgt_dlft_ms_tar","h_drgt_dlft_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dtop_dlft_ms_tar     = ROOT.TH2F("h_dtop_dlft_ms_tar","h_dtop_dlft_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dtop_drgt_ms_tar     = ROOT.TH2F("h_dtop_drgt_ms_tar","h_dtop_drgt_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dtop_dbot_ms_tar     = ROOT.TH2F("h_dtop_dbot_ms_tar","h_dtop_dbot_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dbot_dlft_ms_tar     = ROOT.TH2F("h_dbot_dlft_ms_tar","h_dbot_dlft_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dbot_drgt_ms_tar     = ROOT.TH2F("h_dbot_drgt_ms_tar","h_dbot_drgt_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dtop_dhgt_ms_tar     = ROOT.TH2F("h_dtop_dhgt_ms_tar","h_dtop_dhgt_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)
    h_dbot_dhgt_ms_tar     = ROOT.TH2F("h_dbot_dhgt_ms_tar","h_dbot_dhgt_ms_tar",80,-0.8, 0.8,80,-0.8, 0.8)

    #Calibrated value vs OGP (reference if provided in config file)
    h_dtop_ms_ogp          = ROOT.TH1F("h_dtop_ms_ogp","h_dtop_ms_ogp"          ,40,-0.5, 0.5)
    h_dbot_ms_ogp          = ROOT.TH1F("h_dbot_ms_ogp","h_dbot_ms_ogp"          ,40,-0.5, 0.5)
    h_drgt_ms_ogp          = ROOT.TH1F("h_drgt_ms_ogp","h_drgt_ms_ogp"          ,40,-0.5, 0.5)
    h_dlft_ms_ogp          = ROOT.TH1F("h_dlft_ms_ogp","h_dlft_ms_ogp"          ,40,-0.5, 0.5)
    h_dhgt_ms_ogp          = ROOT.TH1F("h_dhgt_ms_ogp","h_dhgt_ms_ogp"          ,40,-0.5, 0.5)
    h_dwth_ms_ogp          = ROOT.TH1F("h_dwth_ms_ogp","h_dwth_ms_ogp"          ,40,-0.5, 0.5)
    h_drgt_dlft_ms_ogp     = ROOT.TH2F("h_drgt_dlft_ms_ogp","h_drgt_dlft_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dtop_dlft_ms_ogp     = ROOT.TH2F("h_dtop_dlft_ms_ogp","h_dtop_dlft_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dtop_drgt_ms_ogp     = ROOT.TH2F("h_dtop_drgt_ms_ogp","h_dtop_drgt_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dtop_dbot_ms_ogp     = ROOT.TH2F("h_dtop_dbot_ms_ogp","h_dtop_dbot_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dbot_dlft_ms_ogp     = ROOT.TH2F("h_dbot_dlft_ms_ogp","h_dbot_dlft_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dbot_drgt_ms_ogp     = ROOT.TH2F("h_dbot_drgt_ms_ogp","h_dbot_drgt_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dtop_dhgt_ms_ogp     = ROOT.TH2F("h_dtop_dhgt_ms_ogp","h_dtop_dhgt_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    h_dbot_dhgt_ms_ogp     = ROOT.TH2F("h_dbot_dhgt_ms_ogp","h_dbot_dhgt_ms_ogp",80,-0.5, 0.5,80,-0.5, 0.5)
    
    #Arrays for raw values used in scale factor
    x_top_ogp_rw_cal = [ ]
    x_bot_ogp_rw_cal = [ ]
    x_lft_ogp_rw_cal = [ ]
    x_rgt_ogp_rw_cal = [ ]
    x_hgt_ogp_rw_cal = [ ]
    x_wth_ogp_rw_cal = [ ]

    #----------------Create your histograms in here----------------------
    file_name  = inputfile
    ftmp       = ROOT.TFile.Open(file_name)
    t          = ftmp.Get('tilentuple')
    #Loop over tiles
    for tile in range(0, t.GetEntries()):
        t.GetEntry(tile)
        
        #expected values
        thvalues = [t.top_th,t.bot_th,t.lft_th,t.rgt_th,t.hgt_th,t.wth_th]

        expected = []
        for k in range(0,len(expvalues) ):
            if expvalues[k]!=-1: expected.append(expvalues[k])
            else: expected.append(thvalues[k])  
        #ms vs target  
        top = t.top_ms-thvalues[0]
        bot = t.bot_ms-thvalues[1]
        lft = t.lft_ms-thvalues[2]
        rgt = t.rgt_ms-thvalues[3]
        hgt = t.hgt_ms-thvalues[4]
        wth = t.wth_ms-thvalues[5]
        #ms vs ogp
        mtop = t.top_ms-expected[0]
        mbot = t.bot_ms-expected[1]
        mlft = t.lft_ms-expected[2]
        mrgt = t.rgt_ms-expected[3]
        mhgt = t.hgt_ms-expected[4]
        mwth = t.wth_ms-expected[5]
        #raw vs ogp
        dtop = t.top_rw-expected[0]
        dbot = t.bot_rw-expected[1]
        dlft = t.lft_rw-expected[2]
        drgt = t.rgt_rw-expected[3]
        dhgt = t.hgt_rw-expected[4]
        dwth = t.wth_rw-expected[5]

        #--------------------------Fill Histograms in here--------------------------
        #Comparison versus the target specs
        h_dtop_ms_tar.Fill(top)
        h_dbot_ms_tar.Fill(bot)
        h_dlft_ms_tar.Fill(lft)
        h_drgt_ms_tar.Fill(rgt)
        h_dhgt_ms_tar.Fill(hgt)
        h_dwth_ms_tar.Fill(wth)
        h_dtop_dlft_ms_tar.Fill(top,lft)
        h_drgt_dlft_ms_tar.Fill(rgt,lft)
        h_dtop_drgt_ms_tar.Fill(top,rgt)
        h_dtop_dbot_ms_tar.Fill(top,bot)
        h_dbot_dlft_ms_tar.Fill(bot,lft)
        h_dbot_drgt_ms_tar.Fill(bot,rgt)
        h_dtop_dhgt_ms_tar.Fill(top,hgt)
        h_dbot_dhgt_ms_tar.Fill(bot,hgt)

        #Comparison versus the expected (OGP machine)
        h_dtop_ms_ogp.Fill(mtop)
        h_dbot_ms_ogp.Fill(mbot)
        h_dlft_ms_ogp.Fill(mlft)
        h_drgt_ms_ogp.Fill(mrgt)
        h_dhgt_ms_ogp.Fill(mhgt)
        h_dwth_ms_ogp.Fill(mwth)
        h_dtop_dlft_ms_ogp.Fill(mtop,mlft)
        h_drgt_dlft_ms_ogp.Fill(mrgt,mlft)
        h_dtop_drgt_ms_ogp.Fill(mtop,mrgt)
        h_dtop_dbot_ms_ogp.Fill(mtop,mbot)
        h_dbot_dlft_ms_ogp.Fill(mbot,mlft)
        h_dbot_drgt_ms_ogp.Fill(mbot,mrgt)
        h_dtop_dhgt_ms_ogp.Fill(mtop,mhgt)
        h_dbot_dhgt_ms_ogp.Fill(mbot,mhgt)

        #Append array inputs
        x_top_ogp_rw_cal.append(t.top_rw)
        x_bot_ogp_rw_cal.append(t.bot_rw)
        x_lft_ogp_rw_cal.append(t.lft_rw)
        x_rgt_ogp_rw_cal.append(t.rgt_rw)
        x_hgt_ogp_rw_cal.append(t.hgt_rw)
        x_wth_ogp_rw_cal.append(t.wth_rw)
        #--------------------------Fill Histograms in here--------------------------
    #Close the input your file
    ftmp.Close()

    #Prepare information for scale factor calculation
    x_top,ex_top = meanandstdv(x_top_ogp_rw_cal)
    x_bot,ex_bot = meanandstdv(x_bot_ogp_rw_cal)
    x_lft,ex_lft = meanandstdv(x_lft_ogp_rw_cal)
    x_rgt,ex_rgt = meanandstdv(x_rgt_ogp_rw_cal)
    x_hgt,ex_hgt = meanandstdv(x_hgt_ogp_rw_cal)
    x_wth,ex_wth = meanandstdv(x_wth_ogp_rw_cal)
    p_top  = array( 'f', [ x_top])
    p_bot  = array( 'f', [ x_bot])
    p_lft  = array( 'f', [ x_lft])
    p_rgt  = array( 'f', [ x_rgt])
    p_hgt  = array( 'f', [ x_hgt])
    p_wth  = array( 'f', [ x_wth]) 
    ep_top = array( 'f', [ 0 ])
    ep_bot = array( 'f', [ 0 ])
    ep_lft = array( 'f', [ 0 ])
    ep_rgt = array( 'f', [ 0 ])
    ep_hgt = array( 'f', [ 0 ])
    ep_wth = array( 'f', [ 0 ])
    y_top  = array( 'f', [ float(expected[0])/float(x_top) ])
    y_bot  = array( 'f', [ float(expected[1])/float(x_bot) ])
    y_lft  = array( 'f', [ float(expected[2])/float(x_lft) ])
    y_rgt  = array( 'f', [ float(expected[3])/float(x_rgt) ])
    y_hgt  = array( 'f', [ float(expected[4])/float(x_hgt) ])
    y_wth  = array( 'f', [ float(expected[5])/float(x_wth) ])   
    ey_top = array( 'f', [ (ex_top/x_top) * (expected[0]/x_top) ])
    ey_bot = array( 'f', [ (ex_top/x_bot) * (expected[1]/x_bot) ])
    ey_lft = array( 'f', [ (ex_top/x_lft) * (expected[2]/x_lft) ])
    ey_rgt = array( 'f', [ (ex_top/x_rgt) * (expected[3]/x_rgt) ])
    ey_hgt = array( 'f', [ (ex_top/x_hgt) * (expected[4]/x_hgt) ])
    ey_wth = array( 'f', [ (ex_top/x_wth) * (expected[5]/x_wth) ])
    p_top_ogp_rw_cal  = ROOT.TGraphErrors(1,p_top,y_top,ep_top,ey_top)
    p_bot_ogp_rw_cal  = ROOT.TGraphErrors(1,p_bot,y_bot,ep_bot,ey_bot)
    p_rgt_ogp_rw_cal  = ROOT.TGraphErrors(1,p_rgt,y_rgt,ep_rgt,ey_rgt)
    p_lft_ogp_rw_cal  = ROOT.TGraphErrors(1,p_lft,y_lft,ep_lft,ey_lft)
    p_hgt_ogp_rw_cal  = ROOT.TGraphErrors(1,p_hgt,y_hgt,ep_hgt,ey_hgt)
    p_wth_ogp_rw_cal  = ROOT.TGraphErrors(1,p_wth,y_wth,ep_wth,ey_wth)
    p_top_ogp_rw_cal.SetName("p_top_ogp_rw_cal")
    p_bot_ogp_rw_cal.SetName("p_bot_ogp_rw_cal")
    p_rgt_ogp_rw_cal.SetName("p_rgt_ogp_rw_cal")
    p_lft_ogp_rw_cal.SetName("p_lft_ogp_rw_cal")
    p_hgt_ogp_rw_cal.SetName("p_hgt_ogp_rw_cal")
    p_wth_ogp_rw_cal.SetName("p_wth_ogp_rw_cal")
    tmp.WriteTObject(p_top_ogp_rw_cal)
    tmp.WriteTObject(p_bot_ogp_rw_cal)
    tmp.WriteTObject(p_rgt_ogp_rw_cal)
    tmp.WriteTObject(p_lft_ogp_rw_cal)
    tmp.WriteTObject(p_hgt_ogp_rw_cal)
    tmp.WriteTObject(p_wth_ogp_rw_cal)
    #Close your output file
    tmp.Write()
    tmp.Close()

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config' ,  dest='cfgfile',  help='Name of config file',  required = True)
args            = parser.parse_args()
configfilename  = args.cfgfile
#Set defaults

print "[INFO] Reading skim configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
print "    -The input  directories:"
input_dir_dat    = ast.literal_eval(cfgparser.get("histoconfiguration","input_dir_dat"))
print "      *",input_dir_dat
input_dir_cal    = ast.literal_eval(cfgparser.get("histoconfiguration","input_dir_cal"))
print "      *",input_dir_cal
print "    -The output directory:"
output_dir_dat   = ast.literal_eval(cfgparser.get("histoconfiguration","output_dir_dat"))
print "      *",output_dir_dat
print "    -The output directory:"
output_dir_cal   = ast.literal_eval(cfgparser.get("histoconfiguration","output_dir_cal"))
print "      *",output_dir_cal
data_dat      = ast.literal_eval(cfgparser.get("histoconfiguration","data_dat"))
print "    -The list of data files:"
for x in range(len(data_dat)): print "      *",data_dat[x]
data_cal      = ast.literal_eval(cfgparser.get("histoconfiguration","data_cal"))
print "    -The list of data files:"
for x in range(len(data_cal)): print "      *",data_cal[x]

#Make directories
if not os.path.isdir("histograms"):
   os.makedirs("histograms")
if not os.path.isdir("%s"%output_dir_dat):
   os.makedirs("%s"%output_dir_dat)
if not os.path.isdir("%s"%output_dir_cal):
   os.makedirs("%s"%output_dir_cal)

for k in range(0,len(data_dat) ):
    print "[INFO] Filling histograms for %s.root"%data_dat[k][0]
    inputfilename  = input_dir_dat +"/"+ data_dat[k][0] + ".root"
    outputfilename = output_dir_dat+"/histos_" + data_dat[k][0] + ".root"
    Fill_Histograms(inputfilename,outputfilename,data_dat[k][2],data_dat[k][1])
    print"[INFO] Histogram file histos_"+data_dat[k][0]+".root done"

for k in range(0,len(data_cal) ):
    print "[INFO] Filling histograms for %s.root"%data_cal[k][0]
    inputfilename  = input_dir_cal +"/"+ data_cal[k][0] + ".root"
    outputfilename = output_dir_cal+"/histos_" + data_cal[k][0] + ".root"
    Fill_Histograms(inputfilename,outputfilename,data_cal[k][2],data_cal[k][1])
    print"[INFO] Histogram file histos_"+data_cal[k][0]+".root done"
