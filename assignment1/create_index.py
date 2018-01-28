import sys
from os import listdir
from os.path import join, isfile
from nltk.tokenize import wordpunct_tokenize

from progress import progress


# Inverted positional index
positional_index = {}

def read_file(path, docID):
    loc_index = {}
    # extract text from the path, and tokenize
    f = open(path, 'r')
    tokens = wordpunct_tokenize(f.read())
    f.close()
    # save local positional index to temporary dictionary "loc_index"
    for pos in range(len(tokens)):
        token = tokens[pos]
        if token not in loc_index:
            loc_index[token] = []
        loc_index[token].append(pos)
        # if tokens not in positional_index:
        #     positional_index[token] = {}
    # after indexed all tokens, save them to positional index dictionary
    for token, indexes in loc_index.items():
        if token not in positional_index:
            positional_index[token] = {}
        positional_index[token][docID] = indexes


if __name__ == '__main__':
    # read arguments
    if len(sys.argv) != 2:
        print("format: python3 {} [dir]".format(sys.argv[0]));
        sys.exit()
    # get filenames from the [dir]
    path = sys.argv[1]
    files = [f for f in listdir(path) if isfile(join(path, f))]

    f_num = len(files);
    # while i < f_num:
    for i in range(f_num):
        fname = files[i]
        finfo = fname.split(sep='_', maxsplit=2)
        # filename validation
        if finfo[0] != 'doc':
            print('Warning, incorrect format "{}"'.format(fname))
            continue
        try: file_id = int(finfo[1])
        except:
            print('Warning, incorrect format "{}"'.format(fname))
            continue
        # read file, and create indexes
        read_file(join(path, fname), file_id)
        # update progress bar
        progress(i, f_num)
        i += 1

    print("Done!")
