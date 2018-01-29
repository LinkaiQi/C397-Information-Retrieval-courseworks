import sys
import argparse
from os.path import join

from util import INDEX_FILE, send_stdout, searchExpr

def parse_arguments():
    parser = argparse.ArgumentParser(description='Performs boolean queries on a given index')
    parser.add_argument('path', metavar='directory', type=str,
        help='directory of the index file')
    parser.add_argument('query', metavar='query', type=str,
        help='boolean query')
    return parser.parse_args()

if __name__ == '__main__':
    # read arguments
    args = parse_arguments()
    print(args.path)
    print(args.query)

    # open index file
    try:
        path = join(args.path, INDEX_FILE)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Index file does not find "{}".'.format(path))
        sys.exit()

    # parse query
    lisp_bool_query = searchExpr.parseString(args.query)[0]
    print(lisp_bool_query)



    f.close()
