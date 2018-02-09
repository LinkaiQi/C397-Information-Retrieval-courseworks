import sys, ast, argparse
from os.path import join

from util import send_stdout, searchExpr, Token_Preprocessing_Engine
from util import ZONE_INDEX_FILE, STEMMER, AND, OR, NOT, L_BKT, R_BKT, QUOTE


# inverted positional index
positional_index = {}
documents = set()

# zone
TITLE = 0
BODY = 1


# ./zone_scorer [index dir] [k] [g] [q]
def parse_arguments():
    parser = argparse.ArgumentParser(description='Weighted zone scoring')
    parser.add_argument('index_dir', metavar='index_dir', type=str,
        help='directory of the zone index file')
    parser.add_argument('k', metavar='k', type=int,
        help='top k document')
    parser.add_argument('g', metavar='g', type=float,
        help='title weight')
    parser.add_argument('q', metavar='q', type=str,
        help='boolean query')
    return parser.parse_args()

def validate_query(query):
    org_opt = par_opt = 0
    # check original query
    for t in query.split():
        if t.strip(L_BKT+R_BKT) in [AND, OR, NOT]: org_opt += 1
    # check parsed query
    try: lisp_bool_query = searchExpr.parseString(query)[0]
    except: return False
    for t in str(lisp_bool_query).split():
        if t.strip(L_BKT+R_BKT) in [AND, OR, NOT]: par_opt += 1
    return org_opt == par_opt

'''
INPUT: boolean_query
OUTPUT: pre-processed boolean_query (and groups potential pharses) '''
def preprocessing_query(query):
    # groups pharse
    is_pharse = False
    for i in range(len(query)):
        if query[i] == QUOTE: is_pharse = not is_pharse
        if query[i] == ' ' and is_pharse: query = query[:i] + '_' + query[i+1:]
    return query


# TEST CASE:
# get_operands('dictionary love')
# get_operands('(NOT harry_potter) azkaban')
# get_operands('(AND (NOT dictionary) (NOT love)) (AND harrypotter azkaban)')
def get_operands(opds):
    operands = []
    n_lbkt = 0; in_opd = False
    opds = opds.strip()
    for i in range(len(opds)):
        if opds[i] == L_BKT:
            if n_lbkt == 0: start_i = i
            n_lbkt += 1
        elif opds[i] == R_BKT:
            n_lbkt -= 1
            if n_lbkt == 0: operands.append(opds[start_i:i+1])
        elif not in_opd and n_lbkt == 0 and opds[i] != ' ':
            start_i = i
            in_opd = True
        elif in_opd and n_lbkt == 0 and opds[i] == ' ':
            operands.append(opds[start_i:i])
            in_opd = False
    if in_opd:
        operands.append(opds[start_i:])
    # check unbalanced bracket
    assert(n_lbkt == 0)
    return operands

def query_valuation(query, id, zone):
    global st
    # base case (a single term or phrase)
    if query[0] != L_BKT:
        phrase = query.split('_')
        if STEMMER:
            phrase = [st.process_token(token) for token in phrase]
        else:
            phrase = [token.lower() for token in phrase]
        # a single term
        if len(phrase) == 1:
            return search_term(phrase[0], id, zone)
        # a phrase
        else :
            return search_pharse(phrase, id, zone)

    # if not basecase, divide the query into sub-queries
    query = query[1:-1]
    opt, opds = query.split(maxsplit=1)
    sub_q = get_operands(opds);
    if opt == AND:
        return query_valuation(sub_q[0], id, zone) and query_valuation(sub_q[1], id, zone)
    elif opt == OR:
        return query_valuation(sub_q[0], id, zone) or query_valuation(sub_q[1], id, zone)
    elif opt == NOT:
        return not query_valuation(sub_q[0], id, zone)
    else:
        # invalid boolean operator found, raise exception
        raise Exception

'''
INPUT: stemmed pharse, document id
OUTPUT: a boolean value,
    indicate whether the pharse is contained in the document '''
def search_pharse(pharse, doc_id, zone):
    f_term = pharse[0]
    try: occurence = positional_index[f_term][doc_id]
    except KeyError as e: return False
    for term in pharse[1:]:
        new_occurence = []
        for p in occurence:
            try:
                if zone == TITLE and p+1 in positional_index[term][0][doc_id]:
                    new_occurence.append(p+1)
                elif zone == BODY and p+1 in positional_index[term][1][doc_id]:
                    new_occurence.append(p+1)
            except KeyError as e:
                # if the next term (p+1) is not in the positional_index,
                # search the term will return a dictionary 'keyError' exception.
                # Do nothing to remove 'p' from occurence list
                pass
        occurence = new_occurence

    if len(occurence) != 0:
        return True
    else:
        return False

'''
INPUT: stemmed term, document id
OUTPUT: a boolean value,
    indicate whether the term is contained in the document '''
def search_term(term, doc_id, zone):
    try:
        if zone == TITLE:
            positional_index[term][0][doc_id]
        else:
            positional_index[term][1][doc_id]
    except KeyError as e:
        # if the 'term' is not in the positional_index of the given 'doc_id',
        # search the term will return a dictionary 'keyError' exception.
        return False
    return True

def read_index(f):
    global documents
    entries = f.readlines()
    for entry in entries:
        term, index = entry.split(maxsplit=1)
        index = ast.literal_eval(index)
        positional_index[term] = index
        documents = documents | set(index[1].keys())


# Main function
def main():
    global st, documents

    # read arguments
    args = parse_arguments()

    # query validation
    if not validate_query(args.q):
        send_stdout('Error! Invalided boolean query.')
        sys.exit()

    # open index file
    try:
        path = join(args.index_dir, ZONE_INDEX_FILE)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Zone index file "{}" does not exits.'.format(path))
        sys.exit()

    # read index
    send_stdout("Reading zone index ...")
    try:
        read_index(f)
    except Exception as e:
        print(e)
        send_stdout('Error! Invalided zone index file format.')
        sys.exit()

    # initialize query stemmer (Lemmatizer)
    if STEMMER:
        st = Token_Preprocessing_Engine()

    # query preprocessing
    p_query = preprocessing_query(args.q)
    # parse query
    lisp_bool_query = str(searchExpr.parseString(p_query)[0])
    send_stdout("Pharsed Boolean Query: {}.".format(lisp_bool_query))

    # find document that satisfied the boolean query
    send_stdout("Searching and scoring ...")
    result = {}
    for doc_id in documents:
        score = 0;
        if query_valuation(lisp_bool_query, doc_id, TITLE):
            score += 1 * args.g
        if query_valuation(lisp_bool_query, doc_id, BODY):
            score += 1 * (1-args.g)
        result[doc_id] = score
    k_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    for i in range(min(args.k, len(k_result))):
        d, s = k_result[i]
        send_stdout('{id} \t {score}'.format(id=d, score=s))

    f.close()


if __name__ == '__main__':
    main()
