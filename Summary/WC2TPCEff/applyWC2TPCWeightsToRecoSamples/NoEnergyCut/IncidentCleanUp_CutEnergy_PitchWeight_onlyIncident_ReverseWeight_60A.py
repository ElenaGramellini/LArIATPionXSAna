from ROOT import *
import ROOT as root
import numpy as np
import math
import argparse
import os

#gStyle.SetOptStat(0)
def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
    XS =  InteractingHisto.Clone(Name)
   # XS.Sumw2()
   # IncidentHisto.Sumw2()
    XS.Scale(101.10968)
    XS.Divide(IncidentHisto)
    return XS

# mode = 1 is 60A
def efficiencyFunct( L, mode = 0 , printME = False):
    funct = TF1("func","[1]*atan(x*x + [2]) + [0]",1,90)
    if mode:
        funct.SetParameter(0,-1.54880e+01)
        funct.SetParameter(1, 1.03410e+01)
        funct.SetParameter(2, 1.56050e+01)
    else:
        funct.SetParameter(0,-1.80342e+01)
        funct.SetParameter(1, 1.20083e+01)
        funct.SetParameter(2, 1.76809e+01)
        
    if printME:
        c=TCanvas("c","c",700,700)
        c.cd()
        funct.Draw()
        c.Update()
    if L < 1 :
        return funct.Eval(1.)

    return funct.Eval(L)



#Get Input File
parser = argparse.ArgumentParser()
parser.add_argument("fileName"     , nargs='?', default = "/Users/elenag/Documents/Papers/ThatsIt/rootFiles/MC60APionsReco_histo.root", type = str, help="insert fileName")
parser.add_argument("folderName"   , nargs='?', default = "RecoXSPionOnly"                                                           , type = str, help="root folder name")
parser.add_argument("outFileName"  , nargs='?', default = "MC100AElectronReco_histo_cleaned_CutEnergy.root"                     , type = str, help="outfile name")


args    = parser.parse_args()
inFileName   = args.fileName
folder_Name  = args.folderName
outFileName  = args.outFileName
print outFileName , " ------------------------------------- "

f      = root.TFile(inFileName)
myTree = f.Get(folder_Name+"/effTree")

# These come directly from the inputFile
hInteractingKEComp = f.Get(folder_Name+"/hRecoInteractingKE")
hIncidentKEComp    = f.Get(folder_Name+"/hRecoIncidentKE")


