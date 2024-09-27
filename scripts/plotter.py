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
              htmp.SetMarkerSize(0)
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
       histoframe.GetYaxis().SetLabelSize(0.035)
       histoframe.GetXaxis().SetLabelSize(0.035)
       histoframe.GetXaxis().SetLabelOffset(0.010)
       histoframe.GetYaxis().SetTitleOffset(1.5)
       histoframe.GetXaxis().SetTitleOffset(1.1)
       histoframe.GetXaxis().SetTitle(histo[1])
       histoframe.GetYaxis().SetTitle(histo[2])
       histoframe.Draw()
       maxs = []
       for j in range(0,len(allhistos)):  maxs.append(allhistos[j].GetMaximum())
       maxvalue = max(maxs)
       histoframe.SetMaximum(1.5*maxvalue)
       
       #Draw (True) tolerance bars for wrapped (true) or unwrapped (false)
       if histo[3]==True:
             if files[0][3]==True:
                      box = ROOT.TBox(0.2,0,0.6,maxvalue*1.1)
                      box.SetFillColorAlpha(ROOT.kGray,0.8)
                      box.SetLineColor(ROOT.kGray)
                      box.SetFillStyle(3144)
                      box.Draw("SAME")
             else:
                      box = ROOT.TBox(-0.1,0,0,maxvalue*1.1)
                      box.SetFillColorAlpha(ROOT.kGray,0.8)
                      box.SetLineColor(ROOT.kGray)
                      box.SetFillStyle(3144)
                      box.Draw("SAME")
       #Draw all histograms 
       for k in range(0,len(allhistos)):  allhistos[k].Draw("Histo SAME")

       #Draw a legend
       leg_1 = ROOT.TLegend(0.17,0.75,0.90,0.90)
       leg_1.SetNColumns(4)
       leg_1.SetBorderSize(0)
       leg_1.SetTextSize(0.02)
       leg_1.SetTextFont(42)
       leg_1.SetLineColor(1)
       leg_1.SetLineWidth(10)
       leg_1.SetFillColor(0)
       leg_1.SetFillStyle(0)
       leg_1.Draw()
       for k in range(0,len(allhistos)): leg_1.AddEntry(allhistos[k],"%s"%files[k][1], "l")
       if histo[3]==True: leg_1.AddEntry(box,"Tolerance", "f")

       #Add CMS labels
       pt1 = ROOT.TPaveText(0.1863218,0.886316,0.4045977,0.978947,"brNDC")
       pt1.SetBorderSize(0)
       pt1.SetTextAlign(12)
       pt1.SetTextFont(62)
       pt1.SetTextSize(0.05)
       pt1.SetFillColor(0)
       pt1.SetFillStyle(0)
#       pt1.AddText("w240321 Size 34-35 CMS HGCAL SiPM-on-tile")                           # title                             
#       pt1.AddText("v240807b_M40_PNP")                              # title
       pt1.AddText("CMS HGCAL SiPM-on-tile")                              # title
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
              #if k==0: htmp.SetMarkerColor(ROOT.kBlack)
              #else: htmp.SetMarkerColor(files[k][2])
              htmp.SetMarkerColor(files[k][2])
              htmp.SetMarkerSize(1)
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
       c1.SetLeftMargin (0.20)

       #First just a frame to give the format to the plot
       histoframe = ROOT.TH2F("","",allhistos[0].GetNbinsX(),allhistos[0].GetXaxis().GetXmin(), allhistos[0].GetXaxis().GetXmax(),allhistos[0].GetNbinsY(),allhistos[0].GetYaxis().GetXmin(), allhistos[0].GetYaxis().GetXmax())
       histoframe.GetYaxis().SetTitleSize(0.050)
       histoframe.GetXaxis().SetTitleSize(0.055)
       histoframe.GetYaxis().SetLabelSize(0.035)
       histoframe.GetXaxis().SetLabelSize(0.035)
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


       #Draw tolerance bars
       if histo[3]==True:
             if files[k][3]==True:
                    box = ROOT.TBox(0,0,0.6,0.6)
                    box.SetFillColorAlpha(ROOT.kGray,0.8)
                    box.SetLineColor(ROOT.kGray)
                    box.SetFillStyle(3144)
                    box.Draw("SAME")
             else:
                    box = ROOT.TBox(-0.1,-0.1,0,0)
                    box.SetFillColorAlpha(ROOT.kGray,0.8)
                    box.SetLineColor(ROOT.kGray)
                    box.SetFillStyle(3144)
                    box.Draw("SAME")             
       
       #Draw all histograms 
       for k in range(0,len(allhistos)):  allhistos[k].Draw("SCAT SAME")

       #Draw a legend
       leg_1 = ROOT.TLegend(0.20,0.17,0.85,0.31)
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
       if histo[3]==True: leg_1.AddEntry(box,"Tolerance", "f")

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
args            = parser.parse_args()
configfilename  = args.cfgfile

