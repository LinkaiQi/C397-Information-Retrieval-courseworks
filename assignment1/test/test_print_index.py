import sys, io, os
from os.path import join, isfile
from contextlib import redirect_stdout

import unittest
from unittest.mock import patch

# set up relative path for programs to be tested
program_path = sys.path[0] + "/../"
sys.path.append(program_path)

import create_index as ci
import print_index as pi
from util import INDEX_FILE




class TestPrintIndex(unittest.TestCase):

    def set_up_index_file(self):
        # remove index file if it exists
        f = join('.', INDEX_FILE)
        if isfile(f):
            os.remove(f)
        # generate a new index file
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', './documents_2']), redirect_stdout(cout):
            ci.main()

    def test_no_index_file(self):
        # remove index file if it exists
        f = join('.', INDEX_FILE)
        if isfile(f):
            os.remove(f)
        # run print_index
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', '.']), redirect_stdout(cout):
            pi.main()
        s = cout.getvalue()
        # print_index should show error msg if no index file is found
        self.assertTrue('Error! Index file does not find' in s)

    def test_invalid_index_file(self):
        # insert a invalid line in the index file
        f_path = join('.', INDEX_FILE)
        with open(f_path, "w") as f:
            # incorrect index format
            f.write("system_1:[1]_2:[2,3]\n")
        # run print_index
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', '.']), redirect_stdout(cout):
            pi.main()
        s = cout.getvalue()
        self.assertTrue('Error! Invalided index file format' in s)

    def test_printed_index_correctness(self):
        self.set_up_index_file()
        # run print_index
        cout = io.StringIO()
        with unittest.mock.patch('sys.argv', ['python', '.']), redirect_stdout(cout):
            pi.main()
        s = cout.getvalue()
        self.assertTrue('retrieval \t 1:3;2:3' in s)
        self.assertTrue('word \t 4:22 ' in s)


if __name__ == '__main__':
    unittest.main()
