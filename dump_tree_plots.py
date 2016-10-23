import glob
import os
from optparse import OptionParser

import ROOT
from ROOT import gROOT,gPad,gStyle,TCanvas,TFile,TLine,TLatex,TAxis,TLegend,TPostScript

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetOptTitle(False)
ROOT.gStyle.SetLegendBorderSize(0);

canvas = ROOT.TCanvas('draw', 'draw', 0, 0, 1400, 1050)
pad = ROOT.TPad()
canvas.cd()

parser = OptionParser()

parser.add_option("--input", help="Input NTUPs (flat trees!)", default="${ROOTCOREBIN}/../input/")
parser.add_option("--output", help="Directory for output files", default="${ROOTCOREBIN}/../output/")
parser.add_option("--tree", help="Tree name in input NTUPs", default="CollectionTree")
parser.add_option("--weight", help="Event-by-event weight string", default="")
parser.add_option("--label", help="Output file label string", default="label")
parser.add_option("--verbose", action='store_true', help="Verbose output? Default is False", default=False)

(options, args) = parser.parse_args()

print 'mattplotlib\tdump_tree_plots.py\t'+options.input
signal_infiles = glob.glob(options.input)
if options.verbose : print signal_infiles

for file in signal_infiles :

	signal_input = ROOT.TFile.Open(file)
	filename = signal_input.GetName()

	signal_tree = signal_input.Get(options.tree)
	weight = options.weight

	for branch in signal_tree.GetListOfBranches() :

		signal_tree.Draw(branch.GetName(),'(1==1)*'+weight)

		canvas.SaveAs(options.output+options.label+'_'+branch.GetName()+'.pdf')
		canvas.SaveAs(options.output+options.label+'_'+branch.GetName()+'.root')

print 'mattplotlib\tdump_tree_plots.py\tdone!'
