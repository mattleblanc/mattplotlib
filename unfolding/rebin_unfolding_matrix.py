"""
rebin_unfolding_matrix.py
Matt LeBlanc (CERN) <matt.leblanc@cern.ch>

The idea is to find a good binning for an observable you want to unfold.
The input I give is an unfolding matrix with binning that is way too fine --
this script then iteratively rebins the matrix so that the diagonal always has >=args.desiredFrac of entries.

It should add the two entries together which have a sum closest to args.desiredFrac in each step, unless there is
one which has 0 entries.

There are probably better ways to do this.

"""

import os
import argparse
import math
import string
import random

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetOptTitle(False)
ROOT.gStyle.SetLegendBorderSize(0);
ROOT.gStyle.SetPalette(112)

global canvas, canvas
canvas = ROOT.TCanvas('draw1', 'draw1', 0, 0, 800, 800)
canvas.SetLeftMargin(0.15)
canvas.SetRightMargin(0.15)
canvas.cd()

l=ROOT.TLatex()
l.SetNDC()
l.SetTextFont(72)
l.SetTextSize(0.04)
p=ROOT.TLatex()
p.SetNDC();
p.SetTextFont(42)
p.SetTextSize(0.04)

def truncate(n):
        return int(n * 1000) / 1000

def conditionY(h2):
        for iBinY in range(1, h2.GetNbinsY()+1):
            htmp = h2.ProjectionX("blah_h2_"+str(iBinY), iBinY+1, iBinY+1)
            bin1 = 0
            bin2 = htmp.GetNbinsX()
            sf = -1.
            if(htmp.Integral(bin1,bin2)!=0): sf = 1./htmp.Integral(bin1,bin2)
            for iBinX in range(0, h2.GetNbinsX()):
                h2.SetBinContent(iBinX+1,iBinY+1, math.fabs(h2.GetBinContent(iBinX+1, iBinY+1)*sf))
        return h2

def conditionX(h2):
        for iBinX in range(1, h2.GetNbinsX()+1):
            htmp = h2.ProjectionY("blah_h2_"+str(iBinX), iBinX+1, iBinX+1)
            bin1 = 0
            bin2 = htmp.GetNbinsY()
            sf = -1.
            if(htmp.Integral(bin1,bin2)!=0): sf = 1./htmp.Integral(bin1,bin2)
            for iBinY in range(0, h2.GetNbinsY()):
                h2.SetBinContent(iBinX+1,iBinY+1, math.fabs(h2.GetBinContent(iBinX+1, iBinY+1)*sf))
        return h2

