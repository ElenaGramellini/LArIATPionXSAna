from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array

'''
FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root  
FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root  
FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root

FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root   
FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root   
FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root
'''



gStyle.SetOptStat(0)

c1=TCanvas("c1" ,"Data" ,200 ,10 ,700 ,700) #make nice
c1.SetGrid ()

f60_08     = TFile("FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
hPre60_08  = f60_08.Get( "hDistancePre")
hPost60_08 = f60_08.Get( "hDistancePost")
hPre60_08.Rebin(4)
hPost60_08.Rebin(4)
ratio60_08 = hPost60_08.Clone("h60_08")
ratio60_08.SetTitle(";True Track Length [cm]; WC2TPC match efficiency")
ratio60_08.Sumw2()
ratio60_08.Divide(hPre60_08)
ratio60_08.SetLineColor(kBlack)
ratio60_08.Draw("histo")


f60_05     = TFile("FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
hPre60_05  = f60_05.Get( "hDistancePre")
hPost60_05 = f60_05.Get( "hDistancePost")
hPre60_05.Rebin(4)
hPost60_05.Rebin(4)
ratio60_05 = hPost60_05.Clone("h60_05")
ratio60_05.Sumw2()
ratio60_05.Divide(hPre60_05)
ratio60_05.SetLineColor(kRed)
ratio60_05.Draw("histosame")

f60_03     = TFile("FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
hPre60_03  = f60_03.Get( "hDistancePre")
hPost60_03 = f60_03.Get( "hDistancePost")
hPre60_03.Rebin(4)
hPost60_03.Rebin(4)
ratio60_03 = hPost60_03.Clone("h60_03")
ratio60_03.Sumw2()
ratio60_03.Divide(hPre60_03)
ratio60_03.SetLineColor(kOrange)
ratio60_03.Draw("histosame")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(ratio60_08,"Flat wc2tpc eff 0.8")
legend.AddEntry(ratio60_05,"Flat wc2tpc eff 0.5")
legend.AddEntry(ratio60_03,"Flat wc2tpc eff 0.3")

legend.Draw("same")



'''


f3 = TFile("FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root")
h3 = f3.Get( "XS")
h3.SetMarkerColor(kBlack)
h3.SetLineColor(kBlack)
h3.SetMarkerStyle(22)
h3.SetMarkerSize(.72)

f5 = TFile("FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root")
h5 = f5.Get( "XS")
h5.SetMarkerColor(kRed)
h5.SetLineColor(kRed)
h5.SetMarkerStyle(22)
h5.SetMarkerSize(.72)

f4 = TFile("FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root")
h4 = f4.Get( "XS")
h4.SetMarkerColor(kOrange)
h4.SetLineColor(kOrange)
h4.SetMarkerStyle(22)
h4.SetMarkerSize(.72)

gr .Draw ( "APL" ) ;
h  .Draw("same")
h3 .Draw("same")
h5 .Draw("same")
h4 .Draw("same")

'''

c1 . Update ()



raw_input()  
