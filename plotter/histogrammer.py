import ROOT
from ROOT import TFile, TTree, TList
import sys
import os
import argparse
import math

def Fill_Histograms(inputfile,outputfile):
    os.system("mkdir histograms")
    #Create outputfile    
    tmp = ROOT.TFile.Open("histograms/%s"%outputfile,'RECREATE')
    #----------------Create your histograms in here --------------------------
    h_top_ms_top_th= ROOT.TH1F("h_top_ms_top_th","h_top_ms_top_th",2000,-1,1)
    h_dtop_vs_dbot = ROOT.TH2F("h_dtop_vs_dbot","h_dtop_vs_dbot",  2000,-1,1,2000,-1,1)
    #----------------Create your histograms in here--------------------------
    file_name  = inputfile
    ftmp       = ROOT.TFile.Open(file_name)
    t          = ftmp.Get('tilentuple')
    #Loop over tiles
    for tile in range(0, t.GetEntries()):
        t.GetEntry(tile)
        #--------------------------Fill Histograms in here--------------------------
        h_top_ms_top_th.Fill(t.top_ms-t.top_th)
        h_dtop_vs_dbot.Fill(t.top_ms-t.top_th,t.bot_ms-t.bot_th)
        #--------------------------Fill Histograms in here--------------------------
    #Close the input your file
    ftmp.Close()
    #Close your output file
    tmp.Write()
    tmp.Close()

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--inputfile' ,  dest='inputfile',   help='Name of input file',  required = True)
parser.add_argument('--outputfile' ,  dest='outputfile',   help='Name of output file',  required = True)
args             = parser.parse_args()
inputfilename    = args.inputfile
outputfilename   = args.outputfile
#Set defaults

print("[INFO] Reading root file")
#create histogram directory
print("...Filling histograms from "+inputfilename)
Fill_Histograms(inputfilename,outputfilename)
print ("[INFO] Histogram file "+outputfilename+" done")