print "[INFO] Reading configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
input_dir    = ast.literal_eval(cfgparser.get("plotconfiguration","input_dir"))
print "    -The input  directory:"
print "      *",input_dir
output_dir   = ast.literal_eval(cfgparser.get("plotconfiguration","output_dir"))
print "    -The output directory:"
print "      *",output_dir
module_ring   = ast.literal_eval(cfgparser.get("plotconfiguration","module_ring"))
print "    -The module ring:"
print "      *",module_ring

print "[INFO] Reading configuration . . ."

#Files containing the histogram to plot ['Name of file','Legend','Color','Wrapped (True) or Bare (False)'] #EDIT FOR MORE
files = [
           ['histos_Data_bare_T3435_C1.root'  , 'T3435-C1',  ROOT.kBlack,   False],
           ['histos_Data_bare_T3637_C1.root'  , 'T3637-C1',  ROOT.kGray+2,  False], 
           ['histos_Data_bare_T3839_C1.root'  , 'T3839-C1',  ROOT.kRed,     False], 
           ['histos_Data_bare_T4041_C1.root'  , 'T4041-C1',  ROOT.kMagenta, False], 
           ['histos_Data_bare_T3435_C2.root'  , 'T3435-C2',  ROOT.kBlue,    False], 
           ['histos_Data_bare_T3637_C2.root'  , 'T3637-C2',  ROOT.kBlue-7,  False],  
           ['histos_Data_bare_T3839_C2.root'  , 'T3839-C2',  ROOT.kGreen+2, False], 
           ['histos_Data_bare_T4041_C2.root'  , 'T4041-C2',  ROOT.kGreen,   False],  
]

#Histograms to plot ['Histogram name in file','X axis label','Y axis label',Draw tolerance] ##EDIT FOR MORE
histos_1d = [
    ['h_dtop_ms_tar','Top_{PnP} - Top_{Target} [mm]','# of tests'      ,True ],
    ['h_dbot_ms_tar','Bottom_{PnP} - Bottom_{Target} [mm]','# of tests',True ],
    ['h_dlft_ms_tar','Left_{PnP} - Left_{Target} [mm]'  ,'# of tests'  ,True ],
    ['h_drgt_ms_tar','Right_{PnP} - Right_{Target} [mm]' ,'# of tests' ,True ],
    ['h_dhgt_ms_tar','Height_{PnP} - Height_{Target} [mm]','# of tests',True ],
    ['h_dwth_ms_tar','Width_{PnP} - Width_{Target} [mm]' ,'# of tests' ,True ],
    ['h_dtop_ms_ogp','Top_{PnP} - Top_{OGP} [mm]','# of tiles'         ,False],
    ['h_dbot_ms_ogp','Bottom_{PnP} - Bottom_{OGP} [mm]','# of tiles'   ,False],
    ['h_dlft_ms_ogp','Left_{PnP} - Left_{OGP} [mm]'  ,'# of tiles'     ,False],
    ['h_drgt_ms_ogp','Right_{PnP} - Right_{OGP} [mm]' ,'# of tiles'    ,False],
    ['h_dhgt_ms_ogp','Height_{PnP} - Height_{OGP} [mm]','# of tiles'   ,False],
    ['h_dwth_ms_ogp','Width_{PnP} - Width_{OGP} [mm]' ,'# of tiles'    ,False],
]

