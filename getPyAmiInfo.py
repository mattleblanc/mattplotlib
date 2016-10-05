# getPyAmiInfo.py
# Retrieves XS, FE and raw nEvents for a list of samples
#
# Set up pyami first
# > lsetup pyami
#
# Then e.g.
# python ~/mattplotlib/getPyAmiInfo.py --input rcRes/data/Samples_JZW_p2794-pythia.list --output 20p7
#

# This script based on one from Kate Pachal -- what a cool person!

import os
import subprocess
from optparse import OptionParser
import datetime
import pyAMI.client
import pyAMI.atlas.api as AtlasAPI
import csv

parser = OptionParser()
parser.add_option("--input", help="Input list of datasets", default="")
parser.add_option("--output", help="String to identify output file", default="")
(options, args) = parser.parse_args()

client = pyAMI.client.Client('atlas')
AtlasAPI.init()

outFileTag = options.output
inFileList = options.input

containers = [line.rstrip('\n') for line in open(inFileList)]
mydict = {}
for dataset in containers :

    command = "rucio list-dids --short {0}".format(dataset)
    inDS = subprocess.check_output(command,shell=True)
    inDS = inDS.strip()
    inDS = inDS.split(":")[1]

    items = inDS.split(".")
    tag = items[-1].split("_")[0]
    evntDS = ".".join(items[:-3] + ['evgen', 'EVNT', tag])

    tokens = dataset.split(".")
    mystr = tokens[2].split("_")[-1]
    numbers = ""
    for character in mystr:
      if character.isdigit() :
        numbers = numbers+character

    tag = "JZ{0}W".format(numbers)

    info = AtlasAPI.get_dataset_info(client, evntDS)[0]

    infoDict = {}
    infoDict['crossSection'] = info['crossSection_max']
    infoDict['filterEff'] = info['GenFiltEff_mean']
    infoDict['nEvt'] = info['totalEvents']

    print infoDict
    mydict[tag] = infoDict

outfile = "pyAMIInfoForFiles_{0}.py".format(outFileTag)
w = open(outfile, "w")
w.write("amiInfoDict = {\n")
for key, val in sorted(mydict.items()) :
  w.write("'{0}'".format(key)+" : "+ "{" )
  for ikey,ival in val.items() :
    w.write("'{0}' : {1}, ".format(ikey,ival))
  w.write("},\n")
w.write("}")

print "Done."
