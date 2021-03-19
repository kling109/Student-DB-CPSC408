###
# interface.py
#
# A program for managing the content of the Student database.
# A basic CRUD app.  This file handles user input and validation.
#
# Developed by: Trevor Kling
# Last Date Modified: 03/19/2021
###

import re
from studentsdb import StudentDB

# Designed using Regex101
phone_pattern = "^\+?(\d)?(\-)?\(?(\d{3})\)?(\.)?(\-)?(\d{3})(\-)?(\d{3})?(\-)?(\.)?(\d{4})(((ext)|x|(\-))(\d+))?$"
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware"
          "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky"
          "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi"
          "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico"
          "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania"
          "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont"
          "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]

def initialize():
    """
    Produces a StudentDB object to use the various commands with.

    :param path: A string path to the necessary file.
    :return: StudentDB db
    """
    db = StudentDB()
    return db

def read_csv(db: StudentDB, path: str):
    """
    Reads in a CSV file and places its contents in the database object.

    :param db: The database being operated on.
    :param path: Path to the csv object in question
    :return: None
    """
    db.read_csv(path)


def display_db(db: StudentDB):
    """
    Prints the database to the command line.

    :param db: The database to display.
    :return: None.
    """
    db.display_students()


def add_student(db: StudentDB):
    """
    Adds a student to the database.

    :param db: The database to add a student into.
    :return: None
    """
    f_name = input("Input student first name: ")
    l_name = input("Input student last name: ")

    gpa = input("Input student GPA: ")
    try:
        gpa = float(gpa)
    except ValueError:
        print("The given GPA is not a valid number.")
        return None

    major = input("Input student major: ")
    address = input("Input student address: ")
    city = input("Input student city: ")
    sstate = input("Input student state: ")
    if sstate not in states:
        print("The given state is formatted incorrectly.  States should be spelled correctly and capitalized.")
        return None

    zip_code = input("Input student zip code: ")
    if (not re.match("\d{5}(\-\d{4})?", zip_code)):
        print("The given zip code is formatted incorrectly.  Zip codes should follow a formatting like \n"
              "01234-5678.")
        return None

    phone = input("Input student phone number: ")
    if (not re.match(phone_pattern, phone)):
        print("The given phone number is formatted incorrectly. Phone numbers should be formatted like \n"
              "(123)867-5309, or 123-867-5309")
        return None

    params = [f_name, l_name, gpa, major, address, city, sstate, zip_code, phone, 0]
    db.add_student(params)


def update_major(db: StudentDB, id: int, new_major: str):
    """
    Update the major for a given student.

    :param db: The database to update
    :param id: The ID of the student who's major is changing
    :param new_major: The new major
    :return: None
    """
    db.update_student_major(id, new_major)


def update_advisor(db: StudentDB, id: int, new_advisor: str):
    """
    Update the advisor for a given student.

    :param db: The database to update
    :param id: The ID of the student who's advisor is changing
    :param new_advisor: The new advisor
    :return: None
    """
    db.update_student_advisor(id, new_advisor)


def update_phone(db: StudentDB, id: int, new_phone: str):
    """
    Update the phone number for a given student

    :param db: The database to update
    :param id: The ID of the student who's phone number is changing
    :param new_phone: The new phone number
    :return: None
    """
    if (re.match(phone_pattern, new_phone)):
        db.update_student_phone(id, new_phone)
    else:
        print("The given phone number is formatted incorrectly. Phone numbers should be formatted like \n"
              "(123)867-5309, or 123-867-5309")


def delete_student(db: StudentDB, id : int):
    """
    Delete a student from the database.

    :param db: The database to modify
    :param id: The student to remove's id number
    :return: None
    """
    db.delete_student(id)


def search_student(db: StudentDB):
    """
    Allows the user to search the database for students of a variety of types.

    :param db: The database to search
    :return: None.
    """
    print("Students can be searched by:")
    print("1. Major, 2. GPA, 3. City, 4. State, 5. Faculty Advisor")
    choice = input("Select a search method: (1 - 5) ")
    if (choice == "1"):
        major = input("Input the major you would like to find all students from: ")
        db.search_student('Major', "==", major)
    elif (choice == "2"):
        print("Available Operations:")
        print("1. Less Than (<), 2. Greater Than (>), 3. Equal (==), 4. Greater Than or Equal To (>=), 5. Less"
              "Than or Equal To (<=)")
        operator = input("Select an operation: (1 - 5) ")
        gpa = input("Input the GPA you would like to sort by: ")
        if (operator == "1"):
            db.search_student("GPA", "<", gpa)
        elif (operator == "2"):
            db.search_student("GPA", ">", gpa)
        elif (operator == "3"):
            db.search_student("GPA", "==", gpa)
        elif (operator == "4"):
            db.search_student("GPA", ">=", gpa)
        elif (operator == "5"):
            db.search_student("GPA", "<=", gpa)
        else:
            print("That is not a valid choice of operation.")
    elif (choice == "3"):
        city = input("Input the city you would like to find all students from: ")
        db.search_student('City', "==", city)
    elif (choice == "4"):
        state = input("Input the state you would like to find all students from: ")
        db.search_student('State', "==", state)
    elif (choice == "5"):
        advisor = input("Input the advisor you would like to find all students for: ")
        db.search_student('FacultyAdvisor', "==", advisor)
    else:
        print("That is not an accepted search option.")

def run_db():
    """
    Runs the user interaction loop for the program.

    :return: None
    """
    db = initialize()
    run = True
    print("Welcome to the Student Database Management System")
    print("-------------------------------------------------")
    while (run):
        print("- Command List -")
        print("1. Import CSV File")
        print("2. Display All Students")
        print("3. Add New Student")
        print("4. Update Student Information")
        print("5. Delete Student Record")
        print("6. Search Student Records")
        print("7. Exit")
        act = input("Select an option: (1-7) ")
        if (act == "1"):
            path = input("Please input a file path: ")
            read_csv(db, path)
        elif (act == "2"):
            display_db(db)
        elif (act == "3"):
            add_student(db)
        elif (act == "4"):
            id = input("Please select a student ID to update: ")
            print("The fields available to change are:")
            print("1. Major, 2. Advisor, 3. Phone Number")
            field = input("Please select an option: (1-3) ")
            if (field == "1"):
                major = input("Please input the new choice of major: ")
                update_major(db, id, major)
            elif (field == "2"):
                advisor = input("Please input the new choice of advisor: ")
                update_advisor(db, id, advisor)
            elif (field == "3"):
                phone = input("Please input the new choice of phone number: ")
                update_phone(db, id, phone)
            else:
                print("The option you selected is invalid.")
        elif (act == "5"):
            id = input("Please select a student ID to delete: ")
            delete_student(db, id)
        elif (act == "6"):
            search_student(db)
        elif (act == "7"):
            run = False
        else:
            print("The command you selected is invalid.  Please type a number between 1 and 6.")


if __name__ == '__main__':
    run_db()



