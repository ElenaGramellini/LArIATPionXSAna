from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array

def efficiencyFunct( L ):
    p0 =   0.00387083
    p1 =     0.188846
    p2 =    -0.015353
    p3 =  0.000429051

    if L < 1 :
        return p0 + p1 + p2 + p3
    
    if L > 15:
        p0   =     0.789496
        p1   =   0.00483068
        p2   = -0.000109864
        p3   =   5.4741e-07
    return p0 + p1*L + p2*L*L + p3*L*L*L 



'''
FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root  
FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root  
FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root

FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root   
FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root   
FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root
'''



gStyle.SetOptStat(0)

c1=TCanvas("c1" ,"Data" ,200 ,10 ,700 ,700) #make nice
c1.SetGrid ()




f100_08     = TFile("NonFlatEffSameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
hPre100_08  = f100_08.Get( "hDistancePre")
hPost100_08 = f100_08.Get( "hDistancePost")
hPre100_08.Rebin(4)
hPost100_08.Rebin(4)
ratio100_08 = hPost100_08.Clone("h100_08")
ratio100_08.SetTitle(";True Track Length [cm]; WC2TPC match efficiency")
ratio100_08.Sumw2()
ratio100_08.Divide(hPre100_08)
ratio100_08.SetLineColor(kRed)
ratio100_08.Draw("histo")


f100_05     = TFile("NonFlatEffSameFidVol_Z86.0_19.0_-19.0_46.0_1.0100.root")
hPre100_05  = f100_05.Get( "hDistancePre")
hPost100_05 = f100_05.Get( "hDistancePost")
hPre100_05.Rebin(4)
hPost100_05.Rebin(4)
ratio100_05 = hPost100_05.Clone("h100_05")
ratio100_05.Sumw2()
ratio100_05.Divide(hPre100_05)
ratio100_05.SetLineColor(kBlue)
ratio100_05.Draw("histosame")


effFunction1 = TF1("eff1","0.177792881",0,1)
effFunction2 = TF1("eff2","0.00387083+0.188846*x-0.015353*x*x+0.000429051*x*x*x", 1, 15)
effFunction3 = TF1("eff3","0.789496+0.00483068*x-0.00010986*x*x+0.00000054741*x*x*x",15,100)
effFunction1.SetLineColor(kBlack)
effFunction2.SetLineColor(kBlack)
effFunction3.SetLineColor(kBlack)

effFunction1.SetLineWidth(2)
effFunction2.SetLineWidth(2)
effFunction3.SetLineWidth(2)

effFunction1.Draw("same")
effFunction2.Draw("same")
effFunction3.Draw("same")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(ratio100_08,"Non flat wc2tpc eff 60A")
legend.AddEntry(ratio100_05,"Non flat wc2tpc eff 100A")


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
