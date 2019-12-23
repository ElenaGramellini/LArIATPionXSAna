from ROOT import *
import os
import math
import argparse

from ROOT import TEfficiency
from ROOT import gStyle , TCanvas , TGraphErrors
from array import array

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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




c1=TCanvas("c1" ,"Data" ,200 ,10 ,700 ,700) #make nice
c1.SetGrid ()
gr = graphTruth()




f = TFile("../../FiducialVolumeStudy/askForInt/FidVol_Z90.0_19.0_-19.0_46.0_1.0_TrueInt_60A.root")
h = f.Get( "XS")
h.SetMarkerColor(kGreen-2)
h.SetLineColor(kGreen-2)
h.SetMarkerStyle(22)
h.SetMarkerSize(.72)

f3 = TFile("FlatEff0.8SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
h3 = f3.Get( "XS")
h3.SetMarkerColor(kBlack)
h3.SetLineColor(kBlack)
h3.SetMarkerStyle(22)
h3.SetMarkerSize(.72)

f5 = TFile("FlatEff0.5SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
h5 = f5.Get( "XS")
h5.SetMarkerColor(kRed)
h5.SetLineColor(kRed)
h5.SetMarkerStyle(22)
h5.SetMarkerSize(.72)

f4 = TFile("FlatEff0.3SameFidVol_Z86.0_19.0_-19.0_46.0_1.060.root")
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

legend = TLegend(.44,.70,.84,.89)
legend.AddEntry(gr,"G4 Prediction Tot XS")
legend.AddEntry(h,"True Interaction, Z [0., 90.] cm")
legend.AddEntry(h3,"Fid Vol, Z [0., 86.] cm, flat wc2tpc eff 0.8, 60A")
legend.AddEntry(h5,"Fid Vol, Z [0., 86.] cm, flat wc2tpc eff 0.5, 60A")
legend.AddEntry(h4,"Fid Vol, Z [0., 86.] cm, flat wc2tpc eff 0.3, 60A")


legend.Draw("same")


c1 . Update ()



raw_input()  
