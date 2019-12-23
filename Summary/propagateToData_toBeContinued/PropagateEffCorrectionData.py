from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os
import math
from array import array

gStyle.SetOptStat(0)


# Get Truth
effCorr_60_FileName = "Eff_Correction_60A.root"
effCorr_60 = TFile.Open(effCorr_60_FileName)
effCorr_60XS  = effCorr_60.Get("move_XS_5_60A")
effCorr_60XS.Sumw2()

# Get Truth
effCorr_100_FileName = "Eff_Correction_100A.root"
effCorr_100 = TFile.Open(effCorr_100_FileName)
effCorr_100XS  = effCorr_100.Get("move_XS_5_100A")
effCorr_100XS.Sumw2()



f5 = TFile("../Data100A_histo.root")
h5 = f5.Get( "XS")
h5.SetMarkerColor(kBlue)
h5.SetLineColor(kBlue)
h5.SetMarkerStyle(22)
h5.SetMarkerSize(.72)
XS100 = h5.Clone("XS100AWeightAndCorrected")
XS100.Multiply(effCorr_100XS)

f3 = TFile("../Data60A_histo.root")
h3 = f3.Get( "XS")
h3.SetMarkerColor(kRed)
h3.SetLineColor(kRed)
h3.SetMarkerStyle(22)
h3.SetMarkerSize(.72)
XS60 = h3.Clone("XS60AWeightAndCorrected")
XS60.Multiply(effCorr_60XS)

                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",600,600)
c0C.Update()
c0C.SetGrid()
XS60.GetXaxis().SetRangeUser(0,1000)
XS60.GetYaxis().SetRangeUser(0,2)

XS60.Draw("pe")
XS100.Draw("pesame")         

outFile = TFile("MCRecoData.root","recreate")
outFile.cd()

XS60 .Write() 
XS100 .Write() 

outFile.Write()
outFile.Close()

raw_input()

