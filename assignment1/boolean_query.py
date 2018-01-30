import sys
import argparse
from os.path import join

from util import send_stdout, searchExpr
from util import INDEX_FILE, AND, OR, NOT, L_BKT, R_BKT

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

# TEST CASE:
# get_operands('dictionary love')
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


def query_valuation(query):
    print(query)
    # base case (a single term or phrase)
    if query[0] != L_BKT:
        pass
    # if not basecase, divide the query into sub-queries
    query = query[1:-1]
    opt, opds = query.split(maxsplit=1)
    sub_q = get_operands(opds);
    if opt == AND:
        return query_valuation(sub_q[0]) and query_valuation(sub_q[1])
    elif opt == OR:
        return query_valuation(sub_q[0]) or query_valuation(sub_q[1])
    elif opt == NOT:
        return not query_valuation(sub_q[0])
    else:
        raise Exception




if __name__ == '__main__':
    # read arguments
    args = parse_arguments()
    # print(args.path)
    # print(args.query)

    # # open index file
    # try:
    #     path = join(args.path, INDEX_FILE)
    #     f = open(path)
    # except FileNotFoundError as e:
    #     send_stdout('Error! Index file "{}" does not exits.'.format(path))
    #     sys.exit()
    # f.close()

    # query validation
    if not validate_query(args.query):
        send_stdout('Error! Invalided boolean query.')
        sys.exit()

    # parse query
    lisp_bool_query = str(searchExpr.parseString(args.query)[0])
    query_valuation(lisp_bool_query)
