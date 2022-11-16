import ROOT
from ROOT import TFile, TTree, TList
import sys
import os
import argparse
import math
import  string
import ast
import glob
from  ConfigParser import *

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def Plot1D(directory,files,histo,tagname):
       #Plot it
       allhistos = []
       #Get gistograms and give them format, collect them in array
       for k in range(0,len(files)):
              #Get histograms
              #print directory+'/'+files[k][0]
              file = ROOT.TFile.Open(directory+'/'+files[k][0])
              tmp  = file.Get(histo[0])
              htmp = tmp.Clone()
              htmp.SetDirectory(0)
              
              #Add format 
              htmp.SetMarkerColor(files[k][2])
              htmp.SetMarkerSize(2)
              htmp.SetMarkerStyle(20)
              htmp.SetLineColor(files[k][2])
              htmp.SetLineWidth(2)

              #Add histos for plotting  
              allhistos.append(htmp)    
              file.Close()

       #Create Canvas
       c1 = ROOT.TCanvas("c1", "c1", 1300, 1300)
       c1.SetFrameLineWidth(4)
       c1.SetBottomMargin (0.15)
       c1.SetRightMargin (0.05)
       c1.SetLeftMargin (0.15)

       #First just a frame to give the format to the plot
       histoframe = ROOT.TH1F("","",allhistos[0].GetNbinsX(),allhistos[0].GetXaxis().GetXmin(), allhistos[0].GetXaxis().GetXmax())
       histoframe.GetYaxis().SetTitleSize(0.050)
       histoframe.GetXaxis().SetTitleSize(0.055)
       histoframe.GetYaxis().SetLabelSize(0.05)
       histoframe.GetXaxis().SetLabelSize(0.05)
       histoframe.GetXaxis().SetLabelOffset(0.010)
       histoframe.GetYaxis().SetTitleOffset(1.5)
       histoframe.GetXaxis().SetTitleOffset(1.1)
       histoframe.GetXaxis().SetTitle(histo[1])
       histoframe.GetYaxis().SetTitle(histo[2])
       histoframe.Draw()
       maxs = []
       for j in range(0,len(allhistos)):  maxs.append(allhistos[j].GetMaximum())
       maxvalue = max(maxs)
       histoframe.SetMaximum(1.3*maxvalue)
       
       #Draw all histograms 
       for k in range(0,len(allhistos)):  allhistos[k].Draw("Histo SAME")

       #Draw a legend
       leg_1 = ROOT.TLegend(0.15,0.75,0.85,0.90)
       leg_1.SetNColumns(2)
       leg_1.SetBorderSize(0)
       leg_1.SetTextSize(0.030)
       leg_1.SetTextFont(42)
       leg_1.SetLineColor(1)
       leg_1.SetLineWidth(10)
       leg_1.SetFillColor(0)
       leg_1.SetFillStyle(0)
       leg_1.Draw()
       for k in range(0,len(allhistos)): leg_1.AddEntry(allhistos[k],"%s"%files[k][1], "p")

       #Add CMS labels
       pt1 = ROOT.TPaveText(0.1863218,0.886316,0.3045977,0.978947,"brNDC")
       pt1.SetBorderSize(0)
       pt1.SetTextAlign(12)
       pt1.SetTextFont(62)
       pt1.SetTextSize(0.05)
       pt1.SetFillColor(0)
       pt1.SetFillStyle(0)
       pt1.AddText("CMS HGCAL SiPM-on-tile")
       pt1.Draw("SAME")
       #Redrawaxis
       histoframe.Draw("SAME AXIS")
       
       #Save plot
       c1.Update()
       c1.SaveAs("plots/%s/plots1d/plot_%s.png"% (tagname,histo[0]) )
       del c1


