from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os


gStyle.SetOptStat(0)

'''
outFileName = "Eff_Correction_60A.root"
########################################################################
########################    MC Part   ##################################
########################################################################
# Get Monte Carlo files
pionMC_FileName = "AngleCut_5deg_histo_60A.root"
pionMC_File   = TFile.Open(pionMC_FileName)
# Get Interacting and Incident plot
pionMC_Int  = pionMC_File.Get("hInteractingKE")
pionMC_Inc  = pionMC_File.Get("hIncidentKE")
pionMC_Int.Sumw2()
pionMC_Inc.Sumw2()
pionMC_Int.SetLineColor(kBlack)
pionMC_Int.Divide(pionMC_Inc)
pionMC_Int.Scale(101.)
'''

g4FileT = TFile.Open("Truth.root")
hTrueTrue = g4FileT.Get("trueXSAll")

# Get Truth
pionTrue_60_FileName = "/Users/elenag/Documents/Papers/ThatsIt/rootFiles/MC60APionsReco_histo.root"
pionTrue_60 = TFile.Open(pionTrue_60_FileName)
pionTrue_60_Int  = pionTrue_60.Get("TrueXS/hInteractingKE")
pionTrue_60_Inc  = pionTrue_60.Get("TrueXS/hIncidentKE")
pionTrue_60_Int.Sumw2()
pionTrue_60_Inc.Sumw2()
pionTrue_60_Int.SetLineColor(kRed)
pionTrue_60_Int.Divide(pionTrue_60_Inc)
pionTrue_60_Int.Scale(101.)
# Get Truth
pionTrue_100_FileName = "/Users/elenag/Documents/Papers/ThatsIt/rootFiles/MC100APionsReco_histo.root"
pionTrue_100 = TFile.Open(pionTrue_100_FileName)
pionTrue_100_Int  = pionTrue_100.Get("TrueXS/hInteractingKE")
pionTrue_100_Inc  = pionTrue_100.Get("TrueXS/hIncidentKE")
pionTrue_100_Int.Sumw2()
pionTrue_100_Inc.Sumw2()
pionTrue_100_Int.SetLineColor(kBlue)
pionTrue_100_Int.Divide(pionTrue_100_Inc)
pionTrue_100_Int.Scale(101.)




## Refine for bins which are low in Statistics
for i in xrange(1,pionTrue_60_Int.GetSize()-2):
    if pionTrue_60_Int.GetBinCenter(i) < 1. or pionTrue_60_Int.GetBinCenter(i) > 524.:
        pionTrue_60_Int.SetBinContent(i, -1)


trueXSAll = pionTrue_60_Int.Clone("trueXSAll")
trueXSAll.SetLineWidth(2)
for i in xrange(1,pionTrue_100_Int.GetSize()-2):
    if pionTrue_100_Int.GetBinCenter(i) < 176. or pionTrue_100_Int.GetBinCenter(i) > 1001.:
        pionTrue_100_Int.SetBinContent(i, -1)
    elif pionTrue_60_Int.GetBinCenter(i) > 524. :
        trueXSAll.SetBinContent(i, pionTrue_100_Int.GetBinContent(i))
        trueXSAll.SetBinError(i, pionTrue_100_Int.GetBinError(i))
    else:
        trueXSAll.SetBinContent(i, (pionTrue_60_Int.GetBinContent(i) + pionTrue_100_Int.GetBinContent(i))/2.  )
        trueXSAll.SetBinError  (i, TMath.Sqrt(pionTrue_60_Int.GetBinError(i)*pionTrue_60_Int.GetBinError(i)  + pionTrue_100_Int.GetBinError(i)*pionTrue_100_Int.GetBinError(i) )  )

trueXSAll.SetLineColor(kGreen-2)
                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",600,600)
c0C.Update()
c0C.SetGrid()
pionTrue_60_Int.GetXaxis().SetRangeUser(0,1000)
pionTrue_60_Int.GetYaxis().SetRangeUser(0,2)

hTrueTrue.Draw("pe")
pionTrue_60_Int.Draw("pesame")
pionTrue_100_Int.Draw("pesame")         


raw_input()

