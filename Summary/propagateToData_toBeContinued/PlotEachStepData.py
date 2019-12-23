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




fMCTruth  = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/FiveDegreeTruth/Truth.root")
trueXSAll = fMCTruth.Get( "trueXSAll")
trueXSAll.SetLineWidth(2)
trueXSAll.SetLineColor(kGreen-2)

################################# Raw Data XS ########################################################################

fRaw100 = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/rawDataXS/Data100A_histo.root")
hRaw100 = fRaw100.Get( "XS")
hRaw100.SetMarkerColor(kBlue)
hRaw100.SetLineColor(kBlue)
hRaw100.SetMarkerStyle(22)
hRaw100.SetMarkerSize(.72)

fRaw60 = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/rawDataXS/Data60A_histo.root")
hRaw60 = fRaw60.Get( "XS")
hRaw60.SetMarkerColor(kRed)
hRaw60.SetLineColor(kRed)
hRaw60.SetMarkerStyle(22)
hRaw60.SetMarkerSize(.72)


c0Raw = TCanvas("c0Raw","Raw XS",600,600)
c0Raw.Update()
c0Raw.SetGrid()
trueXSAll.SetTitle("Total (#pi-Ar) Cross Section #alpha>5deg; Kinetic Energy [MeV];  Cross Section [Barn]")
trueXSAll.GetXaxis().SetRangeUser(0,1000)
trueXSAll.GetYaxis().SetRangeUser(0,2)
trueXSAll.Draw("histo")
hRaw100.Draw("same")
hRaw60.Draw("same")
legendRaw = TLegend(.44,.70,.84,.89)
legendRaw.AddEntry(trueXSAll,"True Interaction w/ angle > 5 deg")
legendRaw.AddEntry(hRaw60 ,"Data Raw XS, 60A")
legendRaw.AddEntry(hRaw100 ,"Data Raw XS, 100A")
legendRaw.Draw("same")
c0Raw.Update()
c0Raw.SaveAs("Raw.png")




################################# WC2TPCWeight Data XS ########################################################################

fWC2TPCWeight100 = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/WC2TPCEff/applyWC2TPCWeightsToRecoSamples/atanFiles//Data100A_histo.root")
hWC2TPCWeight100 = fWC2TPCWeight100.Get( "XS")
hWC2TPCWeight100.SetMarkerColor(kBlue)
hWC2TPCWeight100.SetLineColor(kBlue)
hWC2TPCWeight100.SetMarkerStyle(22)
hWC2TPCWeight100.SetMarkerSize(.72)

fWC2TPCWeight60 = TFile("/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/WC2TPCEff/applyWC2TPCWeightsToRecoSamples/atanFiles/Data60A_histo.root")
hWC2TPCWeight60 = fWC2TPCWeight60.Get( "XS")
hWC2TPCWeight60.SetMarkerColor(kRed)
hWC2TPCWeight60.SetLineColor(kRed)
hWC2TPCWeight60.SetMarkerStyle(22)
hWC2TPCWeight60.SetMarkerSize(.72)

c0WC2TPCWeight = TCanvas("c0WC2TPCWeight","WC2TPCWeight XS",600,600)
c0WC2TPCWeight.Update()
c0WC2TPCWeight.SetGrid()
trueXSAll.Draw("histo")
hWC2TPCWeight100.Draw("same")
hWC2TPCWeight60.Draw("same")
legendWC2TPCWeight = TLegend(.44,.70,.84,.89)
legendWC2TPCWeight.AddEntry(trueXSAll,"True Interaction w/ angle > 5 deg")
legendWC2TPCWeight.AddEntry(hWC2TPCWeight60 ,"Data WC2TPCWeight XS, 60A")
legendWC2TPCWeight.AddEntry(hWC2TPCWeight100 ,"Data WC2TPCWeight XS, 100A")
legendWC2TPCWeight.Draw("same")
c0WC2TPCWeight.Update()
c0WC2TPCWeight.SaveAs("WC2TPCWeight.png")

################################# BkgSub Data XS ########################################################################

fCorrections = TFile("StepByStepData.root")
hBkgSub100 = fCorrections.Get( "XS100AWeightAndBkgSub")
hBkgSub100.SetMarkerColor(kBlue)
hBkgSub100.SetLineColor(kBlue)
hBkgSub100.SetMarkerStyle(22)
hBkgSub100.SetMarkerSize(.72)

