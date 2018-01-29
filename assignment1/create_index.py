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

from util import INDEX_FILE, send_stdout, progress


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
        send_stdout("format: python {} [dir]".format(sys.argv[0]));
        sys.exit()
    # get filenames from the [dir]
    try:
        path = sys.argv[1]
        files = [f for f in listdir(path) if isfile(join(path, f))]
    except FileNotFoundError as e:
        send_stdout('Error! No such file or directory "{}".'.format(path))
        sys.exit()
    # check whether the index file already exist
    if isfile(INDEX_FILE):
        send_stdout('Error! Index file "{}" already exist.'.format(INDEX_FILE))
        sys.exit()

    skipped_files = []
    f_num = len(files);
    for i in range(f_num):
        fname = files[i]
        finfo = fname.split(sep='_', maxsplit=2)
        # filename validation
        if finfo[0] != 'doc':
            skipped_files.append(fname); continue
        try:
            # read file, and create indexes
            read_file(join(path, fname), int(finfo[1]))
        except:
            skipped_files.append(fname); continue
        # update progress bar
        progress(i+1, f_num)

    send_stdout()
    if len(skipped_files) != 0:
        send_stdout('Warning! Cannot index the following file(s):')
        send_stdout('{} Skipped'.format(skipped_files))

    # write index to file
    f_out = open(INDEX_FILE, 'w')
    for term in sorted(positional_index.keys()):
        f_out.write('{term} {index}\n'.format(term=term, index=positional_index[term]))
    f_out.close()
