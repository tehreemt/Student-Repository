"""
@author: Tehreem Tungekar
This file has a class named TestHW08 which has test cases
implemented to test functions defined in HW08_Tehreem_Tungekar.py
Namely, date_arithmetic(), file_reader(), analyze_files(), pretty_print()
"""

import unittest
from datetime import datetime
import pprint
from HW08_Tehreem_Tungekar import date_arithmetic, file_reader, FileAnalyzer


class TestHW08(unittest.TestCase):
    """
    This class implements test case functions to test
    for functions implemented in HW08_Tehreem_Tungekar
    """
    def test_date_arithmetic(self) -> None:
        """
        This function has test cases for date_arithmetic()
        """
        self.assertEqual(
            date_arithmetic(),
            (datetime(2020, 3, 1, 0, 0), datetime(2019, 3, 2, 0, 0), 241))
        self.assertNotEqual(
            date_arithmetic(),
            ('Mar 02, 2020', 'Mar 03, 2019', 21))

    def test_file_reader(self) -> None:
        """
        This function has test cases for file_reader()
        """
        expect = [('123', 'Jin He', 'Computer Science'),
                  ('234', 'Nanda Koka', 'Software Engineering'),
                  ('345', 'Benji Cai', 'Software Engineering')]
        self.assertEqual(
            list(file_reader('./testFile.txt', 3, '|', True)), expect)
        self.assertNotEqual(
            list(file_reader('./testFile.txt', 3, '|')), expect)
        with self.assertRaises(ValueError):
            list(file_reader('./testFile.txt', 4, '|', True))
        with self.assertRaises(FileNotFoundError):
            list(file_reader('xyz.txt', 3, '|', True))

    def test_analyze_files(self) -> None:
        """
        This function has test cases for analyze_files()
        """
        test = FileAnalyzer('C:/Users/Tehreem/Downloads/TestHW08')
        expected = {'0_defs_in_this_file.py':
                    {'classes': 0,
                     'functions': 0, 'lines': 3, 'characters': 57},
                    'file1.py':
                    {'classes': 2, 'functions': 4, 'lines': 25,
                        'characters': 270}}
        self.assertEqual(test.files_summary, expected)
        with self.assertRaises(FileNotFoundError):
            FileAnalyzer(' ')


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
