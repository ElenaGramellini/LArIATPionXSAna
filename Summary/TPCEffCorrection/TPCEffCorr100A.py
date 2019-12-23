from ROOT import *
import ROOT as root
import numpy as np
import argparse
import os


gStyle.SetOptStat(0)

def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
    XS =  InteractingHisto.Clone(Name)
    XS.Scale(101.10968)
    XS.Divide(IncidentHisto)
    return XS


outFileName = "Eff_Correction_100A.root"

########################################################################
########################    MC Part   ##################################
########################################################################
# Get Monte Carlo files
pionMC_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/WC2TPCEff/applyWC2TPCWeightsToRecoSamples/atanFiles/MC100APionsReco_histo.root"
pionMC_File   = TFile.Open(pionMC_FileName)
# Get Interacting and Incident plot
pionMC_Int  = pionMC_File.Get("hInteractingKE")
pionMC_Inc  = pionMC_File.Get("hIncidentKE")


# Get Truth
pionTrue_5_FileName = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/Summary/FiveDegreeTruth/Truth.root"
pionTrue_5 = TFile.Open(pionTrue_5_FileName)
pionTrue_5_Int  = pionTrue_5.Get("pionTrue_100_Int")
pionTrue_5_Inc  = pionTrue_5.Get("pionTrue_100_Inc")



###############################################################################

eff_Corr_5_Int = pionMC_Int.Clone("eff_Corr_5_Int_100A")
eff_Corr_5_Int.Sumw2()
pionTrue_5_Int.Sumw2()
eff_Corr_5_Int.Divide(pionTrue_5_Int)   

eff_Corr_5_Inc = pionMC_Inc.Clone("eff_Corr_5_Inc_100A")
eff_Corr_5_Inc.Sumw2()
pionTrue_5_Inc.Sumw2()
eff_Corr_5_Inc.Divide(pionTrue_5_Inc)   

moveXS_5 = eff_Corr_5_Inc.Clone("move_XS_5_100A")
moveXS_5.Divide(eff_Corr_5_Int)   

eff_Corr_5_Int .SetFillColor(kWhite) 
eff_Corr_5_Inc .SetFillColor(kWhite) 
moveXS_5       .SetFillColor(kWhite) 

eff_Corr_5_Int .SetLineColor(kRed) 
eff_Corr_5_Inc .SetLineColor(kRed) 
moveXS_5       .SetLineColor(kRed) 


###############################################################################

## Check Staggered Plots Make Sense
c0 = TCanvas("c0","c0",1200,600)
c0.Divide(2,1)
p1c0 = c0.cd(1)
p1c0.SetGrid()
eff_Corr_5_Int.Draw("pe")

p2c0 = c0.cd(2)
p2c0.SetGrid()
c0.Update()
eff_Corr_5_Inc.Draw("pe")
                           
## Check Staggered Plots Make Sense
c0C = TCanvas("c0C","c0C",600,600)
p2c0C = c0C.cd()
p2c0C.SetGrid()
moveXS_5.Draw("pe")
c0C.Update()
     
                                
#####################################################################
#######################    Closure Check   ###########################
#####################################################################
hTrueXS_5 = calculateXSPlot(pionTrue_5_Int, pionTrue_5_Inc, "TrueXS100A"  )
hRecoXS_5 = calculateXSPlot(pionMC_Int    , pionMC_Inc    , "RecoXS100A"  )
hRecoXS_5_Corrected = hRecoXS_5.Clone("hRecoXS_5_Corrected")
hRecoXS_5_Corrected.Multiply(moveXS_5)

hTrueXS_5.SetLineColor(kBlue)
hRecoXS_5.SetLineColor(kRed)
hRecoXS_5_Corrected.SetLineColor(kBlack)

hTrueXS_5.GetXaxis().SetRangeUser(0,1000)
hTrueXS_5.GetYaxis().SetRangeUser(0,2)

## Check Staggered Plots Make Sense
c01 = TCanvas("MCClosure","c01",600,600)
p2c0C = c01.cd()
p2c0C.SetGrid()
hTrueXS_5.SetTitle("MC Closure Test; KE [MeV]; Cross Section [Barn]")
hTrueXS_5.Draw("pe")
hRecoXS_5.Draw("pesame")
hRecoXS_5_Corrected.Draw("pesame")
hTrueXS_5 .SetLineWidth(2) 
hTrueXS_5.GetXaxis().SetRangeUser(0,1000)

legend = TLegend(0.38,0.65,0.90,0.88)
legend.SetHeader("LArIAT Negative Pol Low Energy Tune");
legend.AddEntry(hTrueXS_5,"MCTrue XS")
legend.AddEntry(hRecoXS_5,"MC Reco XS")
legend.AddEntry(hRecoXS_5_Corrected,"MC Reco XS Corrected ")

legend.Draw("same")

c01.Update()
#####################################################################
#######################    Save to File   ###########################
#####################################################################


outFile = TFile(outFileName,"recreate")
outFile.cd()

eff_Corr_5_Int .Write() 
eff_Corr_5_Inc .Write() 
moveXS_5       .Write() 

outFile.Write()
outFile.Close()

raw_input()