def Plot2D(directory,files,histo,tagname):
       #Plot it
       allhistos = []
       #Get gistograms and give them format, collect them in array
       for k in range(0,len(files)):
              #Get histograms
              file = ROOT.TFile.Open(directory+'/'+files[k][0])
              tmp  = file.Get(histo[0])
              htmp = tmp.Clone()
              htmp.SetDirectory(0)
              
              #Add format 
              htmp.SetMarkerColor(files[k][2])
              htmp.SetMarkerSize(2)
              htmp.SetMarkerStyle(20)
              htmp.SetLineColor(files[k][2])
              htmp.SetLineWidth(2)

              #Add histos for plotting  
              allhistos.append(htmp)    
              file.Close()

       #Create Canvas
       c1 = ROOT.TCanvas("c1", "c1", 1300, 1300)
       c1.SetFrameLineWidth(4)
       c1.SetBottomMargin (0.15)
       c1.SetRightMargin (0.05)
       c1.SetLeftMargin (0.15)

       #First just a frame to give the format to the plot
       histoframe = ROOT.TH2F("","",allhistos[0].GetNbinsX(),allhistos[0].GetXaxis().GetXmin(), allhistos[0].GetXaxis().GetXmax(),allhistos[0].GetNbinsY(),allhistos[0].GetYaxis().GetXmin(), allhistos[0].GetYaxis().GetXmax())
       histoframe.GetYaxis().SetTitleSize(0.050)
       histoframe.GetXaxis().SetTitleSize(0.055)
       histoframe.GetYaxis().SetLabelSize(0.05)
       histoframe.GetXaxis().SetLabelSize(0.05)
       histoframe.GetXaxis().SetLabelOffset(0.010)
       histoframe.GetYaxis().SetTitleOffset(1.5)
       histoframe.GetXaxis().SetTitleOffset(1.1)
       histoframe.GetXaxis().SetTitle(histo[1])
       histoframe.GetYaxis().SetTitle(histo[2])
       histoframe.Draw()
       maxs = []
       for j in range(0,len(allhistos)):  maxs.append(allhistos[j].GetMaximum())
       maxvalue = max(maxs)
       histoframe.SetMaximum(1.4*maxvalue)
       
       #Draw all histograms 
       for k in range(0,len(allhistos)):  allhistos[k].Draw("SCAT SAME")

       #Draw a legend
       leg_1 = ROOT.TLegend(0.15,0.17,0.85,0.31)
       leg_1.SetNColumns(2)
       leg_1.SetBorderSize(0)
       leg_1.SetTextSize(0.028)
       leg_1.SetTextFont(42)
       leg_1.SetLineColor(1)
       leg_1.SetLineWidth(10)
       leg_1.SetFillColor(0)
       leg_1.SetFillStyle(0)
       leg_1.Draw()
       for k in range(0,len(allhistos)): leg_1.AddEntry(allhistos[k],"%s"%files[k][1], "p")

       #Add CMS labels
       pt1 = ROOT.TPaveText(0.1863218,0.886316,0.3045977,0.978947,"brNDC")
       pt1.SetBorderSize(0)
       pt1.SetTextAlign(12)
       pt1.SetTextFont(62)
       pt1.SetTextSize(0.05)
       pt1.SetFillColor(0)
       pt1.SetFillStyle(0)
       pt1.AddText("CMS HGCAL SiPM-on-tile")
       pt1.Draw("SAME")
       #Redrawaxis
       histoframe.Draw("SAME AXIS")
       
       #Save plot
       c1.Update()
       c1.SaveAs("plots/%s/plots2d/plot_%s.png"% (tagname,histo[0]) )
       del c1

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config' ,  dest='cfgfile',  help='Name of config file',  required = True)
parser.add_argument('--tag'    ,  dest='tag'    ,  help='Name of the default algo folder (e.g. Default)',  required = True)
args            = parser.parse_args()
configfilename  = args.cfgfile
tagname         = args.tag

print "[INFO] Reading configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
input_dir    = ast.literal_eval(cfgparser.get("plotconfiguration","input_dir"))
print "    -The input  directory:"
print "      *",input_dir
output_dir   = ast.literal_eval(cfgparser.get("plotconfiguration","output_dir"))
print "    -The output directory:"
print "      *",output_dir
os.system("mkdir plots")
os.system("mkdir plots/%s"%tagname)

print "[INFO] Reading configuration . . ."

