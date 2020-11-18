"""
@Tehreem Tungekar
This file has test cases to test classes
and functions defined in
Student_Repository_Tehreem_Tungekar.py
This is HW11
"""
import unittest
import sqlite3
from Student_Repository_Tehreem_Tungekar import University, Student, Instructor, Major


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
        expectMajor = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'],
                       ['CS 501', 'CS 546']],
                       ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]

        actual = [major.info()
                  for major in self.univ._major.values()]
        self.assertEqual(expectMajor, actual)

    def test_student_attributes(self) -> None:
        """This function tests for student details"""

        expectSt = [['10103', 'Jobs, S', 'SFEN',
                    ['CS 501', 'SSW 810'],
                    ['SSW 540', 'SSW 555'], [], 3.38],
                    ['10115', 'Bezos, J', 'SFEN',
                    ['SSW 810'], ['SSW 540', 'SSW 555'],
                    ['CS 501', 'CS 546'], 2.0],
                    ['10183', 'Musk, E', 'SFEN',
                    ['SSW 555', 'SSW 810'],
                    ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
                    ['11714', 'Gates, B', 'CS',
                    ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]]

        actual = [student.info()
                  for cwid, student in self.univ._students.items()]
        self.assertEqual(expectSt, actual)

    def test_instructor_attributes(self) -> None:
        """This function tests for Instructor details"""
        expectIn = [[['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]

        actual = [list(detail) for instructor in self.univ._instructors.values() for detail in instructor.info()]
        self.assertEqual(expectIn, actual)


    def test_student_summary_table_db(self) -> None:
        """ Testing students summary table """
        expected = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                    ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                    ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                    ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                    ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                    ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                    ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                    ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                    ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]

        calculated = []
        db = sqlite3.connect("hw11.db")
        for row in db.execute("select students.Name,students.CWID,Course,Grade,instructors.name from students join grades on students.CWID= StudentCWID join instructors on InstructorCWID=instructors.CWID order by students.Name"):
            calculated.append(row)
        self.assertEqual(expected, calculated)


if __name__ == "__main__":
    """Main method to run test cases"""
    unittest.main(exit=False, verbosity=2)
