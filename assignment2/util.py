import sys
from pyparsing import *

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


# language model file name
LM_NAME = "LMS.txt"
L_TOKEN = "L_TOKEN"

# Use stemmer
STEMMER = True
# Choose stemmer between the 'Wordnet (Lemmatizer)' and the 'Porter'
USE_LEMMATIZER = True


# Word preprocessing stemming engine
class Token_Preprocessing_Engine(object):
    def __init__(self):
        if USE_LEMMATIZER:
            # WordnetStemmer (Lemmatizer)
            nltk.download('wordnet')
            self.engine = WordNetLemmatizer()
        else:
            # PorterStemmer
            self.engine = PorterStemmer()

    def process_token(self, token):
        if USE_LEMMATIZER:
            term = self.engine.lemmatize(token)
        else:
            term = self.engine.stem(token)
        return term.lower()


# Send msg to stdout
def send_stdout(msg=''):
    sys.stdout.write('{}\n'.format(msg))
    sys.stdout.flush()


# Progress Bar Code Reference:
# https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('\r[%s] %s%s ...%s' % (bar, percents, '%', status))
    sys.stdout.flush()
