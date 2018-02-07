import sys, ast
from os.path import join

from util import INDEX_FILE, send_stdout

def rw_index(f):
    entries = f.readlines()
    for entry in entries:
        term, index = entry.split(maxsplit=1)
        index_out = []
        index = ast.literal_eval(index)
        for docID in sorted(index.keys()):
            pos = [str(p) for p in index[docID]]
            index_out.append('{0}:{1}'.format(docID, ','.join(pos)))
        send_stdout('{0} \t {1} '.format(term, ';'.join(index_out)))

def main():
    # read arguments
    if len(sys.argv) != 2:
        send_stdout("format: python {} [directory]".format(sys.argv[0]));
        return
    # open index file
    try:
        path = join(sys.argv[1], INDEX_FILE)
        f = open(path)
    except FileNotFoundError as e:
        send_stdout('Error! Index file does not find "{}".'.format(path))
        return

    # read index file
    try:
        rw_index(f)
    except:
        send_stdout('Error! Invalided index file format "{}".'.format(path))

    f.close()

if __name__ == '__main__':
    main()
