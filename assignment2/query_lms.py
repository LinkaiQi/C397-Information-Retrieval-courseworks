#!/usr/bin/env python3

import sys, ast, argparse, math
from os.path import join

from util import STEMMER, LM_NAME, L_TOKEN
from util import send_stdout, Token_Preprocessing_Engine

# Global variable for store the LM
# KEY = docID, VALUE = terms_MLE
LM_LMS = {}

# Pˆ(t|d) = λ * Pˆmle(t|Md) + (1 − λ) * Pˆmle(t|Mc)
# Lambda used in smoothing of the query generation probability(score)
Lambda = 0.5    # 0 < λ < 1


def parse_arguments():
    parser = argparse.ArgumentParser(description='Calculate the likelihood of a '\
    'query by using language models and output the top k document, sorted by likelihood')
    parser.add_argument('LM_DIR', metavar='language_models_location', type=str,
        help='directory of the index file')
    parser.add_argument('k', metavar='k', type=int, help='output top k document')
    parser.add_argument('query', metavar='multi-term_query', type=str,
        help='boolean query')
    return parser.parse_args()


def estimate_query_lh(terms):
    global LM_LMS, Lambda
    # Q_likelihood store the query generation probability(likelihood) from each document d.
    Q_likelihood = {}

    # Pre-compute Pˆmle(t|Mc) for all the terms in the query
    Lc = 0
    # initialize tf in the collection for all terms in the query to zero
    TFc = {}
    for t in terms:
        TFc[t] = 0
    # accumulate 'Lc' and 'TFc'
    for docID in LM_LMS:
        Lc += LM_LMS[docID][L_TOKEN]
        for t in terms:
            if t in LM_LMS[docID]:
                TFc[t] += LM_LMS[docID][t]
    # calculate MLE of the terms from the collection
    MLEc = {}
    for t in TFc:
        MLEc[t] = TFc[t] / Lc

    # Estimate query generation probability(likelihood) from each document d. (Pˆ(q|Md))
    for docID in LM_LMS:
        # to avoid numerical underflow, estimate 'P: (Pˆ(q|Md)' in log space.
        P = 0
        L = LM_LMS[docID][L_TOKEN]
        for t in terms:
            # calculate Pˆmle(t|Md)
            if t not in LM_LMS[docID]:
                P_tMd = 0
            else:
                P_tMd = LM_LMS[docID][t] / L
            # get Pˆmle(t|Mc)
            P_tMc = MLEc[t]
            # calculate Pˆ(t|d) = λ * Pˆmle(t|Md) + (1 − λ) * Pˆmle(t|Mc)
            P_td = Lambda * P_tMd + (1-Lambda) * P_tMc
            # Mulitply Pˆ(t|d) in log space
            assert P_td != 0
            P += math.log(P_td)
        print(P)
        Q_likelihood[docID] = math.e ** P

    return Q_likelihood


def process_query(query):
    # initialize stemmer (Lemmatizer)
    if STEMMER:
        st = Token_Preprocessing_Engine()
    # process query
    terms = []
    for token in query.split():
        # Stemming and Lowercasing
        if STEMMER:
            t = st.process_token(token)
        else:
            t = token.lower()
        terms.append(t)
    return terms


def main():
    global LM_LMS
    # read arguments
    args = parse_arguments()

    # open language models file
    try:
        path = join(args.LM_DIR, LM_NAME)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Language models file does not find "{}".'.format(path))
        return

    # read language models file
    send_stdout('Reading language models file ...')
    try:
        LM_txt = f.readline()
        LM_LMS = ast.literal_eval(LM_txt)
    except Exception as e:
        send_stdout('Error! Language models file format "{}".'.format(path))
        f.close(); return

    # Tokenize query and run stemmer / Lemmatizer
    query_terms = process_query(args.query)
    print(query_terms)

    # Estimate query likelihood per document
    likelihood = estimate_query_lh(query_terms)

    # Output the top K documents by likelihood
    sorted_docIDs = sorted(likelihood, key=likelihood.get, reverse=True)
    k = min(len(sorted_docIDs), args.k)
    for idx in range(k):
        docID = sorted_docIDs[idx]
        lh = likelihood[docID]
        # FORMAT: doc_id_1 \t query_likelihood \n
        send_stdout('{} \t {}'.format(docID, lh))

    f.close()

if __name__ == '__main__':
    main()
