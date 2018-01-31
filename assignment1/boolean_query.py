import sys, ast, argparse
from os.path import join

from util import send_stdout, searchExpr, Token_Preprocessing_Engine
from util import INDEX_FILE, AND, OR, NOT, L_BKT, R_BKT, QUOTE


# inverted positional index
positional_index = {}
documents = set()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Performs boolean queries on a given index')
    parser.add_argument('path', metavar='directory', type=str,
        help='directory of the index file')
    parser.add_argument('query', metavar='query', type=str,
        help='boolean query')
    return parser.parse_args()

def validate_query(query):
    org_opt = par_opt = 0
    # check original query
    for t in query.split():
        if t.strip(L_BKT+R_BKT) in [AND, OR, NOT]: org_opt += 1
    # check parsed query
    try: lisp_bool_query = searchExpr.parseString(args.query)[0]
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
# get_operands('(AND (NOT harry_potter) azkaban)')
# get_operands('(AND (NOT dictionary) (NOT love)) (AND harrypotter azkaban)')
def get_operands(opds):
    operands = []
    if opds[0] == L_BKT:
        n_lbkt = 0
        for i in range(len(opds)):
            if opds[i] == L_BKT:
                if n_lbkt == 0: start_i = i
                n_lbkt += 1
            elif opds[i] == R_BKT:
                n_lbkt -= 1
                if n_lbkt == 0: operands.append(opds[start_i:i+1])
        # check unbalanced bracket
        assert(n_lbkt == 0)
    else:
        operands = opds.split()
    return operands

def query_valuation(query, id):
    print("--->", query)
    # base case (a single term or phrase)
    if query[0] != L_BKT:
        print("  B")
        phrase = query.split('_')
        phrase = [st.process_token(token) for token in phrase]
        # a single term
        if len(phrase) == 1:
            return search_term(phrase[0], id)
        # a phrase
        else :
            return search_pharse(phrase, id)

    # if not basecase, divide the query into sub-queries
    query = query[1:-1]
    opt, opds = query.split(maxsplit=1)
    sub_q = get_operands(opds);
    print("  N", sub_q)
    if opt == AND:
        return query_valuation(sub_q[0], id) and query_valuation(sub_q[1], id)
    elif opt == OR:
        return query_valuation(sub_q[0], id) or query_valuation(sub_q[1], id)
    elif opt == NOT:
        return not query_valuation(sub_q[0], id)
    else:
        # invalid boolean operator found, raise exception
        raise Exception

'''
INPUT: stemmed pharse, document id
OUTPUT: a boolean value,
    indicate whether the pharse is contained in the document '''
def search_pharse(pharse, doc_id):
    f_term = pharse[0]
    try: occurence = positional_index[f_term][doc_id]
    except KeyError as e: return False
    for term in pharse[1:]:
        new_occurence = []
        for p in occurence:
            try:
                if p+1 in positional_index[term][doc_id]:
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
def search_term(term, doc_id):
    try:
        positional_index[term][doc_id]
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
        documents = documents | set(index.keys())

# Example 'search_pharse' test case:
# _search_pharse_func_tester("established vampire leadership", 240)
def _search_pharse_func_tester(pharse, doc_id):
    terms = []
    t_st = Token_Preprocessing_Engine()
    for token in pharse.split():
        terms.append(t_st.process_token(token))
    result = search_pharse(terms, doc_id)
    send_stdout(result)

if __name__ == '__main__':
    # read arguments
    args = parse_arguments()
    # print(args.path)
    # print(args.query)

    # query validation
    if not validate_query(args.query):
        send_stdout('Error! Invalided boolean query.')
        sys.exit()

    # open index file
    try:
        path = join(args.path, INDEX_FILE)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Index file "{}" does not exits.'.format(path))
        sys.exit()
    # read index
    read_index(f)

    # initialize query stemmer (Lemmatizer)
    st = Token_Preprocessing_Engine()

    # query preprocessing
    p_query = preprocessing_query(args.query)
    # parse query
    lisp_bool_query = str(searchExpr.parseString(p_query)[0])
    send_stdout("Pharsed Boolean Query: {}.".format(lisp_bool_query))

    # find document that satisfied the boolean query
    for doc_id in documents:
        result = []
        if query_valuation(lisp_bool_query, doc_id):
            result.append(doc_id)
    send_stdout("Documents: {}.".format(', '.join(str(lisp_bool_query))))

    f.close()
