"""
@author: Tehreem Tungekar
The main objective of this program is to
begin to build the framework for a project and
summarize student and instructor data
This program has a class named University,
a class named Student and another named Instructor
Added a new class named Majors
"""

from prettytable import PrettyTable
import csv
from collections import defaultdict
from typing import Tuple, Iterator, List, Set, Dict


def file_reader(
            path: str, fields: int, sep=',',
            header=False) -> Iterator[Tuple[str]]:
    """ This function reads field-separated text files and
    yields a tuple with all of the values from a
    single line in the file on each call to next()
    """
    try:
        fp = open(path, 'r')

    except FileNotFoundError:
        print("File not found!")

    else:
        line_num: int = 0
        with fp:
            reader = csv.reader(fp, delimiter=sep)
            for line in reader:
                line_num += 1
                if len(line) != fields:
                    print(
                        f'{path} has {len(line)} fields on',
                        'line {line_num} expected {fields}')
                if header is False:
                    yield tuple(line)
                else:
                    header = False


class University:
    """ This class holds all of  the students,
    instructors and grades for a single University
    """
    def __init__(self, path: str, tables: bool = True) -> None:
        """Init method for University"""
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._major: Dict[str, Major] = dict()

        student_path = "students.txt"
        instructor_path = "instructors.txt"
        grades_path = "grades.txt"
        major_path = "majors.txt"

        try:
            """It is important to execute get_major()
            before get_students() to avoid errors
            """
            self._get_major(major_path)
            self._get_students(student_path)
            self._get_instructors(instructor_path)
            self._get_grades(grades_path)

        except (FileNotFoundError, ValueError) as e:
            print(e)

        else:
            if tables:
                print("\nMajors Table:")
                self.major_table()
                print("\nStudent Table:")
                self.student_table()
                print("\nInstructor Table:")
                self.instructor_table()

    def _get_students(self, path) -> None:
        """Student's details are read using file_reader method
        and added to students dictionary
        """
        for cwid, name, major in file_reader(path, 3, sep=';', header=True):
            if major not in self._major:
                print(f"Student {cwid} '{name}' has unknown major '{major}'")
            else:
                self._students[cwid] = Student(cwid, name, self._major[major])

    def _get_instructors(self, path) -> None:
        """Instructor's details are read using
        file_reader method and added to instructor dictionary"""
        for cwid, name, dept in file_reader(path, 3, sep='|', header=True):
            self._instructors[cwid] = Instructor(cwid, name, dept)

    def _get_grades(self, path) -> None:
        """Grades are read using file_reader
        method and assigned to student and instructor"""
        for std_cwid, course, grade, instructor_cwid in file_reader(
                                            path, 4, sep='|', header=True):
            if std_cwid in self._students:
                self._students[std_cwid].add_course(course, grade)
            else:
                print(f'Student with {std_cwid} not found in Student file')

            if instructor_cwid in self._instructors:
                self._instructors[instructor_cwid].add_student(course)
            else:
                print(f'Instructor {instructor_cwid} not in Instructor File')

    def _get_major(self, path) -> None:
        """Majors are read using file_reader method and students summary
        table has to be updated using the same information
        """
        for major, flag, course in file_reader(path, 3, sep='\t', header=True):
            if major not in self._major:
                self._major[major] = Major(major)
            self._major[major].add_course(course, flag)

    def student_table(self) -> None:
        """This function Pretty Prints Student table"""
        table = PrettyTable(field_names=Student.FIELD_NAMES)
        for student in self._students.values():
            table.add_row(student.info())
        print(table)

    def instructor_table(self) -> None:
        """This function Pretty Prints Instructor table"""
        table = PrettyTable(field_names=Instructor.FIELD_NAMES)
        for instructor in self._instructors.values():
            for row in instructor.info():
                table.add_row(row)
        print(table)

    def major_table(self) -> None:
        """This table Pretty Print Majors table"""
        table = PrettyTable(field_names=Major.FIELD_NAMES)
        for major in self._major.values():
                table.add_row(major.info())
        print(table)


class Student:
    """This class holds all of the details of a student,
    including a dict to store the classes taken and the grade
    where the course is the key and the grade is the value
    """

    FIELD_NAMES: List[str] = ['CWID', 'Name', 'Major',
                              'Completed Courses', 'Remaining Required',
                              'Remaining Electives', 'GPA']

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """Init method for Student class"""
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict()

    def add_course(self, course: str, grade: str) -> None:
        """Adding courses with grades"""
        self._courses[course] = grade

    def gpa(self) -> float:
        """This method is calculating the GPA using a dictionary"""
        grades: Dict[str, float] = {'A': 4.0, 'A-': 3.75, 'B+': 3.25,
                                    'B': 3.0, 'B-': 2.75,
                                    'C+': 2.25, 'C': 2.0,
                                    'C-': 0.00, 'D+': 0.00,
                                    'D': 0.00, 'D-': 0.00, 'F': 0.00}
        try:
            total: float = sum(
                [grades[grade]
                    for grade in self._courses.values()]
                ) / len(self._courses.values())
            return round(total, 2)
        except ZeroDivisionError as e:
            print(e)

    def info(self) -> Tuple[str, str, str, List[str], List[str], List[str]]:
        """This method returns a list of information needed for generating
        pretty table """
        major, passed, remaining, electives = self._major.remaining(
            self._courses)

        return [self._cwid, self._name, major,
                sorted(passed), sorted(remaining),
                sorted(electives), self.gpa()]


class Instructor:
    """This class holds all of the details of an instructor,
    including a defaultdict(int) to store the names of the courses
    taught along with the number of students who have taken the course
    """
    FIELD_NAMES = ['CWID', 'Name', 'Dept', 'Course', 'Number of Students']

    def __init__(self, cwid: str, name: str, dept: str) -> None:
        """Init method for Instructor Class
        """
        self._cwid: str = cwid
        self._name: str = name
        self._dept: str = dept
        self._courses: DefaultDict[str, int] = defaultdict(int)

    def add_student(self, course: str) -> None:
        """Number of students taking course with Instructor"""
        self._courses[course] += 1

    def info(self) -> Iterator[Tuple[str, str, str, str, int]]:
        """Yields the row of Instructors"""
        for course, count in self._courses.items():
            yield [self._cwid, self._name, self._dept, course, count]


class Major:
    """This class holds all the information
    about majors
    """
    FIELD_NAMES = ['Major', 'Required Courses', 'Electives']
    GRADES: Set[str] = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, major: str) -> None:
        """
        Init method for Major class
        """
        self._major: str = major
        self._required: Set[str] = set()
        self._electives: Set[str] = set()

    def add_course(self, course: str, option: str) -> None:
        """Adding a course by determining
        if it is elective or required
        """
        if option == 'R':
            self._required.add(course)
        elif option == 'E':
            self._electives.add(course)
        else:
            print("Invalid Course Flag!")

    def remaining(
            self,
            completed: Dict[str, str]) -> Tuple[str,
                      List[str], List[str], List[str]]:
        """Adding remaining courses not passed/enrolled in and electives"""
        passed: Set[str] = {course for course,
                            grade in completed.items()
                            if grade in Major.GRADES}
        remaining: Set[str] = self._required - passed
        electives: Set[str] = self._electives

        if self._electives.intersection(passed):
            electives = []

        return self._major, list(passed), list(remaining), list(electives)

    def info(self) -> Tuple[str, List[str], List[str]]:
        """ Returning information about majors"""
        return [self._major, sorted(self._required), sorted(self._electives)]


def main():
    University('Homework_10')


if __name__ == '__main__':
    main()
