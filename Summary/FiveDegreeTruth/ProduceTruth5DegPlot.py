from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os
import math
from array import array



# Get Truth
pionTrue_60_FileName = "AngleCut_5deg_histo_60A.root"
pionTrue_60 = TFile.Open(pionTrue_60_FileName)
pionTrue_60_Int  = pionTrue_60.Get("AngleCutTrueXS083/hInteractingKE")
pionTrue_60_Inc  = pionTrue_60.Get("AngleCutTrueXS083/hIncidentKE")

# Get Truth
pionTrue_100_FileName = "AngleCut_5deg_histo_100A.root"
pionTrue_100 = TFile.Open(pionTrue_100_FileName)
pionTrue_100_Int  = pionTrue_100.Get("AngleCutTrueXS083/hInteractingKE")
pionTrue_100_Inc  = pionTrue_100.Get("AngleCutTrueXS083/hIncidentKE")
combinedInt = pionTrue_60_Int.Clone("True_Int")
combinedInc = pionTrue_60_Inc.Clone("True_Inc")
combinedInt.Add(pionTrue_100_Int)
combinedInc.Add(pionTrue_100_Inc)
combinedInt.Sumw2()
combinedInc.Sumw2()
combinedInt.SetLineColor(kGreen-2)
combinedInt.SetLineWidth(2)

trueXSAll = combinedInt.Clone("trueXSAll")
trueXSAll.Divide(combinedInc)
trueXSAll.Scale(101.)



                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",600,600)
c0C.Update()
c0C.SetGrid()
trueXSAll.SetTitle("True Total (#pi-Ar) Cross Section #alpha>5deg; Kinetic Energy [MeV]; True Cross Section [Barn]")
trueXSAll.GetXaxis().SetRangeUser(0,1000)
trueXSAll.GetYaxis().SetRangeUser(0,2)
trueXSAll.Draw("pesame")
combinedInt.Draw("pesame")


f = TFile("Truth.root", "recreate")
pionTrue_60_Int. SetName("pionTrue_60_Int")
pionTrue_60_Inc. SetName("pionTrue_60_Inc")
pionTrue_100_Int. SetName("pionTrue_100_Int")
pionTrue_100_Inc. SetName("pionTrue_100_Inc")

f.Add(pionTrue_60_Int)
f.Add(pionTrue_60_Inc)
f.Add(pionTrue_100_Int)
f.Add(pionTrue_100_Inc)
f.Add(combinedInt)
f.Add(combinedInc)
f.Add(trueXSAll)
f.Write()
f.Close
raw_input()

