###
# studentsdb.py
#
# A program for managing the content of the Student database.
# A basic CRUD app.  This file handles accessing the database.
#
# Developed by: Trevor Kling
# Last Date Modified: 03/19/2021
###

import sqlite3
import os.path
import pandas as pd
from os import path


class StudentDB:

    cols = ["StudentId", "FirstName", "LastName", "GPA", "Major", "FacultyAdvisor", "Address", "City", "State", "ZipCode", "MobilePhoneNumber"]
    conn = None
    student_cursor = None

    def __init__(self):
        self.conn = sqlite3.connect("./StudentDB.sqlite")
        self.student_cursor = self.conn.cursor()


    def __delete__(self, instance):
        self.conn.close()
        del self.student_cursor
        del self.conn


    def read_csv(self, csv_path: str):
        """
        A function to handle importing a given CSV into the Students Database

        :param csv_path: String representing the path the the desired CSV file.
        :return: None
        """
        if path.exists(csv_path):
            i = 0
            with open(csv_path) as input_file:
                columns = input_file.readline()
                data = input_file.readlines()

            columns = columns.strip().split(',')

            records = []
            for i in data:
                i = i.strip().split(',')
                f_name = i[0]
                l_name = i[1]
                addr = i[2]
                city = i[3]
                state = i[4]
                zip_code = i[5]
                phone = i[6]
                major = i[7]
                gpa = float(i[8])
                is_del = 0
                records.append((f_name, l_name, gpa, major, addr, city,
                                state, zip_code, phone, is_del))

            self.conn.executemany(("INSERT INTO Student(FirstName, LastName, "
                              "GPA, Major, Address, City, State, ZipCode, "
                              "MobilePhoneNumber, isDeleted) "
                              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"), records)
            self.conn.commit()
        else:
            print("The given path does not result in a file.")


    def display_students(self):
        """
        Displays all students in the database to the command line.
        :return: None
        """
        self.student_cursor.execute("SELECT StudentId, FirstName, LastName, "
                              "GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, "
                              "MobilePhoneNumber FROM Student WHERE isDeleted == 0;")
        records = self.student_cursor.fetchall()
        if len(records) > 0:
            df = pd.DataFrame(records)
            df.columns = self.cols
            # Setup to print full dataframe rather than cross-section
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(df.to_string(index=False))
        else:
            print("There are no values in the database yet.")


    def add_student(self, params):
        """
        Adds a student to the database.

        :param params: The information that determines the student's parameters
        :return: None
        """
        self.student_cursor.execute(("INSERT INTO Student(FirstName, LastName, "
                           "GPA, Major, Address, City, State, ZipCode, "
                           "MobilePhoneNumber, isDeleted) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"), params)
        self.conn.commit()


    def update_student_major(self, id: int, new_major: str):
        """
        Updates the major of a given student by ID.

        :param id: The ID of the student to update.
        :param new_major: The new major to assign the given student
        :return: None
        """
        self.student_cursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?", (new_major, id))
        self.conn.commit()


    def update_student_advisor(self, id: int, new_advisor: str):
        """
        Updates the advisor of a given student by ID.

        :param id: The ID of the student to update.
        :param new_advisor: The name of the student's new advisor
        :return: None
        """
        self.student_cursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (new_advisor, id))
        self.conn.commit()


    def update_student_phone(self, id: int, new_phone: str):
        """
        Updates the phone number of a given student by ID.

        :param id: The ID of the student to update.
        :param new_phone: The new phone number for the student.
        :return: None
        """
        self.student_cursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (new_phone, id))
        self.conn.commit()


    def delete_student(self, id: int):
        """
        Performs a soft delete of a given student by ID.  The isDeleted field
        is set to 1, and the student will not be displayed in following searches.

        :param id: The ID of the student to delete.
        :return: None
        """
        self.student_cursor.execute("UPDATE Student SET isDeleted = 1 WHERE StudentId = ?", (id,))
        self.conn.commit()


    def search_student(self, *args):
        """
        Searches the database for a student matching a set of conditions passed in
        via args.

        :param args: A list of conditions for the student to match.
        :return:
        """
        col = args[0]
        op = args[1]
        val = args[2]

        self.student_cursor.execute('SELECT StudentId, FirstName, LastName, '
                              'GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, '
                              'MobilePhoneNumber FROM Student WHERE ' + col + op + '? AND isDeleted == 0;', (val,))
        records = self.student_cursor.fetchall()
        if len(records) > 0:
            df = pd.DataFrame(records)
            df.columns = self.cols
            # Setup to print full dataframe rather than cross-section
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(df.to_string(index=False))
        else:
            print("This query returned no results.")


