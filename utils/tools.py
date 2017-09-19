import json
import numpy as np


def lineToValidLists(line, wordDict):
    '''
    Change the input line to valid form while storing words to the word set.
    This function returns 

    Valid form here means that it fills the requirements below.
        * Symbols '.' and '?' are dealt as separated
        * Space or tab (' ' or '\t') separated list
        * Without numbers
        * With only lowercases
        ex) 
         input : '15 Where is Daniel? 	office	10', {'-' : 0, '_' : 1}
         output : 15 (int), ['where', 'is', 'daniel', '?', '-'], ['_', '_', '_', '_', 'office']
            , where the wordDict now is {'-' : 0, '_' : 1, 'where' : 2, 'is' : 3, 'daniel' : 4, '?' : 5}

    Parameters
    ------
    line : a str object which is a line of 1 sentence in the bAbI dataset.
    wordSet : a set of the word which appears in the dataset.
        wordDict should be OrderedDict if you wanna make stable dictionary.

    Returns
    ------
    lineID : the ID of the line, which is the first word of each line.
    questions : 
    answers : 

    '''
    # to deal '.' and '?' as a word, put ' ' before them
    for i, char in enumerate(line[::-1]):
        if char in ['.', '?']:
            line = line[:len(line) - 1 - i] + ' ' + line[len(line) - 1 - i:]
            # put 2 assumptions
            #   * that there only 1 '.' or '?' in a line.
            #   * that there are no \t before '.' and '?'.
            # this is for speeding up
            break

    # make list from the line string
    # we remove numbers here, and store only IDs
    lineList = line.split()
    lineID = lineList[0]
    lineList = lineList[1:-1] if lineList[-1].isdigit() else lineList[1:]

    # update wordDict based on this line while storing answers for question lines.
    # in addition, make questions and answers using index number.
    answer_flg = False
    questions = []
    answers = []
    for word in lineList:
        if word not in wordDict:
            wordDict[word] = len(wordDict)
        if answer_flg:
            questions.append(wordDict['-'])
            answers.append(wordDict[word])
        else:
            questions.append(wordDict[word])
            answers.append(wordDict['_'])
            if word == '?':
                answer_flg= True

    return lineID, questions, answers


def saveReversedDict(wordDict, targetDir):
    '''
    Save wordDict in the reverse form.
    This is for understanding the output of models which is 
    a sequence of onehot vectors.

    The reverse dictionary is saved in json format.
    
    Parameters
    ------
    wordDict : the wordDict which is made from datasets.
    targetDir : the target directory in which you wanna 
        save the reversedDict.

    '''
    with open(targetDir, 'w') as fout:
        reversedDict = dict(zip(wordDict.values(), wordDict.keys()))
        font.write(json.dumps(reversedDict))


def getOneHots(targetList, dictSize):
    '''
    
    Parameters
    ------
    targetList : a list of int which represents a word sequence.
    dictSize : the size of the wordDict which is used for the targetList.
        this information is used for the size of onehot vectors.

    Returns
    ------
    oneHots : a sequence of onehot vectors.
    
    '''
    oneHots = np.zeros((len(targetList), dictSize))
    oneHots[np.arange(len(targetList)), targetList] = 1
    return oneHots
