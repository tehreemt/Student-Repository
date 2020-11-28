"""
@author: Tehreem Tungekar
This is an implementation of Flask
and Jinja2 for Homework 12
The program displays output in a tabular format
in web page on 127.0.0.1:5000/students
"""
import sqlite3
from flask import Flask, render_template
from typing import Dict

app: Flask = Flask(__name__)


@app.route('/students/')
def student_summary() -> str:
    """This function has Query for Students Grades """
    db_path: str = 'hw11.db'

    db: sqlite3.Connection = sqlite3.connect(db_path)
    query: str = """select students.Name, students.CWID, grades.Course,
    grades.Grade, instructors.Name from students,grades,instructors where
    students.CWID=StudentCWID and InstructorCWID=instructors.CWID
    order by students.Name"""

    data: Dict[str,
               str] = [{'Name': name,
                        'CWID': cwid,
                        'Course': course,
                        'Grade': grade,
                        'Instructor': instructor} for name, cwid, course,
                       grade, instructor in db.execute(query)]
    db.close()

    return render_template(
            'students.html',
            title='Stevens Repository',
            table_title='Student, Course, Grade, and Instructor',
            students=data)

app.run(debug=True)
