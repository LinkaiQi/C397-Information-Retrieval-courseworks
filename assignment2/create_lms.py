#!/usr/bin/env python3

import sys
from os import listdir
from os.path import join, isfile

from nltk.tokenize import wordpunct_tokenize

from util import send_stdout, progress
from util import LM_NAME, L_TOKEN, STEMMER, Token_Preprocessing_Engine

# Global variable for store the LM
# KEY = docID, VALUE = terms_MLE
LM_LMS = {}

def read_file(path, docID):
    # extract text from the path, and tokenize
    f = open(path, 'r')
    tokens = wordpunct_tokenize(f.read())
    f.close()

    # store term frequence for each term occurs in the document d
    TF = {}
    # the number of tokens in document d
    L = len(tokens)

    # Iterate through each term in document d,
    # use 'TF' accumulator to count the term frequency
    for token in tokens:
        # Stemming and Lowercasing
        if STEMMER:
            term = st.process_token(token)
        else:
            term = token.lower()
        if term not in TF:
            TF[term] = 0
        TF[term] += 1

    TF[L_TOKEN] = L
    # Store TF to Global variable LM with its docID
    LM_LMS[docID] = TF

# filename validation
# filename format "doc_[docID]_[...]"
def filename_validation(fname):
    finfo = fname.split(sep='_', maxsplit=2)
    if finfo[0] != 'doc':
        return False, None
    try:
        docID = int(finfo[1])
    except ValueError:
        return False, None
    return True, docID

# Main function
def main():
    global st

    # read arguments "% ./create_lms [document dir] [output_dir]"
    if len(sys.argv) != 3:
        send_stdout("Usage: python3 {} [document_dir] [output_dir]".format(sys.argv[0]));
        return
    # get filenames from the [document dir]
    try:
        DOC_DIR = sys.argv[1]
        docs = [f for f in listdir(DOC_DIR) if isfile(join(DOC_DIR, f))]
    except FileNotFoundError as e:
        send_stdout('Error! No such file or directory "{}".'.format(DOC_DIR))
        return
    # check whether the index file already exist in the [output_dir]
    LM_FILE = join(sys.argv[2], LM_NAME)
    if isfile(LM_FILE):
        send_stdout('Error! LM file "{}" already exist.'.format(LM_FILE))
        return

    # initialize stemmer (Lemmatizer)
    if STEMMER:
        st = Token_Preprocessing_Engine()

    skipped_docs = []
    invalid_filename_docs = []
    f_num = len(docs);
    for i in range(f_num):
        fname = docs[i]
        success, docID = filename_validation(fname)
        if not success:
            invalid_filename_docs.append(fname); continue
        try:
            # read file, and create language models (calculate MLE)
            read_file(join(DOC_DIR, fname), docID)
        except Exception as e:
            skipped_docs.append(fname); continue
        # update progress bar
        progress(i+1, f_num)

    send_stdout()
    # show invalid document name/format to stdout
    if len(invalid_filename_docs) != 0:
        send_stdout('Warning! Invalid document name format:')
        send_stdout('{}, Skipped.'.format(invalid_filename_docs))
    if len(skipped_docs) != 0:
        send_stdout('Warning! Cannot process the following doc(s):')
        send_stdout('{}, Skipped.'.format(skipped_docs))

    # write index to file
    f_out = open(LM_FILE, 'w')
    f_out.write(str(LM_LMS))
    f_out.close()


if __name__ == '__main__':
    main()
