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

parser.add_argument("ZMax"   , nargs='?', default =  86.   , type = float, help="root folder name")
parser.add_argument("XMin"   , nargs='?', default =   1.   , type = float, help="root folder name")
parser.add_argument("XMax"   , nargs='?', default =  46.   , type = float, help="root folder name")
parser.add_argument("YMin"   , nargs='?', default = -19.   , type = float, help="root folder name")
parser.add_argument("YMax"   , nargs='?', default =  19.   , type = float, help="root folder name")
parser.add_argument("fileName"     , nargs='?', default = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/AngleCut_0deg_histo_100A.root", type = str, help="insert fileName")
parser.add_argument("folderName"   , nargs='?', default = "AngleCutTrueXS"              , type = str, help="root folder name")



args    = parser.parse_args()
inFileName   = args.fileName
folder_Name  = args.folderName

XMin = args.XMin
YMin = args.YMin
XMax = args.XMax
YMax = args.YMax
ZMax = args.ZMax

outFileName = "SameFidVol_Z"+str(ZMax)+"_"+str(YMax)+"_"+str(YMin)+"_"+str(XMax)+"_"+str(XMin)+"100.root"
print outFileName , " ------------------------------------- "

f      = root.TFile(inFileName)
myTree = f.Get(folder_Name+"/effTree")

# These come directly from the inputFile
hInteractingKEComp = f.Get(folder_Name+"/hInteractingKE")
hIncidentKEComp    = f.Get(folder_Name+"/hIncidentKE")


hInteractingKE   = TH1D("hInteractingKE","hInteractingKE" , hInteractingKEComp.GetSize()-2, hInteractingKEComp.GetXaxis().GetXmin(),  hInteractingKEComp.GetXaxis().GetXmax())
hIncidentKE      = TH1D("hIncidentKE"   ,"hIncidentKE"    , hIncidentKEComp.GetSize()   -2, hIncidentKEComp.GetXaxis().GetXmin()   ,  hIncidentKEComp.GetXaxis().GetXmax()   )

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
     recoIncidentX       = entry.simRecoXPosition
     recoIncidentY       = entry.simRecoYPosition
     recoIncidentZ       = entry.simRecoZPosition
     hLastZ.Fill(trueEndZ)
     recoKESkim = []

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

outFile.Write()
outFile.Close()


'''
 run             = 1
 subrun          = 2
 eventN          = 501
 trueVtxX        = 17.1338
 trueVtxY        = 4.25294
 trueVtxZ        = 3.37508e-15
 trueEndX        = 12.0567
 trueEndY        = 6.64441
 trueEndZ        = 90
 finalKE         = 556.778
 ntruePts        = 1000
 simRecoIncidentKE = 734.557, 
                  733.83, 733.126, 731.58, 731.028, 730.086, 
                  728.768, 727.995, 727.14, 725.757, 725.03, 
                  724.138, 723.3, 722.44, 721.713, 720.901, 
                  719.786, 718.745, 717.863, 716.817
 simRecoXPosition  = 17.1074, 
                  17.0809, 17.0544, 17.028, 17.0015, 16.975, 
                  16.9486, 16.9221, 16.8957, 16.8692, 16.8427, 
                  16.8163, 16.7898, 16.7633, 16.7369, 16.7104, 
                  16.684, 16.6575, 16.631, 16.6046
 simRecoYPosition  = 4.26541, 
                  4.27787, 4.29034, 4.3028, 4.31527, 4.32773, 
                  4.3402, 4.35266, 4.36513, 4.37759, 4.39005, 
                  4.40252, 4.41498, 4.42745, 4.43991, 4.45238, 
                  4.46484, 4.47731, 4.48977, 4.50224
 simRecoZPosition  = 0.469089, 
                  0.938178, 1.40727, 1.87636, 2.34544, 2.81453, 
                  3.28362, 3.75271, 4.2218, 4.69089, 5.15998, 
                  5.62907, 6.09816, 6.56724, 7.03633, 7.50542, 
                  7.97451, 8.4436, 8.91269, 9.38178
 G4Process       = (vector<string>*)0x7ff926d8ca00
'''