hBkgSub60 = fCorrections.Get( "XS60AWeightAndBkgSub")
hBkgSub60.SetMarkerColor(kRed)
hBkgSub60.SetLineColor(kRed)
hBkgSub60.SetMarkerStyle(22)
hBkgSub60.SetMarkerSize(.72)

c0BkgSub = TCanvas("c0BkgSub","BkgSub XS",600,600)
c0BkgSub.Update()
c0BkgSub.SetGrid()
trueXSAll.Draw("histo")
hBkgSub100.Draw("same")
hBkgSub60.Draw("same")
legendBkgSub = TLegend(.44,.70,.84,.89)
legendBkgSub.AddEntry(trueXSAll,"True Interaction w/ angle > 5 deg")
legendBkgSub.AddEntry(hBkgSub60 ,"Data BkgSub XS, 60A")
legendBkgSub.AddEntry(hBkgSub100 ,"Data BkgSub XS, 100A")
legendBkgSub.Draw("same")
c0BkgSub.Update()
c0BkgSub.SaveAs("c0BkgSub.png")



################################# TPCCorr Data XS ########################################################################

hTPCCorr100 = fCorrections.Get( "XS100AWeightBkgSubAndCorrected")
hTPCCorr100.SetMarkerColor(kBlue)
hTPCCorr100.SetLineColor(kBlue)
hTPCCorr100.SetMarkerStyle(22)
hTPCCorr100.SetMarkerSize(.72)

hTPCCorr60 = fCorrections.Get( "XS60AWeightBkgSubAndCorrected")
hTPCCorr60.SetMarkerColor(kRed)
hTPCCorr60.SetLineColor(kRed)
hTPCCorr60.SetMarkerStyle(22)
hTPCCorr60.SetMarkerSize(.72)

c0TPCCorr = TCanvas("c0TPCCorr","TPCCorr XS",600,600)
c0TPCCorr.Update()
c0TPCCorr.SetGrid()
trueXSAll.Draw("histo")
hTPCCorr100.Draw("same")
hTPCCorr60.Draw("same")
legendTPCCorr = TLegend(.44,.70,.84,.89)
legendTPCCorr.AddEntry(trueXSAll,"True Interaction w/ angle > 5 deg")
legendTPCCorr.AddEntry(hTPCCorr60 ,"Data TPCCorr XS, 60A")
legendTPCCorr.AddEntry(hTPCCorr100 ,"Data TPCCorr XS, 100A")
legendTPCCorr.Draw("same")
c0TPCCorr.Update()
c0TPCCorr.SaveAs("c0TPCCorr.png")

'''
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1 = c0.cd(1)
p1.SetGrid()
gr = graphTruth()
gr .Draw ( "APL" ) ;
trueXSAll.SetTitle("True Total (#pi-Ar) Cross Section #alpha>Rawdeg; Kinetic Energy [MeV]; True Cross Section [Barn]")
trueXSAll.GetXaxis().SetRangeUser(0,1000)
trueXSAll.GetYaxis().SetRangeUser(0,2)
trueXSAll.Draw("pesame")
h3.Draw("pesame")
h60.Draw("pesame")


legend1 = TLegend(.44,.70,.84,.89)
legend1.AddEntry(gr,"G4 Prediction Tot XS")
legend1.AddEntry(trueXSAll,"True Interaction w/ angle > Raw deg")
legend1.AddEntry(h3,"Reco XS,  60A w/ WC2TPC weight")
legend1.AddEntry(h60,"Reco XS, 60A w/ WC2TPC weight corrected")
legend1.Draw("same")

p2 = c0.cd(2)
p2.SetGrid()
gr .Draw ( "APL" ) ;
trueXSAll.Draw("pesame")
hRaw.Draw("pesame")
h100.Draw("pesame")

legend2 = TLegend(.44,.70,.84,.89)
legend2.AddEntry(gr,"G4 Prediction Tot XS")
legend2.AddEntry(trueXSAll,"True Interaction w/ angle > Raw deg")
legend2.AddEntry(hRaw,"Reco XS, 100A w/ WC2TPC weight")
legend2.AddEntry(h100,"Reco XS, 100A w/ WC2TPC weight corrected")
legend2.Draw("same")

f = TFile("Truth.root", "recreate")
f.Add(trueXSAll)
f.Write()
f.Close
'''
raw_input()

