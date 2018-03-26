import sys, io, os, ast
from os.path import join, isfile
from contextlib import redirect_stdout

import unittest
from unittest.mock import patch

# set up relative path for programs to be tested
program_path = sys.path[0] + "/../"
sys.path.append(program_path)

import nb_classifier as nb_c


class Test_NB_Classifier(unittest.TestCase):

    def test_no_index_file(self):
        warning = [
            'Error',
            'not find',
            'index', ]
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python3', './test1/train', './test1/test']), redirect_stdout(cout):
            nb_c.main()
        s = cout.getvalue()
        # test whether 'nb_classifier' has correctly return 'index not find' msg.
        for msg in warning:
            self.assertTrue(msg in s)

    def test_a_few_emails_corpus_with_same_train_test_set(self):
        Accuracy = [
            'Training Accuracy: 1',
            'Test Accuracy: 1', ]
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python3', './test2/train', './test2/test']), redirect_stdout(cout):
            nb_c.main()
        s = cout.getvalue()
        # test whether 'nb_classifier' has correctly return 'index not find' msg.
        for ac in Accuracy:
            self.assertTrue(ac in s)

    def test_no_docs_in_corpus(self):
        warning = [
            'not find any documents',
            'none',
            'index file', ]
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python3', './test3/train', './test3/test']), redirect_stdout(cout):
            nb_c.main()
        s = cout.getvalue()
        # test whether 'nb_classifier' has correctly return 'index not find' msg.
        for msg in warning:
            self.assertTrue(msg in s)

    def test_index_file_does_not_match_with_corpus(self):
        warning = [
            'not find any documents',
            'train_set_dir',
            'not',
            'match', ]
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python3', './test4/train', './test4/test']), redirect_stdout(cout):
            nb_c.main()
        s = cout.getvalue()
        # test whether 'nb_classifier' has correctly return 'index not find' msg.
        for msg in warning:
            self.assertTrue(msg in s)

if __name__ == '__main__':
    unittest.main()
