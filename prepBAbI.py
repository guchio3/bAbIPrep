import os
import sys
import argparse


def getArgs(){
    '''
    Set all args as they are utilized by this scripts.

    You can see detailed explanations of each args by
    the command of
    > 'python prepBAbI.py -h'.
        
    '''
    parser = argparse.ArgumentParser(description="")    
    parser.add_argument("", "", help="", required=True)
    args = parser.parse_args() 

    return args
}


def removeNums(line){
    for 
}


def toLowerCase(lineList){
    for word in lineList:

    if !isinstance(word, str):
        sys.exit('ERROR : you can not convert non-str objects to lowercase.')
    return word.lower()
}


def toValidForm(line){
 '''
 Change the input line to valid form.

 Valid form here means that it fills the requirements below.
 * Without numbers
 * 
 
 '''

}


def getIndex(fin){
        a
}

























def main():
    args = getArgs()




if __name__ == '__main__':
    main()
