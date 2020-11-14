"""
@Tehreem Tungekar
This file has test cases to test classes
and functions defined in HW10_Tehreem_Tungekar.py
"""
import unittest
from HW10_Tehreem_Tungekar import University, Student, Instructor, Major


class TestUniversity(unittest.TestCase):
    """This class has all testcases
    to test functions defined in
    HW10_Tehreem_Tungekar.py"""

    def setUp(self) -> None:
        """This methods allow you to define
        instructions that will be executed before
        and after each test method"""
        self.test_path: str = "Homework_10"
        self.univ: University = University(self.test_path, False)

    def test_majors(self) -> None:
        """This function tests majors table"""
        expectMajor = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
                       ['CS 501', 'CS 513', 'CS 545']],
                       ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'],
                       ['SSW 540', 'SSW 565', 'SSW 810']]]

        actual = [major.info()
                  for major in self.univ._major.values()]
        self.assertEqual(expectMajor, actual)

    def test_student_attributes(self) -> None:
        """This function tests for student details"""

        expectSt = [['10103', 'Baldwin, C', 'SFEN',
                    ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'],
                    ['SSW 540', 'SSW 555'], [], 3.44],
                    ['10115', 'Wyatt, X', 'SFEN',
                    ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'],
                    ['SSW 540', 'SSW 555'], [], 3.81],
                    ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'],
                    ['SSW 540', 'SSW 564'],
                    ['CS 501', 'CS 513', 'CS 545'], 3.88],
                    ['10175', 'Erickson, D', 'SFEN',
                    ['SSW 564', 'SSW 567', 'SSW 687'],
                    ['SSW 540', 'SSW 555'],
                    ['CS 501', 'CS 513', 'CS 545'], 3.58],
                    ['10183', 'Chapman, O', 'SFEN',
                    ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
                    ['CS 501', 'CS 513', 'CS 545'], 4.0],
                    ['11399', 'Cordova, I', 'SYEN', ['SSW 540'],
                    ['SYS 612', 'SYS 671', 'SYS 800'], [], 3.0],
                    ['11461', 'Wright, U', 'SYEN',
                    ['SYS 611', 'SYS 750', 'SYS 800'],
                    ['SYS 612', 'SYS 671'],
                    ['SSW 540', 'SSW 565', 'SSW 810'], 3.92],
                    ['11658', 'Kelly, P', 'SYEN', [],
                    ['SYS 612', 'SYS 671', 'SYS 800'],
                    ['SSW 540', 'SSW 565', 'SSW 810'], 0.0],
                    ['11714', 'Morton, A', 'SYEN',
                    ['SYS 611', 'SYS 645'],
                    ['SYS 612', 'SYS 671', 'SYS 800'],
                    ['SSW 540', 'SSW 565', 'SSW 810'], 3.0],
                    ['11788', 'Fuller, E', 'SYEN', ['SSW 540'],
                    ['SYS 612', 'SYS 671', 'SYS 800'], [], 4.0]]

        actual = [student.info()
                  for cwid, student in self.univ._students.items()]
        self.assertEqual(expectSt, actual)

    def test_instructor_attributes(self) -> None:
        """This function tests for Instructor details"""
        expectIn = [('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I',  'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)]

        actual = [tuple(
            detail) for instructor in self.univ._instructors.values(
        ) for detail in instructor.info()]
        self.assertEqual(expectIn, actual)


if __name__ == "__main__":
    """Main method to run test cases"""
    unittest.main(exit=False, verbosity=2)
