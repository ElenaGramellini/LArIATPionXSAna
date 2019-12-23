from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os
import math
from array import array

gStyle.SetOptStat(0)
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
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

def graphTruth():
    fname   = "PionMinusG4.txt"
    kineticEnergy = []
    crossSec      = []
    crossSec_el   = []
    crossSec_inel = []
    zero          = []

    title = ""
    with open(fname) as f:
        for fLine in f.readlines():
            w = fLine.split()
            if is_number(w[0]):
                runIn    = int(w[0])
                ke       = float(w[1])
                xstot       = float(w[4])
                kineticEnergy.append(ke)
                crossSec.append(xstot)
                zero.append(0.)
            else:
                if "for" not in fLine: 
                    continue
                title =  fLine[9:]

    #define some data points . . .
    x      = array('f', kineticEnergy )
    y      = array('f', crossSec)
    y_el   = array('f', crossSec_el)
    y_inel = array('f', crossSec_inel)
    exl    = array('f', zero)
    exr    = array('f', zero)
    
    nPoints=len(x)
    # . . . and hand over to TGraphErros object
    gr      = TGraphErrors ( nPoints , x , y     , exl, exr )
    gr.SetTitle(title+"; Kinetic Energy [MeV]; Cross Section [barn]")
    gr . GetXaxis().SetRangeUser(0,1000)
    gr . GetYaxis().SetRangeUser(0,2.)
    gr . SetLineWidth(2) ;
    gr . SetLineColor(kGreen-2) ;
    gr . SetFillColor(0)
    return gr


# Get Truth
pionTrue_60_FileName = "AngleCut_5deg_histo_60A.root"
pionTrue_60 = TFile.Open(pionTrue_60_FileName)
pionTrue_60_Int  = pionTrue_60.Get("AngleCutTrueXS083/hInteractingKE")
pionTrue_60_Inc  = pionTrue_60.Get("AngleCutTrueXS083/hIncidentKE")
pionTrue_60_Int.Sumw2()
pionTrue_60_Inc.Sumw2()
pionTrue_60_Int.SetLineColor(kBlue)
pionTrue_60_Int.Divide(pionTrue_60_Inc)
pionTrue_60_Int.Scale(101.)
# Get Truth
pionTrue_100_FileName = "AngleCut_5deg_histo_100A.root"
pionTrue_100 = TFile.Open(pionTrue_100_FileName)
pionTrue_100_Int  = pionTrue_100.Get("AngleCutTrueXS083/hInteractingKE")
pionTrue_100_Inc  = pionTrue_100.Get("AngleCutTrueXS083/hIncidentKE")
pionTrue_100_Int.Sumw2()
pionTrue_100_Inc.Sumw2()
pionTrue_100_Int.SetLineColor(kRed)
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


f5 = TFile("../cleanReco/MC100APionsReco_histo.root")
h5 = f5.Get( "XS")
h5.SetMarkerColor(kBlue)
h5.SetLineColor(kBlue)
h5.SetMarkerStyle(22)
h5.SetMarkerSize(.72)

f3 = TFile("../cleanReco/MC60APionsReco_histo.root")
h3 = f3.Get( "XS")
h3.SetMarkerColor(kRed)
h3.SetLineColor(kRed)
h3.SetMarkerStyle(22)
h3.SetMarkerSize(.72)


fC = TFile("MCRecoClosure.root")
h60  = fC.Get( "XS60AWeightAndCorrected")
h100 = fC.Get( "XS100AWeightAndCorrected")
h60.SetMarkerColor(kBlack)
h60.SetLineColor(kBlack)
h60.SetMarkerStyle(22)
h60.SetMarkerSize(.72)
h100.SetMarkerColor(kBlack)
h100.SetLineColor(kBlack)
h100.SetMarkerStyle(22)
h100.SetMarkerSize(.72)




                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",600,600)
c0C.Update()
c0C.SetGrid()
pionTrue_60_Int.GetXaxis().SetRangeUser(0,1000)
pionTrue_60_Int.GetYaxis().SetRangeUser(0,2)

pionTrue_60_Int.Draw("pe")
pionTrue_100_Int.Draw("pesame")         

c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1 = c0.cd(1)
p1.SetGrid()
gr = graphTruth()
gr .Draw ( "APL" ) ;
trueXSAll.SetTitle("True Total (#pi-Ar) Cross Section #alpha>5deg; Kinetic Energy [MeV]; True Cross Section [Barn]")
trueXSAll.GetXaxis().SetRangeUser(0,1000)
trueXSAll.GetYaxis().SetRangeUser(0,2)
trueXSAll.Draw("pesame")
h3.Draw("pesame")
h60.Draw("pesame")


legend1 = TLegend(.44,.70,.84,.89)
legend1.AddEntry(gr,"G4 Prediction Tot XS")
legend1.AddEntry(trueXSAll,"True Interaction w/ angle > 5 deg")
legend1.AddEntry(h3,"Reco XS,  60A w/ WC2TPC weight")
legend1.AddEntry(h60,"Reco XS, 60A w/ WC2TPC weight corrected")
legend1.Draw("same")

p2 = c0.cd(2)
p2.SetGrid()
gr .Draw ( "APL" ) ;
trueXSAll.Draw("pesame")
h5.Draw("pesame")
h100.Draw("pesame")

legend2 = TLegend(.44,.70,.84,.89)
legend2.AddEntry(gr,"G4 Prediction Tot XS")
legend2.AddEntry(trueXSAll,"True Interaction w/ angle > 5 deg")
legend2.AddEntry(h5,"Reco XS, 100A w/ WC2TPC weight")
legend2.AddEntry(h100,"Reco XS, 100A w/ WC2TPC weight corrected")
legend2.Draw("same")

f = TFile("Truth.root", "recreate")
f.Add(trueXSAll)
f.Write()
f.Close
raw_input()

