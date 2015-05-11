"""
juxtapy directory and file nose tests


project    : juxtapy
version    : 0.1.0
status     : development
modifydate : 2015-04-28 20:38:00 -0700
createdate : 2015-04-26 08:54:00 -0700
website    : https://github.com/tmthydvnprt/juxtapy
author     : tmthydvnprt
email      : tmthydvnprt@users.noreply.github.com
maintainer : tmthydvnprt
license    : MIT
copyright  : Copyright 2015, juxtapy
credits    :

"""

# test dependancies
import os
import unittest

# testing dependancies
import juxtapy.juxta

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
        jxt = juxtapy.juxta.Juxta(FROM_PATH, TO_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertNotEqual(response, 'ERROR: from and to path are not compatible')

    def test2(self):
        """ test directory comparison fails"""
        jxt = juxtapy.juxta.Juxta(FROM_PATH, TO_FILE_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertEqual(response, 'ERROR: from and to path are not compatible')

class FileTests(unittest.TestCase):
    """ test directory comparison"""

    def test1(self):
        """ test file comparison passes"""
        jxt = juxtapy.juxta.Juxta(FROM_FILE_PATH, TO_FILE_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertNotEqual(response, 'ERROR: from and to path are not compatible')

    def test2(self):
        """ test file comparison fails"""
        jxt = juxtapy.juxta.Juxta(FROM_FILE_PATH, TO_PATH, OUTPUT_PATH)
        response = jxt.compare()
        self.assertEqual(response, 'ERROR: from and to path are not compatible')

class WriteIndex(unittest.TestCase):
    """ write an index.html for test site"""

    def test1(self):
        """test index.html"""
        juxtapy.juxta.write_index(OUTPUT_PATH)
        self.assertEqual(True, True)
