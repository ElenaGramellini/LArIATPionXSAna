from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array


gStyle.SetOptStat(0)

c1=TCanvas("c1" ,"Data" ,200 ,10 ,1400 ,700) #make nice
c1.Divide(2,1)
p1=c1.cd(1)
p1.SetGrid ()
#f60A = TFile("bkgFiles/BkgSub_0.152muons_0.148electrons_60A.root")
f60A = TFile("bkgFiles/BkgSub_0.152muons_0.045electrons_60A.root")
h60A = f60A.Get( "C_Int_Over_C_Inc_60A")
h60A.SetTitle("60A Beamline Bkg Effect; KE [MeV]; Correction")
h60A.GetXaxis().SetRangeUser(0,1000.)
h60A.SetMarkerColor(kRed)
h60A.SetLineColor(kRed)
h60A.Draw("")

p2=c1.cd(2)
p2.SetGrid()
f100A = TFile("bkgFiles/BkgSub_0.14muons_0.045electrons_100A.root")
h100A = f100A.Get( "C_Int_Over_C_Inc_100A")
h100A.SetTitle("100A Beamline Bkg Effect; KE [MeV]; Correction")
h100A.GetXaxis().SetRangeUser(0,1000.)
h100A.SetMarkerColor(kBlue)
h100A.SetLineColor(kBlue)
h100A.Draw("")

c2 = TCanvas("c2","c2",600,600)
c2.SetGrid()
h60A.SetTitle("Beamline Bkg Effect; KE [MeV]; Correction for Bkg")
h60A.Draw()
h100A.Draw("same")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(h60A ,"60A correction for bkg")
legend.AddEntry(h100A,"100A correction for bkg")

legend.Draw("same")

c2.Update()
raw_input()  
