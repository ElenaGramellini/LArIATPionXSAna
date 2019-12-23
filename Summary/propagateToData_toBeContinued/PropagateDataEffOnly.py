from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os
import math
from array import array

gStyle.SetOptStat(0)


# Get Truth
effCorr_60_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/TPCEffCorrection/Eff_Correction_60A.root"
effCorr_60 = TFile.Open(effCorr_60_FileName)
effCorr_60XS  = effCorr_60.Get("move_XS_5_60A")
effCorr_60XS.Sumw2()

bkgSub_60_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/BeamlineBkgContributions/bkgFiles/BkgSub_0.152muons_0.148electrons_60A.root"
bkgSub_60 = TFile.Open(bkgSub_60_FileName)
bkgSub_60XS  = bkgSub_60.Get("C_Int_Over_C_Inc_60A")
bkgSub_60XS.Sumw2()

# Get Truth
effCorr_100_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/TPCEffCorrection/Eff_Correction_100A.root"
effCorr_100 = TFile.Open(effCorr_100_FileName)
effCorr_100XS  = effCorr_100.Get("move_XS_5_100A")
effCorr_100XS.Sumw2()


bkgSub_100_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/BeamlineBkgContributions/bkgFiles/BkgSub_0.14muons_0.045electrons_100A.root"
bkgSub_100 = TFile.Open(bkgSub_100_FileName)
bkgSub_100XS  = bkgSub_100.Get("C_Int_Over_C_Inc_100A")
bkgSub_100XS.Sumw2()


f5 = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/WC2TPCEff/applyWC2TPCWeightsToRecoSamples/atanFiles/Data100A_histo.root")
h5 = f5.Get( "XS")
h5.SetMarkerColor(kBlue)
h5.SetLineColor(kBlue)
h5.SetMarkerStyle(22)
h5.SetMarkerSize(.72)
XS100 = h5.Clone("XS100AWeightAndBkgSub")
XS100.Multiply(effCorr_100XS)


f3 = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/WC2TPCEff/applyWC2TPCWeightsToRecoSamples/atanFiles/Data60A_histo.root")
h3 = f3.Get( "XS")
h3.SetMarkerColor(kRed)
h3.SetLineColor(kRed)
h3.SetMarkerStyle(22)
h3.SetMarkerSize(.72)
XS60 = h3.Clone("XS100AWeightAndBkgSub")
XS60.Multiply(effCorr_60XS)


# Get Truth
truth_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/FiveDegreeTruth/Truth.root"
truthF = TFile.Open(truth_FileName)
trueXSAll = truthF.Get("trueXSAll")
trueXSAll.SetLineColor(kGreen-2)




                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",600,600)
c0C.Update()
c0C.SetGrid()
trueXSAll.GetXaxis().SetRangeUser(0,1000)
trueXSAll.GetYaxis().SetRangeUser(0,2)

trueXSAll.Draw("pe")
XS60.Draw("pesame")
XS100.Draw("pesame")         


raw_input()

