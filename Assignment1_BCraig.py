#Briana Craig
#Assignment 1 - sqlite
#CPSC 408-1
#brcraig@chapman.edu
import sqlite3
import csv

#declare initial database
def create_database():
    conn = sqlite3.connect('Students.db')
    cursor = conn.cursor()

    # Create the Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
            StudentId INTEGER PRIMARY KEY,
            FirstName TEXT,
            LastName TEXT,
            Address TEXT,
            City TEXT,
            State TEXT,
            ZipCode TEXT,
            MobilePhoneNumber TEXT,
            Major TEXT,
            GPA REAL,
            FacultyAdvisor TEXT,
            isDeleted INTEGER
        )
    ''')

    conn.commit()
    conn.close()

#convert data from csv to database
def import_data_from_csv():
    conn = sqlite3.connect('Students.db')
    cursor = conn.cursor()

    # Open the CSV file
    with open('students.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Skip the header row in the CSV
        next(csv_reader, None)
        for row in csv_reader:
            cursor.execute(''' INSERT INTO Students (StudentId, FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''', (csv_reader.line_num, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], "Default advisor", 0))
    conn.commit()
    conn.close()

#clean up and make sure everything is closed/empty
def close():
    conn = sqlite3.connect('Students.db')
    cursor = conn.cursor()
    endquery = "drop table Students"
    cursor.execute(endquery)
    conn.commit()
    conn.close()

#function to display all students in database
def display_all_students():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('Students.db')
        cursor = conn.cursor()

        select_query = 'SELECT * FROM Students WHERE isDeleted = 0'
        cursor.execute(select_query)
        rows = cursor.fetchall()

        for row in rows:
            for value in row[:-1]:  # exclude the last column, will all be 0 anyway
                print(value, end=', ')
            print()

        # Close the database connection
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

#function for adding a new student
def add_new_student():
    try:
        # Collect input from the user
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        gpa = input("Enter GPA: ")
        major = input("Enter Major: ")
        advisor = input("Enter Faculty Advisor: ")
        address = input("Enter Address: ")
        city = input("Enter City: ")
        state = input("Enter State: ")
        zip_code = input("Enter Zip Code: ")
        phone_number = input("Enter Mobile Phone Number: ")

        # Validate GPA
        try:
            gpa = float(gpa)
        except ValueError:
            print(f"Invalid GPA value: {gpa}. Aborting insertion.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect('Students.db')
        cursor = conn.cursor()

        # Insert the new student data into the database
        insert_query = '''INSERT INTO Students (StudentId, FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA, FacultyAdvisor, isDeleted)
                        VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(insert_query,
                       (first_name, last_name, address, city, state, zip_code, phone_number, major, gpa, advisor, 0))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        print("New student added successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

#function for updating a student's information
def update_student():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('Students.db')
        cursor = conn.cursor()

        student_id = input("Enter Student ID to update: ")
        #validate input is integer
        try:
            student_id = int(student_id)
        except ValueError:
            print(f"{student_id} is not an valid input, student id must be an integer.")
            return

        # Check if the student id is in table
        test_query = '''SELECT * from Students where StudentId = ?'''
        cursor.execute(test_query, (student_id, ), )
        results = cursor.fetchall()

        # Check if the result is not null
        if len(results) != 0:
            major = input("Enter Major: ")
            advisor = input("Enter Faculty Advisor: ")
            mobile_number = input("Enter Mobile Phone Number: ")
            # Update the specified student's data
            update_query = '''UPDATE Students SET Major = ?, FacultyAdvisor = ?, MobilePhoneNumber = ?
                                    WHERE StudentId = ?'''
            cursor.execute(update_query, (major, advisor, mobile_number, student_id))
            print("Student information updated successfully.")
        else:
            print("Student id not found")


        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

#function that soft deletes a student from the database
def delete_student():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('Students.db')
        cursor = conn.cursor()

        student_id = int(input("Enter Student ID to delete: "))
        #validate that input is an integer
        try:
            student_id_int = int(student_id)
        except ValueError:
            print(f"{student_id} is not an valid input, student id must be an integer.")
            return

        test_query = '''SELECT * from Students where StudentId = ?'''
        cursor.execute(test_query, (student_id_int,), )
        results = cursor.fetchall()

        # Check if the result is not null
        if len(results) != 0:
            delete_query = 'UPDATE Students SET isDeleted = 1 WHERE StudentId = ?'
            cursor.execute(delete_query, (student_id,))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        print("Student deleted successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

#function that returns search for a student with a certain attribute
def search_students():
    try:
        import sqlite3

        # Connect to the SQLite database
        conn = sqlite3.connect('Students.db')
        cursor = conn.cursor()

        #get input and remove punctuation and make all lower case
        search_option = input("Search by (Major/GPA/City/State/Advisor): ")
        filter_search_option = search_option.strip().lower()

        #check if the attribute the want to search by is valid
        if filter_search_option not in ['major', 'gpa', 'city', 'state', 'advisor']:
            print("Invalid search option.")
            conn.close()
            exit()

        #format the search field to match name of column in table
        if filter_search_option == "major":
            formatted_search_option = "Major"
        elif filter_search_option == "gpa":
            formatted_search_option = "GPA"
        elif filter_search_option == "city":
            formatted_search_option = "City"
        elif filter_search_option == "state":
            formatted_search_option = "State"
        else:
            formatted_search_option = "FacultyAdvisor"

        search_term = input(f"Enter the {formatted_search_option} to search for: ")
        search_query = f'SELECT * FROM Students WHERE {formatted_search_option} COLLATE NOCASE = ? AND isDeleted = 0'
        cursor.execute(search_query, (search_term,))
        results = cursor.fetchall()

        if len(results) == 0:
            print("No matching students found.")
        else:
            for row in results:
                print(row)

        # Close the database connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"SQLite error: {str(e)}")

#main method
create_database()
while True:
    print("\nOptions:")
    print("1. Import data from students.csv")
    print("2. Display all students")
    print("3. Add new student")
    print("4. Update student")
    print("5. Delete student")
    print("6. Search/Display students by Major, GPA, City, State, or Advisor")
    print("7. Exit")

    option = input("Select an option: ")

    if option == '1':
        import_data_from_csv()
    elif option == '2':
        display_all_students()
    elif option == '3':
        add_new_student()
    elif option == '4':
        update_student()
    elif option == '5':
        delete_student()
    elif option == '6':
        search_students()
    elif option == '7':
        print("Exiting the application.")
        break
    else:
        print("Invalid option. Please choose a valid option.")
close()
