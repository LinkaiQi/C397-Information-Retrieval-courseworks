import sys, io, os, ast
from os.path import join, isfile
from contextlib import redirect_stdout

import unittest
from unittest.mock import patch

# set up relative path for programs to be tested
program_path = sys.path[0] + "/../"
sys.path.append(program_path)

import create_index as ci
from util import INDEX_FILE


class TestCreateIndex(unittest.TestCase):

    def setUp(self):
        # remove index file if it exists
        f = join('.', INDEX_FILE)
        if isfile(f):
            os.remove(f)

    def test_invalid_filename_format(self):
        invalid_file = [
            'doc_five_non_numerical_id.txt',
            'doc_6.txt',
            'invalid_file.txt', ]
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', './documents_1']), redirect_stdout(cout):
            ci.main()
        s = cout.getvalue()
        # test whether 'create_index' has catched these invalid files
        for f_name in invalid_file:
            self.assertTrue(f_name in s)

    def test_index_correctness(self):
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', './documents_2']), redirect_stdout(cout):
            ci.main()
        f_path = join('.', INDEX_FILE)
        # test if the index file has been created
        self.assertTrue(isfile(f_path))
        index_file = open(f_path)
        for line in index_file.readlines():
            term, index = line.split(maxsplit=1)
            posting = ast.literal_eval(index)
            self.assertTrue(type(posting) == dict)
        index_file.close()

    def test_index_file_already_exist(self):
        # create a dummy index file
        f_path = join('.', INDEX_FILE)
        with open(f_path, "w") as f:
            f.write("")
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', './documents_1']), redirect_stdout(cout):
            ci.main()
        s = cout.getvalue()
        self.assertTrue('already exist' in s)


if __name__ == '__main__':
    unittest.main()
