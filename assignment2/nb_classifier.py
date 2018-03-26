#!/usr/bin/env python3

import sys, string, math
from os import listdir
from os.path import join, isfile

import nltk
nltk.download('stopwords')
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords

from util import send_stdout, progress
from util import STEMMER, Token_Preprocessing_Engine

# Global variables
INDEX_FILENAME = 'index'
HAM = 'ham'; SPAM = 'spam'


def read_index_file(file_path):
    class_index = {}
    f = open(file_path, 'r')
    f_text = f.readlines()
    f.close()
    for entry in f_text:
        try:
            c, email = entry.split()
        except ValueError:
            send_stdout("Invalid index format {}, skipped.".format(entry))
            continue
        if c not in [HAM, SPAM]:
            send_stdout("Invalid index format {}, skipped.".format(entry))
            continue
        class_index[email] = c
    return class_index


# Extract vocabulary from email corpus, and remove stop words and punctuation
def extract_vocabulary(D):
    V = set()
    # get set of stopwords and punctuation
    stop_words_punct = set(stopwords.words('english')) | set(string.punctuation)
    # collect all vocabulary from corpus
    for d in D:
        text = D[d]
        text_tokens = wordpunct_tokenize(text)
        filtered_v = [w for w in text_tokens if not w in stop_words_punct]
        V.update(filtered_v)
    return V


def count_docs_in_class(Index, D, c):
    count = 0
    for d in D:
        if Index[d] == c:
            count += 1
    return count


def count_tokens_of_term(Index, D, c, V):
    Tc = {}
    # initialize T_ct to zero for all terms in V
    for t in V:
        Tc[t] = 0
    # count tokens of all terms in doc(email) that is classified in 'c'
    for doc_name in D:
        if Index[doc_name] == c:
            text = D[doc_name]
            for t in wordpunct_tokenize(text):
                if t in V:
                    if t not in Tc:
                        Tc[t] = 0
                    Tc[t] += 1
    return Tc


# Naive Bayes algorithm in Figure 13.2 of the textbook (Training part)
def train_multinomial_NB(Index, D):
    prior = {}
    condprob = {}
    # V <- EXTRACTVOCABULARY(D)
    send_stdout('\t extracting vocabulary ...')
    V = extract_vocabulary(D)
    # N <- COUNTDOCS(D)
    N = len(D)
    for c in [HAM, SPAM]:
        send_stdout('\t counting docs in class "{}" ...'.format(c))
        Nc = count_docs_in_class(Index, D, c)
        prior[c] = Nc/N

        send_stdout('\t counting tokens of term in class "{}" ...'.format(c))
        Tc = count_tokens_of_term(Index, D, c, V)

        # calcuate condprob
        send_stdout('\t calcuating condprob in class "{}" ...'.format(c))
        denominator = 0
        for t_prime in V:
            denominator += (Tc[t_prime] + 1)
        for t in V:
            numerator = Tc[t] + 1
            condprob[(c, t)] = numerator / denominator
    return V, prior, condprob


# Extract tokens from document
def extract_tokens_from_doc(V, d):
    W = set()
    for tokens in wordpunct_tokenize(d):
        if tokens in V:
            W.add(tokens)
    return W


# Naive Bayes algorithm in Figure 13.2 of the textbook (testing part)
def apply_multinomial_NB(V, prior, condprob, d):
    score = {}
    W = extract_tokens_from_doc(V, d)
    for c in [HAM, SPAM]:
        score[c] = math.log(prior[c])
        for t in W:
            score[c] += math.log(condprob[(c, t)])
    # arg max c in C score[c]
    if score[HAM] > score[SPAM]:
        return HAM
    else:
        return SPAM


# Open documents from disk, and store in memory(in python dictionary)
def read_emails(dir, files, index):
    D = {}
    for file in files:
        if file in index:
            f = open(join(dir, file), 'r', encoding='iso-8859-15')
            D[file] = f.read()
            f.close()
    return D


# Document classification, and calculate accuracy according to index
def doc_classification(Index, D, V, prior, condprob):
    correct = 0
    for doc_name in D:
        c = apply_multinomial_NB(V, prior, condprob, D[doc_name])
        if c == Index[doc_name]:
            correct += 1
    return correct / len(D)


# Main function
def main():
    global st

    # read arguments "% ./nb_classifier [train_set_dir] [test_set_dir]"
    if len(sys.argv) != 3:
        send_stdout("Usage: python3 {} [train_set_dir] [test_set_dir]".format(sys.argv[0]));
        return

    # check index files is in the 'train_set_dir' and 'test_set_dir'
    train_index_path = join(sys.argv[1], INDEX_FILENAME)
    if not isfile(train_index_path):
        send_stdout('Error! Does not find "{}" file in the [train_set_dir].'.format(INDEX_FILENAME))
        return
    test_index_path = join(sys.argv[2], INDEX_FILENAME)
    if not isfile(test_index_path):
        send_stdout('Error! Does not find "{}" file in the [test_set_dir].'.format(INDEX_FILENAME))
        return

    # get emails from the [train_set_dir]
    try:
        train_files = [f for f in listdir(sys.argv[1]) \
            if isfile(join(sys.argv[1], f)) and f != INDEX_FILENAME]
    except FileNotFoundError as e:
        send_stdout('Error! No such file or directory "{}".'.format(sys.argv[1]))
        return
    # get emails from the [test_set_dir]
    try:
        test_files = [f for f in listdir(sys.argv[2]) \
            if isfile(join(sys.argv[2], f)) and f != INDEX_FILENAME]
    except FileNotFoundError as e:
        send_stdout('Error! No such file or directory "{}".'.format(sys.argv[2]))
        return

    # read train/test index file
    send_stdout('Reading training/test set index file ...')
    train_index = read_index_file(train_index_path)
    test_index = read_index_file(test_index_path)

    # read train/test emails
    send_stdout('Reading training/test set files(emails) ...')
    train_D = read_emails(sys.argv[1], train_files, train_index)
    test_D = read_emails(sys.argv[2], test_files, test_index)

    # Train multinomial in Naive Bayes
    send_stdout('Training Naive Bayes classifier ...')
    V, prior, condprob = train_multinomial_NB(train_index, train_D)

    send_stdout('Run spam detection using Naive Bayes classifier:')
    # run email HAM / SPAM classification, and calculate accuracy
    accuracy = doc_classification(train_index, train_D, V, prior, condprob)
    send_stdout('Training Accuracy: {}.'.format(accuracy))

    accuracy = doc_classification(test_index, test_D, V, prior, condprob)
    send_stdout('Test Accuracy: {}.'.format(accuracy))


if __name__ == '__main__':
    main()
