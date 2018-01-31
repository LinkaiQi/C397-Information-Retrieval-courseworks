import sys
from pyparsing import *

import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


# Index file name
INDEX_FILE = "index.txt"

# Choose stemmer between the 'Wordnet (Lemmatizer)' and the 'Porter'
USE_LEMMATIZER = True

# Boolean query operator
AND = 'AND'; OR = "OR"; NOT = "NOT"
L_BKT = '('; R_BKT = ')'; QUOTE = '"'


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


# Boolean query parser (Parsing simple string and generating lisp)
# Code reference:
# http://kitchingroup.cheme.cmu.edu/blog/2014/03/31/Using-pyparsing-for-search-queries-with-tags/
class UnaryOperation(object):
    'takes one operand,e.g. not'
    def __init__(self, tokens):
        self.op, self.operands = tokens[0]

class BinaryOperation(object):
    'takes two or more operands, e.g. and, or'
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][0::2]

class SearchAnd(BinaryOperation):
    def __repr__(self):
        return '(AND {0})'.format(' '.join(str(oper) for oper in self.operands))

class SearchOr(BinaryOperation):
    def __repr__(self):
        return '(OR {0})'.format(' '.join(str(oper) for oper in self.operands))

class SearchNot(UnaryOperation):
    def __repr__(self):
        return '(NOT {0})'.format(self.operands)

class SearchTerm(object):
    'represents a termthat is being searched. here just a word'
    def __init__(self, tokens):
        self.term = tokens[0]
    def __repr__(self):
        return self.term

# the grammar
and_ = CaselessLiteral("AND")
or_ = CaselessLiteral("OR")
not_ = CaselessLiteral("NOT")

searchTerm = Word(alphanums) | quotedString.setParseAction(removeQuotes)
searchTerm.setParseAction(SearchTerm)

searchExpr = operatorPrecedence(searchTerm,
    [(not_, 1, opAssoc.RIGHT, SearchNot),
     (and_, 2, opAssoc.LEFT, SearchAnd),
     (or_, 2, opAssoc.LEFT, SearchOr)])

# print(searchExpr.parseString('NOT kpt')[0])
# print(searchExpr.parseString('NOT (kpt AND eos)')[0])
# print(searchExpr.parseString('wood AND blue OR red')[0])
# print(searchExpr.parseString('wood AND blue AND heavy OR red')[0])
# print(searchExpr.parseString('(dictionary AND love) OR ("harry potter" AND azkaban)')[0])
