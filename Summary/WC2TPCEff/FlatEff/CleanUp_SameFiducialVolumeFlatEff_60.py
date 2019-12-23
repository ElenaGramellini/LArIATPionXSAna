from ROOT import *
import ROOT as root
import numpy as np
import math
import argparse
import os

#gStyle.SetOptStat(0)
def calculateXSPlot(InteractingHisto, IncidentHisto, Name  ):
    XS1 =  InteractingHisto.Clone(Name)
   # XS.Sumw2()
   # IncidentHisto.Sumw2()
    XS1.Scale(101.10968)
    XS1.Divide(IncidentHisto)
    return XS1


#Get Input File
parser = argparse.ArgumentParser()
parser.add_argument("eff"    , nargs='?', default =  0.5   , type = float, help="root folder name")
parser.add_argument("ZMax"   , nargs='?', default =  86.   , type = float, help="root folder name")
parser.add_argument("XMin"   , nargs='?', default =   1.   , type = float, help="root folder name")
parser.add_argument("XMax"   , nargs='?', default =  46.   , type = float, help="root folder name")
parser.add_argument("YMin"   , nargs='?', default = -19.   , type = float, help="root folder name")
parser.add_argument("YMax"   , nargs='?', default =  19.   , type = float, help="root folder name")
parser.add_argument("fileName"     , nargs='?', default = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/AngleCut_0deg_histo_60A.root", type = str, help="insert fileName")
parser.add_argument("folderName"   , nargs='?', default = "AngleCutTrueXS"              , type = str, help="root folder name")



args    = parser.parse_args()
inFileName   = args.fileName
folder_Name  = args.folderName

eff  = args.eff
XMin = args.XMin
YMin = args.YMin
XMax = args.XMax
YMax = args.YMax
ZMax = args.ZMax

outFileName = "FlatEff"+str(eff)+"SameFidVol_Z"+str(ZMax)+"_"+str(YMax)+"_"+str(YMin)+"_"+str(XMax)+"_"+str(XMin)+"60.root"
print outFileName , " ------------------------------------- "

f      = root.TFile(inFileName)
myTree = f.Get(folder_Name+"/effTree")

# These come directly from the inputFile
hInteractingKEComp = f.Get(folder_Name+"/hInteractingKE")
hIncidentKEComp    = f.Get(folder_Name+"/hIncidentKE")


hInteractingKE   = TH1D("hInteractingKE","hInteractingKE" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE      = TH1D("hIncidentKE"   ,"hIncidentKE"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

hDistancePre  = TH1D("hDistancePre"   ,"hDistancePre" , 1000, 0,100)
hDistancePost = TH1D("hDistancePost"  ,"hDistancePost", 1000, 0,100)

hLastZ      = TH1D("hLastZ"   ,"hLastZ" , 1000, 0,100)

countReject = 0
countKeep   = 0

print myTree.GetEntry()
sillyCount =0 
for entry in myTree:
     sillyCount += 1
     if not sillyCount % 10000:
          print sillyCount
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     eventN              = entry.eventN
     recoIncidentKE      = entry.simRecoIncidentKE
     trueEndX            = entry.trueEndX
     trueEndY            = entry.trueEndY
     trueEndZ            = entry.trueEndZ
     trueVtxX            = entry.trueVtxX
     trueVtxY            = entry.trueVtxY
     trueVtxZ            = entry.trueVtxZ
     recoIncidentX       = entry.simRecoXPosition
     recoIncidentY       = entry.simRecoYPosition
     recoIncidentZ       = entry.simRecoZPosition
     hLastZ.Fill(trueEndZ)
     recoKESkim = []

     distance = TMath.Sqrt((trueEndX-trueVtxX)*(trueEndX-trueVtxX) + (trueEndY-trueVtxY)*(trueEndY-trueVtxY) + (trueEndZ-trueVtxZ)*(trueEndZ-trueVtxZ) )
     hDistancePre.Fill(distance)
     if np.random.random_sample() > eff:
         continue
     hDistancePost.Fill(distance)

     for i in xrange(len(recoIncidentKE)):
         e = recoIncidentKE[i]
         if e > 0:
             thisX = recoIncidentX[i]
             thisY = recoIncidentY[i]
             thisZ = recoIncidentZ[i]
             if thisZ > ZMax or thisY > YMax or thisY < YMin or thisX < XMin or thisX > XMax:
                 continue
             hIncidentKE.Fill(e)
             recoKESkim.append(e)
     
     if trueEndZ > ZMax or trueEndY > YMax or trueEndY < YMin or trueEndX < XMin or trueEndX > XMax:
            continue

     if len(recoKESkim):
         hInteractingKE.Fill( recoKESkim[len(recoKESkim)-1] )
         

XS  = calculateXSPlot(hInteractingKE   , hIncidentKE    , "XS")



outFile = TFile(outFileName,"recreate")
outFile.cd()

hInteractingKEComp.Write("hInteractingKEComp",TObject.kWriteDelete)  
hIncidentKEComp.Write("hIncidentKEComp",TObject.kWriteDelete)  

hInteractingKE.Write()
hIncidentKE.Write()
XS.Write()
hLastZ.Write()
hDistancePre.Write()
hDistancePost.Write()

outFile.Write()
outFile.Close()

