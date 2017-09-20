# in the root directory of this repository, run
# > PYTHONPATH=. python testCodes/test1.py

from utils.tools import *
import os
import sys

source_dir = 'datasets/en-valid-10k/'
target_dir = 'datasets/preped/'
source_files = [source_dir + source_file for source_file in os.listdir(source_dir)]

prepBAbI(source_files, target_dir)
