import ROOT
from ROOT import TFile, TTree, TList
import sys
import os
import argparse
import math
import ast
import glob
from  ConfigParser import *

def Fill_Histograms(inputfile,outputfile):
    #Create outputfile    
    tmp = ROOT.TFile.Open(outputfile,'RECREATE')
    #----------------Create your histograms in here --------------------------
    h_dtop_ms_th    = ROOT.TH1F("h_dtop_ms_th","h_dtop_ms_th",20,-0.5,0.5)
    h_dbot_ms_th    = ROOT.TH1F("h_dbot_ms_th","h_dbot_ms_th",20,-0.5,0.5)
    h_drgt_ms_th    = ROOT.TH1F("h_drgt_ms_th","h_drgt_ms_th",20,-0.5,0.5)
    h_dlft_ms_th    = ROOT.TH1F("h_dlft_ms_th","h_dlft_ms_th",20,-0.5,0.5)
    h_drgt_dlft     = ROOT.TH2F("h_drgt_dlft","h_drgt_dlft",2000,-0.5,0.5,2000,-0.5,0.5)
    h_dtop_dlft     = ROOT.TH2F("h_dtop_dlft","h_dtop_dlft",2000,-0.5,0.5,2000,-0.5,0.5)
    h_dtop_drgt     = ROOT.TH2F("h_dtop_drgt","h_dtop_drgt",2000,-0.5,0.5,2000,-0.5,0.5)
    h_dtop_dbot     = ROOT.TH2F("h_dtop_dbot","h_dtop_dbot",2000,-0.5,0.5,2000,-0.5,0.5)
    h_dbot_dlft     = ROOT.TH2F("h_dbot_dlft","h_dbot_dlft",2000,-0.5,0.5,2000,-0.5,0.5)
    h_dbot_drgt     = ROOT.TH2F("h_dbot_drgt","h_dbot_drgt",2000,-0.5,0.5,2000,-0.5,0.5)

    #----------------Create your histograms in here--------------------------
    file_name  = inputfile
    ftmp       = ROOT.TFile.Open(file_name)
    t          = ftmp.Get('tilentuple')
    #Loop over tiles
    for tile in range(0, t.GetEntries()):
        t.GetEntry(tile)
        dtop = t.top_ms-t.top_th
        dbot = t.bot_ms-t.bot_th
        dlft = t.lft_ms-t.lft_th
        drgt = t.rgt_ms-t.rgt_th
        #--------------------------Fill Histograms in here--------------------------
        h_dtop_ms_th.Fill(dtop)
        h_dbot_ms_th.Fill(dbot)
        h_dlft_ms_th.Fill(dlft)
        h_drgt_ms_th.Fill(drgt)
        h_dtop_dlft.Fill(dtop,dlft)
        h_drgt_dlft.Fill(drgt,dlft)
        h_dtop_drgt.Fill(dtop,drgt)
        h_dtop_dbot.Fill(dtop,dbot)
        h_dbot_dlft.Fill(dbot,dlft)
        h_dbot_drgt.Fill(dbot,drgt)
        #--------------------------Fill Histograms in here--------------------------
    #Close the input your file
    ftmp.Close()
    #Close your output file
    tmp.Write()
    tmp.Close()

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config' ,  dest='cfgfile',  help='Name of config file',  required = True)
parser.add_argument('--tag'    ,  dest='tag'    ,  help='Name of the default algo folder (e.g. Default)',  required = True)
args            = parser.parse_args()
configfilename  = args.cfgfile
tagname         = args.tag
#Set defaults

print "[INFO] Reading skim configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
input_dir    = ast.literal_eval(cfgparser.get("histoconfiguration","input_dir"))
print "    -The input  directory:"
print "      *",input_dir
output_dir   = ast.literal_eval(cfgparser.get("histoconfiguration","output_dir"))
print "    -The output directory:"
print "      *",output_dir
datas      = ast.literal_eval(cfgparser.get("histoconfiguration","datas"))
print "    -The list of data files:"
for x in range(len(datas)): print "      *",datas[x]
os.system("mkdir histograms")
os.system("mkdir histograms/%s"%tagname)

for data in datas:
    print "[INFO] Filling histograms for %s.root"%data
    inputfilename  = input_dir +"/"+tagname + "/" + data + ".root"
    outputfilename = output_dir+"/"+tagname + "/histos_" + data + ".root"
    Fill_Histograms(inputfilename,outputfilename)
    print"[INFO] Histogram file histos_"+data+".root done"