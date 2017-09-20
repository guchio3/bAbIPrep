import os
import sys
import argparse

from utils.tools import prepBAbI


def getArgs():
    '''
    Set all args as they are utilized by this scripts.

    You can see detailed explanations of each args by
    the command of
    > 'python prepBAbI.py -h'.
        
    '''
    parser = argparse.ArgumentParser(description="The script which preprocess bAbI dataset \
        to vector type usable form.")
    parser.add_argument("-s", "--source_dir", help="the source directory in which you have \
            bAbI datasets.", required=True)
    parser.add_argument("-t", "--target_dir", help="the target directory in which you wanna \
            save preprocessed dataset.", required=True)
    args = parser.parse_args() 
    if args.source_dir[-1] != '/':
        args.source_dir += '/'
    if args.target_dir[-1] != '/':
        args.target_dir += '/'

    return args


def main():
    args = getArgs()
    source_files = [args.source_dir + source_file for source_file in os.listdir(args.source_dir)]
    prepBAbI(source_files, args.target_dir)


if __name__ == '__main__':
    main()
