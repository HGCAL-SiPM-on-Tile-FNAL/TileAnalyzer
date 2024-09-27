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

def PlotFit(directory,files,histo,tagname):
       #Plot it
       print histo
       allhistos = []
       #Get gistograms and give them format, collect them in array
       for k in range(0,len(files)):
              #Get histograms
              file = ROOT.TFile.Open(directory+'/'+files[k][0])
              tmp  = file.Get(histo[0])
              print histo[0]
              htmp = tmp.Clone()
              #htmp.SetDirectory(0)
              
              #Add format 
              htmp.SetMarkerColor(files[k][2])
              htmp.SetMarkerSize(1)
              htmp.SetMarkerStyle(20)
              htmp.SetLineColor(files[k][2])
              htmp.SetLineWidth(2)

              #Add histos for plotting  
              allhistos.append(htmp)    
              file.Close()

       #Make a joined graph a fit it
       gr = ROOT.TGraphAsymmErrors() 
       ipt=0
       means = []
       for h in allhistos:
          gr.SetPoint(ipt, h.GetX()[0],h.GetY()[0])
          gr.SetPointError(ipt, 0,0,h.GetErrorY(1),h.GetErrorY(1))
          ipt+=1
       gr.Fit("pol1","","",40,60) #24-36 #32-40 #40-60
       gr.SetMarkerSize(1)
       gr.SetMarkerStyle(21)
       gr.SetLineWidth(2)
       gr.SetMarkerColor(ROOT.kBlue)
       gr.SetLineColor(ROOT.kBlack)
       f = gr.GetFunction("pol1")
       f.SetLineColor(ROOT.kBlack)

       #Create Canvas
       c1 = ROOT.TCanvas("c1", "c1", 1300, 1300)
       c1.SetFrameLineWidth(4)
       c1.SetBottomMargin (0.15)
       c1.SetRightMargin (0.05)
       c1.SetLeftMargin (0.20)

       #First just a frame to give the format to the plot
       histoframe = ROOT.TH1F("","",100,20,60)
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
       histoframe.SetMaximum(1.04)
       histoframe.SetMinimum(0.98)           
       
       #Draw all histograms 
       for k in range(0,len(allhistos)):  allhistos[k].Draw("P SAME")

       #Draw fit
       f.Draw("same")
       #Draw a legend
       leg_1 = ROOT.TLegend(0.20,0.17+0.55,0.85,0.31+0.55)
       leg_1.SetNColumns(2)
       leg_1.SetBorderSize(0)
       leg_1.SetTextSize(0.028)
       leg_1.SetTextFont(42)
       leg_1.SetLineColor(1)
       leg_1.SetLineWidth(10)
       leg_1.SetFillColor(0)
       leg_1.SetFillStyle(0)
       leg_1.Draw()
       for k in range(0,len(allhistos)): leg_1.AddEntry(allhistos[k],"%s"%files[k][1], "pe")
       leg_1.AddEntry(f,"Fit (y = %.5f x + %.5f)"%(f.GetParameter(1),f.GetParameter(0)),"l")

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
       c1.SaveAs("plots/%s/plotscal/plot_%s.png"% (tagname,histo[0]) )
       del c1

#Get input/output information
parser = argparse.ArgumentParser(description='Command line parser of skim options')
parser.add_argument('--config' ,  dest='cfgfile',  help='Name of config file',  required = True)
args            = parser.parse_args()
configfilename  = args.cfgfile

print "[INFO] Reading configuration file . . ."
cfgparser = ConfigParser()
cfgparser.read('%s'%configfilename)
input_dir    = ast.literal_eval(cfgparser.get("calconfiguration","input_dir"))
print "    -The input  directory:"
print "      *",input_dir
output_dir   = ast.literal_eval(cfgparser.get("calconfiguration","output_dir"))
print "    -The output directory:"
print "      *",output_dir
module_ring   = ast.literal_eval(cfgparser.get("calconfiguration","module_ring"))
print "    -The module ring:"
print "      *",module_ring
fit_range     = ast.literal_eval(cfgparser.get("calconfiguration","fit_range"))
print "    -The fit range: %i,%i"%(fit_range[0],fit_range[1])
print "[INFO] Reading configuration . . ."

#Files containing the histogram to plot ['Name of file','Legend','Color'] #EDIT FOR MORE
files = [
            ['histos_Data_bare_T3435_OGP_1.root'  , 'Bare-34/35 (OGP1)',  ROOT.kRed+3,True],
            ['histos_Data_bare_T3637_OGP_1.root'  , 'Bare-36/37 (OGP1)',  ROOT.kBlue+3,True],
            ['histos_Data_bare_T3839_OGP_1.root'  , 'Bare-38/39 (OGP1)',  ROOT.kGreen+3,True],
            ['histos_Data_bare_T4041_OGP_1.root'  , 'Bare-40/41 (OGP1)',  ROOT.kOrange+3,True],
]

points_1d = [
    ['p_top_ogp_rw_cal','Top_{PnP} [mm]'   ,'SF_{Top}    = Top_{OGP} / Top_{PnP}'       ],
    ['p_bot_ogp_rw_cal','Bottom_{PnP} [mm]','SF_{Bottom} = Bottom_{OGP} / Bottom_{PnP}' ],
    ['p_lft_ogp_rw_cal','Left_{PnP} [mm]'  ,'SF_{Left}   = Left_{OGP} / Left_{PnP}'     ],
    ['p_rgt_ogp_rw_cal','Right_{PnP} [mm]' ,'SF_{Right}  = Right_{OGP} / Right_{PnP}'   ],
    ['p_hgt_ogp_rw_cal','Height_{PnP} [mm]','SF_{Height} = Height_{OGP} / Height_{PnP}' ],
    ['p_wth_ogp_rw_cal','Width_{PnP} [mm]' ,'SF_{Width}  = Width_{OGP} / Width_{PnP}'   ],
]

#Make directories
if not os.path.isdir("plots"):
   os.makedirs("plots")
if not os.path.isdir("plots/%s/plotscal"%module_ring):
   os.makedirs("plots/%s/plotscal"%module_ring)

#loop over the 2d histograms you want to compare
print "[INFO] Plotting fits . . ."
for histo in points_1d: PlotFit(input_dir,files,histo,module_ring)