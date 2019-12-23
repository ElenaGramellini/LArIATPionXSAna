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
f60A = TFile("Eff_Correction_60A.root")
h60A = f60A.Get( "move_XS_5_60A")
h60A.SetTitle("60A Correction for Reco Effect; KE [MeV]; Correction")
h60A.GetXaxis().SetRangeUser(0,1000.)
h60A.SetMarkerColor(kRed)
h60A.SetLineColor(kRed)
h60A.Draw("")

p2=c1.cd(2)
p2.SetGrid()
f100A = TFile("Eff_Correction_100A.root")
h100A = f100A.Get( "move_XS_5_100A")
h100A.SetTitle("100A Correction for Reco Effect; KE [MeV]; Correction")
h100A.GetXaxis().SetRangeUser(0,1000.)
h100A.SetMarkerColor(kBlue)
h100A.SetLineColor(kBlue)
h100A.Draw("")

c=TCanvas("c" ,"Data" ,200 ,10 ,700 ,700) #make nice                                                                                                                                                          
c.SetGrid()
h60A.Draw("")
h100A.Draw("same")
legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(h60A ,"60A correction for TPCCorr")
legend.AddEntry(h100A,"100A correction for TPCCorr")
legend.Draw("same")
c.Update()


raw_input()  
