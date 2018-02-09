import sys, argparse
from os import listdir
from os.path import join, isfile

from nltk.tokenize import wordpunct_tokenize

from util import send_stdout, progress
from util import ZONE_INDEX_FILE, STEMMER, Token_Preprocessing_Engine


# inverted positional zone index
zone_index = {}


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create index for weighted zone scoring')
    parser.add_argument('doc_dir', metavar='doc_dir', type=str,
        help='directory of the documents localed')
    parser.add_argument('index_dir', metavar='index_dir', type=str,
        help='directory to save the generated index file')
    return parser.parse_args()


def read_doc(path, docID, title):
    # Indexing 'title' zone
    # replace underline with space in doc title
    title = title.replace('_', ' ')
    title_tokens = wordpunct_tokenize(title)
    # create local position index for 'title' zone
    title_index = {}
    for pos in range(len(title_tokens)):
        # Stemming and Lowercasing
        if STEMMER:
            term = st.process_token(title_tokens[pos])
        else:
            term = title_tokens[pos].lower()
        if term not in title_index:
            title_index[term] = []
        title_index[term].append(pos)

    # Indexing 'body(content)' zone
    f = open(path, 'r')
    body_tokens = wordpunct_tokenize(f.read())
    f.close()
    # create local position index for 'body' zone
    body_index = {}
    for pos in range(len(body_tokens)):
        # Stemming and Lowercasing
        if STEMMER:
            term = st.process_token(body_tokens[pos])
        else:
            term = body_tokens[pos].lower()
        if term not in body_index:
            body_index[term] = []
        body_index[term].append(pos)

    # after indexed all terms, save them to positional index dictionary
    # i = 0 -> title zone
    # i = 1 -> body zone
    for i in range(2):
        loc_index = [title_index, body_index][i]
        for term, posting in loc_index.items():
            if term not in zone_index:
                zone_index[term] = [{}, {}]
            zone_index[term][i][docID] = posting


def read_dir(doc_dir, doc_files):
    skipped_files = []
    f_num = len(doc_files);
    for i in range(f_num):
        fname = doc_files[i]
        finfo = fname.split(sep='_', maxsplit=2)
        # filename validation
        if finfo[0] != 'doc':
            skipped_files.append(fname); continue
        try:
            # read file, and create indexes
            read_doc(join(doc_dir, fname), int(finfo[1]), finfo[2])
        except Exception as e:
            print(e)
            skipped_files.append(fname); continue
        # update progress bar
        progress(i+1, f_num)
    # show skipped invalid docs
    send_stdout()
    if len(skipped_files) != 0:
        send_stdout('Warning! Cannot index the following file(s):')
        send_stdout('{}, Skipped.'.format(skipped_files))


def main():
    global st
    # read arguments
    args = parse_arguments()

    # get filenames from the [document dir]
    try:
        doc_files = [f for f in listdir(args.doc_dir) if isfile(join(args.doc_dir, f))]
    except FileNotFoundError as e:
        send_stdout('Error! No such file or directory "{}".'.format(args.doc_dir))
        return
    # check whether the index file for zone scoring already exist
    if isfile(join(args.index_dir, ZONE_INDEX_FILE)):
        send_stdout('Error! Index file "{}" already exist.'.\
            format(join(args.index_dir, ZONE_INDEX_FILE)))
        return

    # initialize stemmer (Lemmatizer)
    if STEMMER:
        st = Token_Preprocessing_Engine()

    # read directory -> read doc -> create zone indexes
    read_dir(args.doc_dir, doc_files)

    # write index to file
    f_out = open(join(args.index_dir, ZONE_INDEX_FILE), 'w')
    for term in sorted(zone_index.keys()):
        f_out.write('{term} {posting}\n'.format(term=term, posting=zone_index[term]))
    f_out.close()


if __name__ == '__main__':
    main()
