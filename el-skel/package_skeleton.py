#!/usr/bin/env python

'''
mattplotlib/el-skel/package_skeleton.py
Make an empty package skeleton.

This is meant to replace the old
rc make_skeleton MyAnalysis
(for lazy people)

Matt LeBlanc <matt.leblanc@cern.ch> 2017/01/31
'''

import os
import logging
from optparse import OptionParser

logging.basicConfig(level=logging.INFO)

parser = OptionParser()

###
# options
# job configuration
parser.add_option("--package", help="What is your package going to be named?", default="MyAnalysis")

(options, args) = parser.parse_args()

if(not os.path.exists(options.package)):
    os.system('mkdir '+options.package)
    os.system('mkdir '+options.package+'/Root')
    os.system('mkdir '+options.package+'/'+options.package)
    os.system('ls -l '+options.package)
    logging.info("Done!")
else:
    logging.info("This path exists! Aborting.")
