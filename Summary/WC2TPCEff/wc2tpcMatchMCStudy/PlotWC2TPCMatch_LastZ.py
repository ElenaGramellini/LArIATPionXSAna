from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array


gStyle.SetOptFit(11111)

c1=TCanvas("c1" ,"Data" ,200 ,10 ,1400 ,700) #make nice
c1.Divide(2,1)
p1=c1.cd(1)
p1.SetGrid ()

f60A = TFile("Lenths_AfterWC2TPC_60A.root")
h60A = f60A.Get( "hLastZTrue")
h60A.Rebin(4)
h60A.SetMarkerColor(kRed)
h60A.SetLineColor(kRed)
f60B = TFile("Lenths_BeforeWC2TPC_60A.root")
h60B = f60B.Get( "hLastZTrue")
h60B.Rebin(4)
h60B.SetMarkerColor(kRed)
h60B.SetLineColor(kRed)
h60B.Scale(717000./275000.)

WC2TPCMatch60A = h60A.Clone("WC2TPCMatch60A")
WC2TPCMatch60A.Sumw2()
WC2TPCMatch60A.Divide(h60B)
WC2TPCMatch60A.GetYaxis().SetRangeUser(0.,1.)
WC2TPCMatch60A.SetTitle("WC2TPC Match 60A; True Last Z [cm]; Events After Match / Events Before Match")
WC2TPCMatch60A.Draw("pe")
#fit60 = TF1("fit60","[0]*log(x + [2]) + [1]",2,90)
fit60 = TF1("fit60","[1]*atan(x*x + [2]) + [0]",1,90)
fit60.SetParameter(0, -1.17464e+01)
fit60.SetParameter(1,  7.95233e+00)
fit60.SetParameter(2,  1.12823e+01)
WC2TPCMatch60A.Fit(fit60,"R")


 


p2=c1.cd(2)
p2.SetGrid ()
f100A = TFile("Lenths_AfterWC2TPC_100A.root")
h100A = f100A.Get( "hLastZTrue")
h100A.Rebin(4)
h100A.SetMarkerColor(kBlue)
h100A.SetLineColor(kBlue)

f100B = TFile("Lenths_BeforeWC2TPC_100A.root")
h100B = f100B.Get( "hLastZTrue")
h100B.Rebin(4)
h100B.SetMarkerColor(kBlue)
h100B.SetLineColor(kBlue)
h100B.Scale(718332./274936.)



WC2TPCMatch100A = h100A.Clone("WC2TPCMatch100A")
WC2TPCMatch100A.Sumw2()
WC2TPCMatch100A.Divide(h100B)
WC2TPCMatch100A.GetYaxis().SetRangeUser(0.,1.)
WC2TPCMatch100A.SetTitle("WC2TPC Match 100A; True Last Z [cm]; Events After Match / Events Before Match")
WC2TPCMatch100A.Draw("pe")
fit100 = TF1("fit100","[1]*atan(x*x + [2]) + [0]",1,90)
fit100.SetParameter(0, -1.28700e+01)
fit100.SetParameter(1,  8.71446e+00)
fit100.SetParameter(2,  1.15204e+01)
WC2TPCMatch100A.Fit(fit100,"R")
c1 . Update ()


c3=TCanvas("c3" ,"MC" ,200 ,10 ,700 ,700) #make nice
c3.SetGrid ()
WC2TPCMatch60A.Draw("histo")
WC2TPCMatch100A.Draw("histosame")

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(WC2TPCMatch60A, " 60A, MC")
legend.AddEntry(WC2TPCMatch100A,"100A, MC")
legend.Draw("pe")




c2=TCanvas("c2" ,"Data" ,200 ,10 ,700 ,700) #make nice
c2.SetGrid ()
WC2TPCMatch60A.Draw("histo")
WC2TPCMatch100AShift = WC2TPCMatch100A.Clone("WC2TPCMatch100AShift")
for i in xrange(WC2TPCMatch100AShift.GetSize()-2):
    WC2TPCMatch100AShift.SetBinContent(i, WC2TPCMatch100AShift.GetBinContent(i)-0.065958)
WC2TPCMatch100AShift.SetLineColor(kBlue-3)
WC2TPCMatch100AShift.Draw("samehisto")

legend2 = TLegend(.44,.70,.84,.89)
legend2.AddEntry(WC2TPCMatch60A, " 60A, MC")
legend2.AddEntry(WC2TPCMatch100AShift,"100A, MC Shift down by a flat 6.5%")
legend2.Draw("same")

raw_input()  
