import sys
from os import listdir
from os.path import join, isfile

'''
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
'''
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.porter import PorterStemmer

from progress import progress


# inverted positional index
positional_index = {}
'''
# Lemmatizer
wnl = WordNetLemmatizer()
'''
# PorterStemmer
st = PorterStemmer()

def read_file(path, docID):
    loc_index = {}
    # extract text from the path, and tokenize
    f = open(path, 'r')
    tokens = wordpunct_tokenize(f.read())
    f.close()
    # save local positional index to temporary dictionary "loc_index"
    for pos in range(len(tokens)):
        '''
        # Lemmatization and Lowercasing
        term = wnl.lemmatize(tokens[pos]).lower()
        '''
        # Stemming and Lowercasing
        term = st.stem(tokens[pos]).lower()
        if term not in loc_index:
            loc_index[term] = []
        loc_index[term].append(pos)
    # after indexed all terms, save them to positional index dictionary
    for term, indexes in loc_index.items():
        if term not in positional_index:
            positional_index[term] = {}
        positional_index[term][docID] = indexes


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

    print()

    # write index to file
    for term in sorted(positional_index.keys()):
        print(term)
    print(len(positional_index.keys()))
