"""
juxtapy directory and file nose tests
"""

# test dependancies
import os
import unittest

# testing dependancies
from juxtapy.juxta import Juxta

# test inputs
CURRENT_PATH = os.path.dirname(__file__)
FROM_PATH = os.path.join(CURRENT_PATH, 'inputs', 'from')
TO_PATH = os.path.join(CURRENT_PATH, 'inputs', 'to')
FROM_FILE_PATH = os.path.join(CURRENT_PATH, 'inputs', 'from.txt')
TO_FILE_PATH = os.path.join(CURRENT_PATH, 'inputs', 'to.txt')
OUTPUT_PATH = os.path.join(CURRENT_PATH, 'outputs')

# test cases
class DirectoryTests(unittest.TestCase):
    """ test directory comparison"""

    def test1(self):
        """ test directory comparison passes"""
        jxt = Juxta(FROM_PATH, TO_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertNotEqual(response, 'ERROR: from and to patch are not compatible')

    def test2(self):
        """ test directory comparison fails"""
        jxt = Juxta(FROM_PATH, TO_FILE_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertEqual(response, 'ERROR: from and to patch are not compatible')

class FileTests(unittest.TestCase):
    """ test directory comparison"""

    def test1(self):
        """ test file comparison passes"""
        jxt = Juxta(FROM_FILE_PATH, TO_FILE_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertNotEqual(response, 'ERROR: from and to patch are not compatible')

    def test2(self):
        """ test file comparison fails"""
        jxt = Juxta(FROM_FILE_PATH, TO_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertEqual(response, 'ERROR: from and to patch are not compatible')