#Histograms to plot ['Histogram name in file','X axis label','Y axis label','Draw Tolerance (True)'] #EDIT FOR MORE
histos_2d = [
    ['h_dtop_drgt_ms_tar','Top_{PnP} - Top_{Target} [mm]'       ,'Right_{PnP} - Right_{Target} [mm]'  ,True],
    ['h_dtop_dlft_ms_tar','Top_{PnP} - Top_{Target} [mm]'       ,'Left_{PnP} - Left_{Target} [mm])'   ,True],
    ['h_dtop_dbot_ms_tar','Top_{PnP} - Top_{Target} [mm]'       ,'Bottom_{PnP} - Bottom_{Target} [mm]',True],
    ['h_dbot_drgt_ms_tar','Bottom_{PnP} - Bottom_{Target} [mm]' ,'Right_{PnP} - Right_{Target} [mm]'  ,True],
    ['h_dbot_dlft_ms_tar','Bottom_{PnP} - Bottom_{Target} [mm]' ,'Left_{PnP} - Left_{Target} [mm]'    ,True],
    ['h_drgt_dlft_ms_tar','Right_{PnP} - Right_{Target} [mm]'   ,'Left_{PnP} - Left_{Target} [mm]'    ,True],
    ['h_dtop_dhgt_ms_tar','Top_{PnP} - Top_{Target} [mm]'       ,'Height_{PnP} - Height_{Target} [mm]',True],
    ['h_dbot_dhgt_ms_tar','Bottom_{PnP} - Bottom_{Target} [mm]' ,'Height_{PnP} - Height_{Target} [mm]',True],
    ['h_dtop_drgt_ms_ogp','Top_{PnP} - Top_{OGP} [mm]'       ,'Right_{PnP} - Right_{OGP} [mm]'        ,False],
    ['h_dtop_dlft_ms_ogp','Top_{PnP} - Top_{OGP} [mm]'       ,'Left_{PnP} - Left_{OGP} [mm])'         ,False],
    ['h_dtop_dbot_ms_ogp','Top_{PnP} - Top_{OGP} [mm]'       ,'Bottom_{PnP} - Bottom_{OGP} [mm]'      ,False],
    ['h_dbot_drgt_ms_ogp','Bottom_{PnP} - Bottom_{OGP} [mm]' ,'Right_{PnP} - Right_{OGP} [mm]'        ,False],
    ['h_dbot_dlft_ms_ogp','Bottom_{PnP} - Bottom_{OGP} [mm]' ,'Left_{PnP} - Left_{OGP} [mm]'          ,False],
    ['h_drgt_dlft_ms_ogp','Right_{PnP} - Right_{OGP} [mm]'   ,'Left_{PnP} - Left_{OGP} [mm]'          ,False],
    ['h_dtop_dhgt_ms_ogp','Top_{PnP} - Top_{OGP} [mm]'       ,'Height_{PnP} - Height_{OGP} [mm]'      ,False],
    ['h_dbot_dhgt_ms_ogp','Bottom_{PnP} - Bottom_{OGP} [mm]' ,'Height_{PnP} - Height_{OGP} [mm]'      ,False],
]

#Make directories
if not os.path.isdir("plots"):
   os.makedirs("plots")
if not os.path.isdir("plots/%s"%module_ring):
   os.makedirs("plots/%s"%module_ring)
if not os.path.isdir("plots/%s/plots1d"%module_ring):
   os.makedirs("plots/%s/plots1d"%module_ring)
if not os.path.isdir("plots/%s/plots2d"%module_ring):
   os.makedirs("plots/%s/plots2d"%module_ring)

#loop over the 1d histograms you want to compare
print "[INFO] Plotting 1d distributions . . ."
for histo in histos_1d: Plot1D(input_dir,files,histo,module_ring)

#loop over the 2d histograms you want to compare
print "[INFO] Plotting 2d distributions . . ."
for histo in histos_2d: Plot2D(input_dir,files,histo,module_ring)
