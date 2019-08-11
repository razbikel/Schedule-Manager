import sqlite3
import os
import atexit
import sys

DBExist = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')
with dbcon:
    cursor = dbcon.cursor()


def close_db():
    dbcon.commit()
    dbcon.close()


atexit.register(close_db)


def create_tables():
    cursor.execute(""" CREATE TABLE courses(id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    student TEXT NOT NULL,
    number_of_students INTEGER NOT NULL,
    class_id INTEGER REFERENCES classrooms(id),
    course_length INTEGER NOT NULL)
    """)
    cursor.execute(""" CREATE TABLE students( grade TEXT PRIMARY KEY,
    count INTEGER NOT NULL)
    """)
    cursor.execute(""" CREATE TABLE classrooms( id INTEGER PRIMARY KEY,
    location TEXT NOT NULL,
    current_course_id INTEGER NOT NULL,
    current_course_time_left INTEGER NOT NULL)
    """)


def insert_course(id, course_name, student, number_of_students, class_id, course_length):
    cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?)",
                   (id, course_name, student, number_of_students, class_id, course_length))


def insert_student(grade, count):
    cursor.execute("INSERT INTO students VALUES (?, ?)", (grade, count))


def insert_classroom(id, location, current_course_id, current_course_time_left):
    cursor.execute("INSERT INTO classrooms VALUES (?, ?, ?, ?)",
                   (id, location, current_course_id, current_course_time_left))


def print_Tables():
    cursor.execute("SELECT * FROM courses")
    list_courses = cursor.fetchall()
    print('courses')
    for item in list_courses:
        print(item)

    cursor.execute("SELECT * FROM classrooms")
    list_classes = cursor.fetchall()
    print('classrooms')
    for item in list_classes:
        print(item)

    cursor.execute("SELECT * FROM students")
    list_students = cursor.fetchall()
    print('students')
    for item in list_students:
        print(item)


def insert_Tables_From_Config(config):
    with open(config) as inputfile:
        for line in inputfile:
            s = line.split(', ')
            if s[0] == 'S':
                insert_student(s[1].strip(), s[2].strip())
            elif s[0] == 'C':
                insert_course(s[1].strip(), s[2].strip(), s[3].strip(), s[4].strip(), s[5].strip(), s[6].strip())
            elif s[0] == 'R':
                insert_classroom(s[1].strip(), s[2].strip(), 0, 0)


def main(argv):
    if not DBExist:
        create_tables()
        insert_Tables_From_Config(argv[1])
        print_Tables()


if __name__ == '__main__':
    main(sys.argv)
