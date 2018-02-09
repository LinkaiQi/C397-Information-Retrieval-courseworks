import sys, ast, argparse
import math
from os.path import join

from util import INDEX_FILE
from util import send_stdout, progress, Token_Preprocessing_Engine


# inverted positional index
positional_index = {}
document_ids = set()

# parse argument format:
#   [index location] [k] [scores] [term_1] [term_2] ... [term_n]
def parse_arguments():
    parser = argparse.ArgumentParser\
        (description='Ranks documents according to the Vector Space model')
    parser.add_argument('path', metavar='index_location', type=str,
        help='directory of the index file')
    parser.add_argument('k', metavar='k', type=int,
        help='the number of documents to retrieve')
    parser.add_argument('score', metavar='score', type=str,
        help='should be either y or n, indicating whether or not to print the '
        'scores together with each document identifier')
    parser.add_argument('terms', metavar='term', type=str, nargs='+',
        help='query search terms')
    return parser.parse_args()

def read_index(f):
    global document_ids
    send_stdout('reading index ...')
    entries = f.readlines()
    for entry in entries:
        term, index = entry.split(maxsplit=1)
        index = ast.literal_eval(index)
        positional_index[term] = index
        document_ids = document_ids | set(index.keys())

# get the length of each document
def get_length():
    # Initialize length for all documents to zero
    length = {}
    for d in document_ids:
        length[d] = 0
    # Accumulate length
    for term in positional_index:
        posting = positional_index[term]
        for d in posting:
            length[d] = length[d] + len(posting[d])
    return length

'''
INPUT: a term(t) in the query
OUTPUT: inverse document frequency (idf) of the term t '''
def get_term_weight(t):
    # tf-idf scheme for term weight
    # idf(t) = log (N / df(t)).
    N = len(document_ids)
    df = len(positional_index[t])
    return math.log10(N/df)

# Computing vector scores
def cosine_score(q):
    # Initialize score for all documents to zero
    score = {}
    for d in document_ids:
        score[d] = 0
    # Initialize Length[N]
    # length = get_length()
    for term in q:
        # calculate w(term,q) and fetch postings list for 'term'
        if term not in positional_index:
            continue
        w = get_term_weight(term)
        postings_list = positional_index[term]
        for doc_id in postings_list:
            tf = len(postings_list[doc_id])
            score[doc_id] += w * tf
    # for d in document_ids:
    #     score[d] = score[d] / length[d]
    return score

def main():
    # read arguments
    args = parse_arguments()
    if args.score not in ['y', 'n']:
        send_stdout('Error! arg "scores" should be either y or n')
        sys.exit()

    # open index file
    try:
        path = join(args.path, INDEX_FILE)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Index file "{}" does not exits.'.format(path))
        sys.exit()

    # initialize query stemmer (Lemmatizer)
    if STEMMER:
        st = Token_Preprocessing_Engine()
        query = [st.process_token(t) for t in args.terms]
    else:
        query = [t.lower() for t in args.terms]

    # read index
    try:
        read_index(f)
    except:
        send_stdout('Error! Invalided index file format.')
        sys.exit()

    # compute vector space scores
    score = cosine_score(query)
    k_score = sorted(score.items(), key=lambda x:x[1], reverse=True)
    for i in range(min(args.k, len(k_score))):
        d, s = k_score[i]
        if args.score == 'y':
            send_stdout('{id} \t {score}'.format(id=d, score=s))
        else:
            send_stdout('{id}'.format(id=d))

    f.close()


if __name__ == '__main__':
    main()
