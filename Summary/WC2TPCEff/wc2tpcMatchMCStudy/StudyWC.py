from ROOT import *
import ROOT as root
import numpy as np
import math
import argparse
import os


#Get Input File
parser = argparse.ArgumentParser()
parser.add_argument("fileName"     , nargs='?', default = "/Users/elenag/Documents/Papers/ThatsIt/code/TrueTree/secondTry/EffCorrection/AngleCut_5deg_histo_100A.root", type = str, help="insert fileName")
parser.add_argument("folder_Name"          , nargs='?', default = ""              , type = str, help="root folder name")
parser.add_argument("set"          , nargs='?', default = "100"              , type = str, help="root folder name")
parser.add_argument("qualifier"    , nargs='?', default = "Before"           , type = str, help="root folder name")

args         = parser.parse_args()
inFileName   = args.fileName
set          = args.set
qualifier    = args.qualifier
folder_Name  = args.folder_Name


outFileName = "Lenths_"+qualifier+"WC2TPC_"+set+"A.root"
print outFileName , " ------------------------------------- "

f      = root.TFile(inFileName)
myTree = f.Get(folder_Name+"/effTree")

hDistancePre  = TH1D("hTrackLenghtTrue"   ,"hDistancePre" , 1000, 0,100)
hLastZ        = TH1D("hLastZTrue"         ,"hLastZ" , 1000, 0,100)

countReject = 0
countKeep   = 0

print myTree.GetEntry()
sillyCount =0 
for entry in myTree:
     sillyCount += 1
     if not sillyCount % 10000:
          print sillyCount
     # Now you have acess to the leaves/branches of each entry in the tree, e.g.
     trueEndX            = entry.trueEndX
     trueEndY            = entry.trueEndY
     trueEndZ            = entry.trueEndZ
     trueVtxX            = entry.trueVtxX
     trueVtxY            = entry.trueVtxY
     trueVtxZ            = entry.trueVtxZ
     hLastZ.Fill(trueEndZ)
     distance = TMath.Sqrt((trueEndX-trueVtxX)*(trueEndX-trueVtxX) + (trueEndY-trueVtxY)*(trueEndY-trueVtxY) + (trueEndZ-trueVtxZ)*(trueEndZ-trueVtxZ) )
     hDistancePre.Fill(distance)


outFile = TFile(outFileName,"recreate")
outFile.cd()
hLastZ.Write()
hDistancePre.Write()

outFile.Write()
outFile.Close()