hInteractingKE   = TH1D("hInteractingKE","hInteractingKE" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE      = TH1D("hIncidentKE"   ,"hIncidentKE"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hInteractingKEMax = TH1D("hInteractingKEMax","hInteractingKEMax",hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKEMax    = TH1D("hIncidentKEMax"   ,"hIncidentKEMax"   , hIncidentKEComp.GetSize()  -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hInteractingKEMin = TH1D("hInteractingKEMin","hInteractingKEMin",hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKEMin    = TH1D("hIncidentKEMin"   ,"hIncidentKEMin"   , hIncidentKEComp.GetSize()  -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

uncertaintyEDep        = 0.03
uncertaintyMomentum    = 1.
relUncertaintyMomentum = 0.02
uncertaintyELoss       = 8.


countReject = 0
countKeep   = 0

print myTree.GetEntry()
sillyCount =0 
for entry in myTree:
     sillyCount += 1
     if not sillyCount % 10000:
          print sillyCount
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     eventN     = entry.eventN
     recoIncidentKE      = entry.recoIncidentKE
     recoZPosition       = entry.recoZPosition
     isTrackInteracting  = entry.isTrackInteracting
     momentum            = entry.WCMom
     recoPitch           = entry.recoPitch
     uncertaintyMomentum = relUncertaintyMomentum*momentum
     recoEndX            = entry.recoEndX
     recoEndY            = entry.recoEndY
     recoEndZ            = entry.recoEndZ
     recoVtxX            = entry.recoVtxX
     recoVtxY            = entry.recoVtxY
     recoVtxZ            = entry.recoVtxZ


     distance = recoEndZ
     if recoEndZ < recoVtxZ:
         distance = recoVtxZ
     decisionW = 1./efficiencyFunct(distance,1)
     # Keeping only meaningful points
     recoZposSkim = []
     recoKESkim   = []
     recoZposSkimCp = []
     recoKESkimCp   = []
     recoPitchSkim  = []

     # clean up non sensical numbers
     for i in recoZPosition:         
         if i < -900. or  math.isnan(i) or i < 0.000001 or i > 150000:
              continue
         recoZposSkim.append(i)
         recoZposSkimCp.append(i)


     for i in recoIncidentKE:
          if i < -990  or  math.isnan(i) or i < 0.001 or i > 150000:
              continue
          recoKESkim.append(i)
          recoKESkimCp.append(i)

     indexList = -1
     for i in recoPitch:
         if i < -900. or  math.isnan(i) or i < 0.3:
             continue
         recoPitchSkim.append(i)


    
     #if len(recoZposSkim) -  len(recoPitchSkim) != 0:
     #    print "Z-Pitch", len(recoZposSkim), len(recoKESkim), len(recoPitchSkim),  len(recoZposSkim) -  len(recoPitchSkim) 

     #if len(recoKESkim) -  len(recoPitchSkim) != 1:
     #    print "KEInc-Pitch", len(recoZposSkim), len(recoKESkim), len(recoPitchSkim),  len(recoKESkim) -  len(recoPitchSkim)   



     if recoZposSkim[-1] < 0.01:
         recoZposSkim  = recoZposSkim[:-1]
         recoPitchSkim = recoPitchSkim[:-1]
     if recoKESkim[-1] < 0.01:
         recoKESkim   = recoKESkim[:-1]

     # calculate weights... we are 1 weight short, so we need to add one
     pitchWeights = [ i/0.47 for i in recoPitchSkim] 
     pitchWeights.append(pitchWeights[len(pitchWeights)-1])
     #for i in xrange(len(recoPitchSkim)):
     #    print i, recoPitchSkim[i], pitchWeights[i]

     #if len(recoZposSkim) - len(recoKESkim) != -1:
     #    print "Off", len(recoZposSkim), len(recoKESkim), len(recoZposSkim) - len(recoKESkim)


     correction = 0
     for i in xrange(len(recoKESkim)):
         if recoKESkim[i] > 1.:
             w = 1
             try:
                 w = pitchWeights[i]
                 if w > 20000:
                     w = pitchWeights[i-1]
                     if w > 20000:
                         print "fuck"
                         w = 1

             except:
                 print "puppa"
                 #pitchWeights[len(pitchWeights)-1]
             
             correction = uncertaintyMomentum*uncertaintyMomentum + uncertaintyELoss*uncertaintyELoss + i*i*uncertaintyEDep*uncertaintyEDep
             correction = TMath.Sqrt(correction)

             hIncidentKE.Fill(recoKESkim[i],w*decisionW)
             hIncidentKEMax.Fill(recoKESkim[i]+correction,w*decisionW)
             hIncidentKEMin.Fill(recoKESkim[i]-correction,w*decisionW)

     if isTrackInteracting:
         if recoKESkim[len(recoKESkim)-1] > 100:
             hInteractingKE.Fill(recoKESkim[len(recoKESkim)-1],decisionW)
             hInteractingKEMax.Fill(recoKESkim[len(recoKESkim)-1]+correction,decisionW)
             hInteractingKEMin.Fill(recoKESkim[len(recoKESkim)-1]-correction,decisionW)



print "counters ", countKeep, countReject, countReject+countKeep
XS      = calculateXSPlot(hInteractingKE   , hIncidentKE    , "XS")
XSMax   = calculateXSPlot(hInteractingKEMax, hIncidentKEMax , "XSMax")
XSMin   = calculateXSPlot(hInteractingKEMin, hIncidentKEMin , "XSMin")



outFile = TFile(outFileName,"recreate")
outFile.cd()

hInteractingKEComp.Write("hInteractingKEComp",TObject.kWriteDelete)  
hIncidentKEComp.Write("hIncidentKEComp",TObject.kWriteDelete)  

hInteractingKE.Write()
hIncidentKE.Write()
hInteractingKEMax.Write()
hIncidentKEMax.Write()
hInteractingKEMin.Write()
hIncidentKEMin.Write()
XS.Write()
XSMax.Write()
XSMin.Write()



outFile.Write()
outFile.Close()