def combine(h2, desiredFrac, bins):
    again=True

    max_pair_value = 0
    max_pair_index = -1
    zero_bins = False
    for iBinX in range(1, h2.GetNbinsX()-1):
        for iBinY in range(1, h2.GetNbinsY()-1):
            if(iBinX!=iBinY): continue

            integral1 = h2.Integral(1, h2.GetNbinsX(),   iBinY,   iBinY)
            integral2 = h2.Integral(1, h2.GetNbinsX(),   iBinY+1, iBinY+1)
            
            if(integral1==0 or integral2==0): zero_bins = True
            
            #print(iBinX, h2.GetBinContent(iBinX,iBinY))

            if(zero_bins):
                if(integral1==0):
                        max_pair_value = 0.
                        max_pair_index = iBinX
                if(integral2==0):
                        max_pair_value = 0.
                        max_pair_index = iBinX+1
                #print("merge zero bins!",max_pair_index)
            elif(h2.GetBinContent(iBinX,iBinY) < desiredFrac and not zero_bins):
                if( abs( desiredFrac - ( h2.GetBinContent(iBinX,iBinY) + h2.GetBinContent(iBinX+1,iBinY+1) ) ) > max_pair_value ):
                    max_pair_value = h2.GetBinContent(iBinX,iBinY) + h2.GetBinContent(iBinX+1,iBinY+1)
                    max_pair_index = iBinX
                    
    if(max_pair_index<0):
        again=False

    if(again):
        print("Merge bins:\t"+str(max_pair_index)+"\t("+str(h2.GetBinContent(max_pair_index,max_pair_index))+" entries)\t"+str(max_pair_index+1)+"\t("+str(h2.GetBinContent(max_pair_index+1,max_pair_index+1))+" entries)")

        letters = string.ascii_uppercase
        histo_str = (''.join(random.choice(letters) for i in range(10)))
                       
        # declare the new histogram, with one bin fewer
        h2_new = ROOT.TH2D("h2_"+histo_str, "h2_"+histo_str, h2.GetNbinsX()-1, 0, h2.GetNbinsX()-1, h2.GetNbinsY()-1, 0, h2.GetNbinsY()-1)
        for iBinX in range(1, h2.GetNbinsX()-1):
            for iBinY in range(1, h2.GetNbinsY()-1):
                
                # logic
                x_is_lower  = (iBinX <  max_pair_index)
                x_is_merged = (iBinX == max_pair_index)
                x_is_higher = (iBinX >= (max_pair_index+1))
                
                y_is_lower  = (iBinY <  max_pair_index)
                y_is_merged = (iBinY == max_pair_index)
                y_is_higher = (iBinY >= (max_pair_index+1))

                # if x and y are lower than the merged bin, it should be the same as the old histogram

                summed_content = 0.
                if( x_is_merged and not y_is_merged ):
                    summed_content = h2.GetBinContent(iBinX,iBinY)+h2.GetBinContent(iBinX+1,iBinY)
                elif( y_is_merged and not x_is_merged ):
                    summed_content = h2.GetBinContent(iBinX,iBinY)+h2.GetBinContent(iBinX,iBinY+1)
                elif( y_is_merged and x_is_merged ):
                    summed_content = h2.GetBinContent(iBinX,iBinY)
                    summed_content += h2.GetBinContent(iBinX,iBinY+1)
                    summed_content += h2.GetBinContent(iBinX+1,iBinY)
                    summed_content += h2.GetBinContent(iBinX+1,iBinY+1)      
                elif( x_is_lower and y_is_lower):
                    summed_content = h2.GetBinContent(iBinX,iBinY)
                elif( x_is_higher and y_is_lower):
                    summed_content = h2.GetBinContent(iBinX+1,iBinY)
                elif( x_is_lower and y_is_higher):
                    summed_content = h2.GetBinContent(iBinX,iBinY+1)
                elif( x_is_higher and y_is_higher):
                    summed_content = h2.GetBinContent(iBinX+1,iBinY+1)

                h2_new.SetBinContent(iBinX,
                                     iBinY,
                                     summed_content)
        h2_new.Print()
        del bins[max_pair_index]
        print(bins)
        return h2_new,again
    else:
        again=False
        print("Not again!")
        return h2,again
        
    # shouldn't get here
    assert(1==0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--inFile", dest='inFile', default="", required=True, help="Input file.")
    parser.add_argument("--inMatrix", dest='inMatrix', default="h2_unfolding_resp_jet_m_pt", help="Input histo.")
    parser.add_argument("--outDir", dest='outDir', default="", help="Output directory.")
    parser.add_argument("--xtitle", dest='xtitle', default="", required=False, help="x-axis title.")
    parser.add_argument("--ytitle", dest='ytitle', default="", required=False, help="x-axis title.")
    parser.add_argument("--desiredFrac", dest='desiredFrac', type=float, help="what % of entries on diagonal?")
    parser.add_argument("--rebin", dest='rebin', default=1, type=int, help="initial rebinning factor")
    parser.add_argument("--minValue", dest='minValue', default=0., type=float, help="what is the minimum observable value for this matrix?")
    parser.add_argument("--maxValue", dest='maxValue', default=1., type=float, help="what is the maximum observable value for this matrix?")
    args = parser.parse_args()

    the_file = ROOT.TFile.Open(args.inFile)
    h2 = the_file.Get(args.inMatrix)
    assert(h2)

    h2.Print()

    h2.Rebin2D(args.rebin,args.rebin)
    h2 = conditionY(h2)

    print(h2.GetNbinsX(), h2.GetNbinsY())
    assert(h2.GetNbinsX()==h2.GetNbinsY())

    bins = []
    temp_h1 = ROOT.TH1F("temp_for_binning", "temp_for_binning", h2.GetNbinsX(), args.minValue, args.maxValue)
    for the_bin in range(1,temp_h1.GetNbinsX()+1) :
        bins.append(truncate(temp_h1.GetBinLowEdge(the_bin)))

    print(bins)

    nIterations = 0
    again=True
    while again==True:
        print("Iteration "+str(nIterations)+"\t"+h2.GetTitle())
        
        h2.SetMinimum(0.)
        h2.SetMaximum(1.)

        h2.GetXaxis().SetTitle(args.xtitle)
        h2.GetYaxis().SetTitle(args.ytitle)
        h2.Draw("COLZ")
        
        l.DrawLatex(0.15,  0.905, "ATLAS")
        p.DrawLatex(0.285, 0.905, "Simulation Internal")
        ROOT.gPad.RedrawAxis()

        if(nIterations<10):                       
            canvas.SaveAs(args.outDir+"00"+str(nIterations)+".pdf")
            canvas.SaveAs(args.outDir+"00"+str(nIterations)+".png")
        elif(nIterations>=10 and nIterations<100): 
            canvas.SaveAs(args.outDir+"0"+str(nIterations)+".pdf")
            canvas.SaveAs(args.outDir+"0"+str(nIterations)+".png")
        else:
            canvas.SaveAs(args.outDir+str(nIterations)+".pdf")
            canvas.SaveAs(args.outDir+str(nIterations)+".png")

        nIterations+=1
        h2,again = combine(conditionY(h2),args.desiredFrac, bins)

    print("Final binning:")
    print(bins)
    print("All done!")
