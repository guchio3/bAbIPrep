import os
import sys
import argparse

from utils import *


def getArgs():
    '''
    Set all args as they are utilized by this scripts.

    You can see detailed explanations of each args by
    the command of
    > 'python prepBAbI.py -h'.
        
    '''
    parser = argparse.ArgumentParser(description="The script which preprocess bAbI dataset \
        to vector type usable form.")
    parser.add_argument("-i", "--input_file", help="", required=True)
    args = parser.parse_args() 

    return args


def main():
    args = getArgs()


if __name__ == '__main__':
    main()