#Files containing the histogram to plot ['Name of file','Legend','Color'] #EDIT FOR MORE
files = [
#            ['histos_Data_1819_1_1_M_0.root',      'NIU-18/19, f1, M, 0',  ROOT.kGreen+1],
#            ['histos_Data_1819_1_2_M_0.root',      'NIU-18/19, f2, M, 0',  ROOT.kRed],
#            ['histos_Data_1819_1_3_M_0.root',      'NIU-18/19, f3, M, 0',  ROOT.kBlue+1],
#            ['histos_Data_1819_1_4_M_0.root',      'NIU-18/19, f4, M, 0',  ROOT.kOrange+1],
#            ['histos_Data_1819_1_5_M_0.root',      'NIU-18/19, f5, M, 0',  ROOT.kViolet],
#            ['histos_Data_1819_1_6_M_0.root',      'NIU-18/19, f6, M, 0',  ROOT.kAzure+1],
#            ['histos_Data_1819_1_7_M_0.root',      'NIU-18/19, f7, M, 0',  ROOT.kPink+1],
#            ['histos_Data_1819_1_8_M_0.root',      'NIU-18/19, f8, M, 0',  ROOT.kBlack],

#            ['histos_Data_1819_1_1_H_0.root',      'NIU-18/19, f1, H, 0',  ROOT.kGreen+1],
#            ['histos_Data_1819_1_2_H_0.root',      'NIU-18/19, f2, H, 0',  ROOT.kRed],
#            ['histos_Data_1819_1_3_H_0.root',      'NIU-18/19, f3, H, 0',  ROOT.kBlue+1],
#            ['histos_Data_1819_1_4_H_0.root',      'NIU-18/19, f4, H, 0',  ROOT.kOrange+1],
#            ['histos_Data_1819_1_5_H_0.root',      'NIU-18/19, f5, H, 0',  ROOT.kViolet],
#            ['histos_Data_1819_1_6_H_0.root',      'NIU-18/19, f6, H, 0',  ROOT.kAzure+1],
#            ['histos_Data_1819_1_7_H_0.root',      'NIU-18/19, f7, H, 0',  ROOT.kPink+1],
#            ['histos_Data_1819_1_8_H_0.root',      'NIU-18/19, f8, H, 0',  ROOT.kBlack],
        ]

#Histograms to plot ['Histogram name in file','X axis label','Y axis label'] ##EDIT FOR MORE
histos_1d = [
    ['h_dtop_ms_th','#Delta_{top} = Observed - Expected (mm)','# of tiles'],
    ['h_dbot_ms_th','#Delta_{bot} = Observed - Expected (mm)','# of tiles'],
    ['h_dlft_ms_th','#Delta_{lft} = Observed - Expected (mm)','# of tiles'],
    ['h_drgt_ms_th','#Delta_{rgt} = Observed - Expected (mm)','# of tiles'],
]

#Histograms to plot ['Histogram name in file','X axis label','Y axis label'] #EDIT FOR MORE
histos_2d = [
    ['h_dtop_drgt','#Delta_{top} (mm)','#Delta_{rgt} (mm)'],
    ['h_dtop_dlft','#Delta_{top} (mm)','#Delta_{lft} (mm)'],
    ['h_dtop_dbot','#Delta_{top} (mm)','#Delta_{bot} (mm)'],
    ['h_dbot_drgt','#Delta_{bot} (mm)','#Delta_{rgt} (mm)'],
    ['h_dbot_dlft','#Delta_{bot} (mm)','#Delta_{lft} (mm)'],
    ['h_drgt_dlft','#Delta_{rgt} (mm)','#Delta_{lft} (mm)'],
]

#Plot 1d distributions
os.system("mkdir plots/%s"%tagname)
os.system("mkdir plots/%s/plots1d/"%tagname)
#loop over the 1d histograms you want to compare
print "[INFO] Plotting 1d distributions . . ."
for histo in histos_1d: Plot1D(input_dir+"/"+tagname,files,histo,tagname)

#Plot 2d distributions
os.system("mkdir plots/%s"%tagname)
os.system("mkdir plots/%s/plots2d/"%tagname)
#loop over the 2d histograms you want to compare
print "[INFO] Plotting 2d distributions . . ."
for histo in histos_2d: Plot2D(input_dir+"/"+tagname,files,histo,tagname)



