class Student:
    def __init__(self, name, roll_no, age, maths_marks, python_marks):
        self.name = name
        self.roll_no = roll_no
        self.age = age
        self.maths_marks = maths_marks
        self.python_marks = python_marks


def add_student():
    try:
        name = input("Enter Name : ")
        roll = input("Enter Roll Number : ")
        age = int(input("Enter Age : "))
        maths_marks = int(input("Enter Maths Marks : "))
        python_marks = int(input("Enter Python Marks : "))

        if age <= 0:
            print("Age should be greater than 0")
            return

        if maths_marks < 0 or maths_marks > 100:
            print("Maths Marks should be between 0 and 100")
            return

        if python_marks < 0 or python_marks > 100:
            print("Python Marks should be between 0 and 100")
            return

        student = Student(name, roll, age, maths_marks, python_marks)

        file = open("data.txt", "a")
        file.write(f"{student.roll_no},{student.name},{student.age},{student.maths_marks},{student.python_marks}\n")
        file.close()

        print("Student Added Successfully")

    except ValueError:
        print("Please enter valid numbers.")


def view_students():
    try:
        file = open("data.txt", "r")
        data = file.readlines()

        if len(data) == 0:
            print("No Student Records")
        else:
            for line in data:
                student = line.strip().split(",")

                print("----------------------------")
                print("Roll No      :", student[0])
                print("Name         :", student[1])
                print("Age          :", student[2])
                print("Maths Marks  :", student[3])
                print("Python Marks :", student[4])

        file.close()

    except FileNotFoundError:
        print("Student File Not Found")


def search_student():
    roll = input("Enter Roll Number : ")
    try:
        file = open("data.txt", "r")

        for line in file:
            student = line.strip().split(",")

            if student[0] == roll:
                print("\nStudent Found")
                print("----------------------------")
                print("Roll No      :", student[0])
                print("Name         :", student[1])
                print("Age          :", student[2])
                print("Maths Marks  :", student[3])
                print("Python Marks :", student[4])
                file.close()
                return

        file.close()
        print("Student Not Found")

    except FileNotFoundError:
        print("Student File Not Found")


def update_student():
    roll = input("Enter Roll Number : ")
    try:
        file = open("data.txt", "r")
        lines = file.readlines()
        file.close()

        file = open("data.txt", "w")

        for line in lines:
            student = line.strip().split(",")

            if student[0] == roll:
                name = input("Enter New Name : ")
                age = int(input("Enter New Age : "))
                maths_marks = int(input("Enter New Maths Marks : "))
                python_marks = int(input("Enter New Python Marks : "))

                new_student = Student(name, roll, age, maths_marks, python_marks)

                file.write(f"{new_student.roll_no},{new_student.name},{new_student.age},{new_student.maths_marks},{new_student.python_marks}\n")

                for remaining_line in lines[lines.index(line) + 1:]:
                    file.write(remaining_line)

                file.close()
                print("Student Updated Successfully")
                return

            else:
                file.write(line)

        file.close()
        print("Student Not Found")

    except ValueError:
        print("Invalid Input")

    except FileNotFoundError:
        print("Student File Not Found")


def delete_student():
    roll = input("Enter Roll Number : ")
    try:
        file = open("data.txt", "r")
        lines = file.readlines()
        file.close()

        file = open("data.txt", "w")

        for line in lines:
            student = line.strip().split(",")

            if student[0] == roll:

                for remaining_line in lines[lines.index(line) + 1:]:
                    file.write(remaining_line)

                file.close()
                print("Student Deleted Successfully")
                return

            else:
                file.write(line)

        file.close()
        print("Student Not Found")

    except FileNotFoundError:
        print("Student File Not Found")


while True:
    print("\n========== Student Management System ==========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choose = input("Enter Your Choice : ")

    if choose == "1":
        add_student()
    elif choose == "2":
        view_students()
    elif choose == "3":
        search_student()
    elif choose == "4":
        update_student()
    elif choose == "5":
        delete_student()
    elif choose == "6":
        print("Thank You...")
        break
    else:
        print("Invalid Choice")