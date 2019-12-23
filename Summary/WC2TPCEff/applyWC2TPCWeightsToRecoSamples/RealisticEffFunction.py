from ROOT import *
import ROOT as root
import numpy as np
import math
import argparse
import os


#mode = 0 for 100A
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


