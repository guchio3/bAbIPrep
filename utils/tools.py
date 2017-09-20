import numpy as np
import json
import sys
import re
from itertools import chain


def lineToValidLists(line, word_dict):
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
            , where the word_dict now is {'-' : 0, '_' : 1, 'where' : 2, 'is' : 3, 'daniel' : 4, '?' : 5}

    Parameters
    ------
    line : a str object which is a line of 1 sentence in the bAbI dataset.
    word_dict : a dictionary which indexes all appearing words to an int number.
        word_dict should be OrderedDict if you wanna make stable dictionary.

    Returns
    ------
    line_id : the ID of the line, which is the first word of each line.
    question_words : a list of int all the elements of which represent
                     words in a question data.
    answer_words : a list of int all the elements of which represent
                   words in a answer data.

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

    # make list from the line string.
    # we remove numbers here, and store only IDs.
    # also, all the words should be lowercase here.
    # in addition, replace s,n,e,w to south,north,east,west based on the DNC paper.
    line_list = re.split(' |\t|,|\n', line)
    line_id = line_list[0]
    direction_dict = {'s': 'south', 'n' : 'north', 'e' : 'east', 'w' : 'west'}
    line_list = [word.lower() if not word.lower() in direction_dict else direction_dict[word.lower()] 
            for word in line_list if not word.isdigit() and not word == '']

    # update word_dict based on this line while storing answer_words for question lines.
    # in addition, make question_words and answer_words using index number.
    answer_flg = False
    question_words = []
    answer_words = []
    for word in line_list:
        if word not in word_dict:
            word_dict[word] = len(word_dict)
        if answer_flg:
            question_words.append(word_dict['-'])
            answer_words.append(word_dict[word])
        else:
            question_words.append(word_dict[word])
            answer_words.append(word_dict['_'])
            if word == '?':
                answer_flg= True

    return line_id, question_words, answer_words


def getOneHots(target_list, dict_size):
    '''
    Make onehot vectors from the target_list.
    Each onehot vectors' dimension is depends on the dict_size.
    
    Parameters
    ------
    target_list : a list of int which represents a word sequence.
    dict_size : the size of the word_dict which is used for the target_list.
                this information is used for the size of onehot vectors.

    Returns
    ------
    one_hots : a sequence of onehot vectors.
    
    '''
    one_hots = np.zeros((len(target_list), dict_size))
    one_hots[np.arange(len(target_list)), target_list] = 1
    return one_hots


def saveReversedDict(word_dict, target_dir):
    '''
    Save word_dict in the reverse form.
    This is for understanding the output of models which is 
    a sequence of onehot vectors.
    The reverse dictionary is saved in json format.

    NOTE : Each story is not saved in the onehot format but in index format.
    
    Parameters
    ------
    word_dict : the word_dict which is made from datasets.
    target_dir : a str object that specify the target directory 
        in which you wanna save the reversed_dict.

    '''
    with open(target_dir, 'w') as fout:
        reversed_dict = dict(zip(word_dict.values(), word_dict.keys()))
        fout.write(json.dumps(reversed_dict))


def prepBAbI(source_files, target_dir):
    '''
    the batch size of this dataset is fixed to 1 based on the DNC paper.
    
    Parameters
    ------
    source_files : a list of str all the elements of which specify
                   the names of source bAbI data files. 
    target_dir : a str object which specifies the target directory in which
                  you wanna save the preprocessed bAbI dataset. 
                  the preprocessed bAbI dataset is saved in json format.
    
    Returns
    ------
    word_dict : a dictionary which indexes all appearing words to an int number.
        word_dict should be OrderedDict if you wanna make stable dictionary.
    
    '''
    if not isinstance(source_files, list):
        sys.exit('ERROR : source_files must be list object.')
    if not isinstance(target_dir, str):
        sys.exit('ERROR : target_dir must be str object.')
    if target_dir[-1] != '/':
        target_dir += '/'

    
    # prepare for dataset conversion
    word_dict = {'_' : 0, '-' : 1}
    question_stories = []
    answer_stories = []
    
    # start dataset conversion.
    # this for loop is for getting question_stories and answer_stories.
    # this program loads all stories on memory once, but it's OK because
    # even the biggest data in the bAbI dataset has only 4.2M.
    for source_file in source_files:
        print('Parsing stories of %s' % source_file)
        fin = open(source_file, 'r')
        line = fin.readline()

        former_id = 0
        question_story = []
        answer_story = []
        question_stories = []
        answer_stories = []
        while(line):
            line_id, question_words, answer_words = lineToValidLists(line, word_dict)
            if former_id < int(line_id):
                question_story.append(question_words)
                answer_story.append(answer_words)
            else:
                # merge words in one story
                question_stories.append([word for sentence in question_story for word in sentence])
                answer_stories.append([word for sentence in answer_story for word in sentence])
                question_story = [question_words]
                answer_story = [answer_words]
    
            former_id = int(line_id)
            line = fin.readline()

        print('Saving stories of %s' % source_file)
        out_filename = target_dir + source_file.split('/')[-1].split('.')[0] + '.json'
        fout = open(out_filename, 'w')
        for question_story, answer_story in zip(question_stories, answer_stories):
            fout.write(json.dumps([[question_story], [answer_story]]) + '\n')

    # save reversed_dict to the specified file.
    # this is used when we understand the inputs and outputs
    # which are used for experiments.
    dict_file = target_dir + 'dict.json'
    print('Generating dictionary at %s' % dict_file)
    saveReversedDict(word_dict, dict_file)
