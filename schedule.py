import sqlite3
import os


def main():
    DBExist = os.path.isfile('schedule.db')
    if DBExist:
        dbcon = sqlite3.connect('schedule.db')
        cursor = dbcon.cursor()

        def courses_Is_Not_Empty():
            cursor.execute("SELECT * FROM courses")
            return len(cursor.fetchall()) is not 0

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

        if courses_Is_Not_Empty() is not True:
            print_Tables()

        i = 0

        while os.path.isfile('schedule.db') and courses_Is_Not_Empty():
            cursor.execute("SELECT * FROM classrooms")
            classes = cursor.fetchall()

            for item in classes:
                time = item[3]
                if time is 0:
                    cursor.execute("SELECT * FROM courses WHERE courses.class_id = ?", (item[0],))
                    course = cursor.fetchone()
                    if course is not None:
                        cursor.execute(
                            " UPDATE classrooms SET current_course_id = ? WHERE classrooms.id = ?",
                            (course[0], item[0]))
                        cursor.execute(
                            " UPDATE classrooms SET current_course_time_left = ? WHERE classrooms.id = ?",
                            (course[5], item[0]))
                        cursor.execute("SELECT * FROM students WHERE students.grade = ?", (course[2],))
                        student = cursor.fetchone()
                        cursor.execute("UPDATE students SET count = ? WHERE students.grade = ?",
                                       (student[1] - course[3], course[2]))
                        dbcon.commit()
                        location = item[1]
                        course_Name = course[1]
                        print("(" + str(i) + ") " + location + ": " + course_Name + " is schedule to start")
                elif time is 1:
                    cursor.execute("SELECT * FROM courses WHERE courses.id = ?", (item[2],))
                    course_To_Remove = cursor.fetchone()
                    location = item[1]
                    course_Name = course_To_Remove[1]
                    print("(" + str(i) + ") " + location + ": " + course_Name + " is done")
                    cursor.execute("DELETE FROM courses WHERE courses.id = ?", (course_To_Remove[0],))
                    dbcon.commit()
                    cursor.execute("SELECT * FROM courses WHERE courses.class_id = ?", (item[0],))
                    course = cursor.fetchone()
                    if course is not None:
                        cursor.execute("UPDATE classrooms SET current_course_id = ? WHERE classrooms.id = ?",
                                       (course[0], item[0]))
                        cursor.execute(
                            "UPDATE classrooms SET current_course_time_left = ? WHERE classrooms.id = ?",
                            (course[5], item[0]))
                        cursor.execute("SELECT * FROM students WHERE students.grade = ?", (course[2],))
                        student = cursor.fetchone()
                        cursor.execute("UPDATE students SET count = ? WHERE grade = ?",
                                       (student[1] - course[3], course[2]))
                        dbcon.commit()
                        location = item[1]
                        course_Name = course[1]
                        print("(" + str(i) + ") " + location + ": " + course_Name + " is schedule to start")
                    else:
                        cursor.execute("UPDATE classrooms SET current_course_id = ? WHERE classrooms.id = ?",
                                       (0, item[0]))
                        cursor.execute(
                            "UPDATE classrooms SET current_course_time_left = ? WHERE classrooms.id = ?",
                            (0, item[0]))
                        dbcon.commit()
                else:
                    cursor.execute(
                        "UPDATE classrooms SET current_course_time_left = ? WHERE classrooms.id = ?",
                        (item[3] - 1, item[0]))
                    cursor.execute("SELECT * FROM courses WHERE courses.id = ?", (item[2],))
                    course = cursor.fetchone()
                    dbcon.commit()
                    location = item[1]
                    course_Name = course[1]
                    print("(" + str(i) + ") " + location + ": " + "occupied by " + course_Name)
            i += 1
            print_Tables()


if __name__ == '__main__':
    main()
