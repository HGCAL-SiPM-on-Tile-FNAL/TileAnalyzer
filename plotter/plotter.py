import ROOT
from ROOT import TFile, TTree, TList
import sys
import os
import argparse
import math

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

def Plot1D(directory,files,histo):
       #Plot it
       allhistos = []
       #Get gistograms and give them format, collect them in array
       for k in range(0,len(files)):
              #Get histograms
              print directory+'/'+files[k][0]
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
       leg_1 = ROOT.TLegend(0.25,0.75,0.85,0.90)
       leg_1.SetNColumns(3)
       leg_1.SetBorderSize(0)
       leg_1.SetTextSize(0.030)
       leg_1.SetTextFont(42)
       leg_1.SetLineColor(1)
       leg_1.SetLineWidth(10)
       leg_1.SetFillColor(0)
       leg_1.SetFillStyle(0)
       leg_1.Draw()
       for k in range(0,len(allhistos)): leg_1.AddEntry(allhistos[k],"%s"%files[k][1], "l")

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
       c1.SaveAs("plots1d/plot_%s.png"%histo[0])
       c1.SaveAs("plots1d/plot_%s.pdf"%histo[0])
       del c1


def Plot2D(directory,files,histo):
       #Plot it
       allhistos = []
       #Get gistograms and give them format, collect them in array
       for k in range(0,len(files)):
              #Get histograms
              print directory+'/'+files[k][0]
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
       histoframe.SetMaximum(1.3*maxvalue)
       
       #Draw all histograms 
       for k in range(0,len(allhistos)):  allhistos[k].Draw("SCAT SAME")

       #Draw a legend
       leg_1 = ROOT.TLegend(0.25,0.75,0.85,0.90)
       leg_1.SetNColumns(3)
       leg_1.SetBorderSize(0)
       leg_1.SetTextSize(0.030)
       leg_1.SetTextFont(42)
       leg_1.SetLineColor(1)
       leg_1.SetLineWidth(10)
       leg_1.SetFillColor(0)
       leg_1.SetFillStyle(0)
       leg_1.Draw()
       for k in range(0,len(allhistos)): leg_1.AddEntry(allhistos[k],"%s"%files[k][1], "l")

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
       c1.SaveAs("plots2d/plot_%s.png"%histo[0])
       c1.SaveAs("plots2d/plot_%s.pdf"%histo[0])
       del c1

print "[INFO] Reading configuration . . ."

directory   = 'histograms'

#Files containing the histogram to plot ['Name of file','Legend','Color'] #EDIT FOR MORE
files = [
            ['histos_DESY_May23.root',          'DESY May 23',        ROOT.kRed],
            ['histos_calibration_May23.root',   'Calibration May 23',  ROOT.kAzure],
        ]

#Histograms to plot ['Histogram name in file','X axis label','Y axis label'] ##EDIT FOR MORE
histos_1d = [
    ['h_top_ms_top_th','Top: measured-theoretical (mm)','# of tiles'],
]

#Histograms to plot ['Histogram name in file','X axis label','Y axis label'] #EDIT FOR MORE
histos_2d = [
    ['h_dtop_vs_dbot','Top: measured-theoretical (mm)','Bottom: measured-theoretical (mm)'],
]

#Plot 1d distributions
os.system("mkdir plots1d")
#loop over the 1d histograms you want to compare
print "[INFO] Plotting 1d distributions . . ."
for histo in histos_1d: Plot1D(directory,files,histo)

#Plot 2d distributions
os.system("mkdir plots2d")
#loop over the 2d histograms you want to compare
print "[INFO] Plotting 2d distributions . . ."
for histo in histos_2d: Plot2D(directory,files,histo)