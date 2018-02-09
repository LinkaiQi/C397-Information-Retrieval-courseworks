import sys
from os import listdir
from os.path import join, isfile

from nltk.tokenize import wordpunct_tokenize

from util import send_stdout, progress
from util import ZONE_INDEX_FILE, STEMMER, Token_Preprocessing_Engine



def parse_arguments():
    parser = argparse.ArgumentParser(description='Create index for weighted zone scoring')
    parser.add_argument('doc_dir', metavar='document dir', type=str,
        help='directory of the documents localed')
    parser.add_argument('index_dir', metavar='index dir', type=str,
        help='directory to save the generated index file')
    return parser.parse_args()

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
            skipped_files.append(fname); continue
        # update progress bar
        progress(i+1, f_num)


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

    read_dir(args.doc_dir, doc_files)


if __name__ == '__main__':
    main()
