#!/usr/bin/env python3

import sys, ast
from os.path import join

from util import LM_NAME, L_TOKEN, send_stdout

def print_lms(f):
    LM_txt = f.readline()
    LM_LMS = ast.literal_eval(LM_txt)
    for docID in sorted(LM_LMS.keys()):
        doc_TF = LM_LMS[docID]
        L = doc_TF[L_TOKEN]
        output = '{} \t '.format(docID)
        for term in doc_TF:
            # MLE(t|d) = tf(t,d) / L(d)
            output = output + term + ':' + str(doc_TF[term]/L) + ', '
        if output[-2:] == ', ':
            output = output[:-2]
        # FORMAT: 'doc_id \t term_1:term_1_MLE, term_2:term_2_MLE, ...'
        send_stdout(output)


def main():
    # read arguments
    # % ./print_lms [language_models_location]
    if len(sys.argv) != 2:
        send_stdout("Usage: python3 {} [language_models_location]".format(sys.argv[0]));
        return
    # open language models file
    try:
        path = join(sys.argv[1], LM_NAME)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Language models file does not find "{}".'.format(path))
        return

    # read language models file and print the MLE per term & document
    send_stdout('Reading language models file ...')
    try:
        print_lms(f)
    except Exception as e:
        send_stdout('Error! Language models file format "{}".'.format(path))

    f.close()

if __name__ == '__main__':
    main()
