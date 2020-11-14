"""
@author: Tehreem Tungekar
There are three parts in this assignment:
Part 1: Date Arithmetic Operations
Part 2: field separated file reader
Part 3: Scanning directories and files
"""
import csv
import os
from prettytable import PrettyTable
from datetime import datetime, timedelta
from typing import Tuple, Iterator


def date_arithmetic() -> Tuple[datetime, datetime, int]:
    """ This function answers the following questions and returns a tuple:
1. What is the date three days after Feb 27, 2020?
2. What is the date three days after Feb 27, 2019?
3. How many days passed between Feb 1, 2019 and Sept 30, 2019?
"""
    date1: str = "Feb 27, 2020"
    date2: str = "Feb 27, 2019"
    date3: str = "Feb 1, 2019"
    date4: str = "Sep 30, 2019"

    dt1: datetime = datetime.strptime(date1, "%b %d, %Y")
    dt2: datetime = datetime.strptime(date2, "%b %d, %Y")
    dt3: datetime = datetime.strptime(date3, "%b %d, %Y")
    dt4: datetime = datetime.strptime(date4, "%b %d, %Y")

    num_days: int = 3
    res1: datetime = dt1 + timedelta(num_days)
    res2: datetime = dt2 + timedelta(num_days)

    delta: datetime = dt4 - dt3
    res3: int = delta.days
    return res1, res2, res3


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
        raise FileNotFoundError("File not found!")

    else:
        line_num: int = 0
        with fp:
            reader = csv.reader(fp, delimiter=sep)
            for line in reader:
                line_num += 1
                if len(line) != fields:
                    raise ValueError(
                        f'{path} has {len(line)} fields on',
                        'line {line_num} expected {fields}')
                if header is False:
                    yield tuple(line)
                else:
                    header = False
        fp.close()


class FileAnalyzer:
    """ This class when given a directory name,
    searches that directory for Python files.
    For each file, opens it and calculates
    a summary of the file
    """
    def __init__(self, directory: str) -> None:
        """ """
        self.directory: str = directory
        self.files_summary: Dict[str, Dict[str, int]] = dict()

        self.analyze_files()

    def analyze_files(self) -> None:
        """ This is a method that populates the summarized
        data into self.files_summary
        """
        path: str = self.directory
        direct: List[str] = os.listdir(path)
        for f in direct:
            if f.endswith('.py'):
                try:
                    fp = open(os.path.join(path, f), 'r')
                except FileNotFoundError:
                    raise FileNotFoundError("Unable to open file!")
                else:
                    with fp:
                        character_count: int = 0
                        class_count: int = 0
                        function_count: int = 0
                        line_count: int = 0

                        for line in fp:
                            character_count += len(line)
                            line_count += 1

                            if line.strip().startswith('def '):
                                function_count += 1
                            if line.startswith('class '):
                                class_count += 1

                        self.files_summary[f] = {
                            'classes': class_count,
                            'functions': function_count,
                            'lines': line_count,
                            'characters': character_count
                        }

    def pretty_print(self) -> None:
        """ This is a method that prints out the pretty table
        from the data stored in the self.files_summary
        """
        pretty: PrettyTable = PrettyTable()
        pretty.field_names = ['File Name', 'Classes',
                              'Functions', 'Lines', 'Characters']

        for i, j in self.files_summary.items():
            pretty.add_row([i, j['classes'], j['functions'],
                            j['lines'], j['characters']])

        print("\nSummary for ", self.directory)
        print(pretty)
