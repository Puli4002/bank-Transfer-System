class Task:
    def __init__(self, task_name):
        self.task_name = task_name
        self.status = "Pending"
def add_task():
    try:
        task_name = input("Enter Task : ")
        task = Task(task_name)
        file = open("tasks.txt", "a")
        file.write(task.task_name + "," + task.status + "\n")
        file.close()

        print("Task Added Successfully")

    except Exception:
        print("Something Went Wrong")

def view_tasks():
    try:
        file = open("tasks.txt", "r")
        data = file.readlines()
        if len(data) == 0:
            print("No Tasks Available")
        else:
            print("\n------ Task List ------")
            number = 1
            for line in data:
                task = line.strip().split(",")
                print(number, ".", task[0], "-", task[1])
                number += 1
        file.close()

    except FileNotFoundError:
        print("No Task File Found")
    
def search_task():
    try:
        task_name = input("Enter Task Name : ")
        file = open("tasks.txt", "r")
        for line in file:
            task = line.strip().split(",")
            if task[0].lower() == task_name.lower():
                print("\nTask Found")
                print("Task :", task[0])
                print("Status :", task[1])

                file.close()
                return
        file.close()
        print("Task Not Found")

    except FileNotFoundError:
        print("No Task File Found")

def update_task():
    try:
        task_name = input("Enter Task Name : ")
        file = open("tasks.txt", "r")
        data = file.readlines()
        file.close()
        file = open("tasks.txt", "w")
        updated = 0
        for line in data:
            task = line.strip().split(",")
            if task[0].lower() == task_name.lower():
                print("1. Pending")
                print("2. Completed")
                choice = input("Enter Choice : ")
                if choice == "1":
                    status = "Pending"
                elif choice == "2":
                    status = "Completed"
                else:
                    status = task[1]
                file.write(task[0] + "," + status + "\n")
                updated = 1
            else:
                file.write(line)
        file.close()
        if updated == 1:
            print("Task Updated Successfully")
        else:
            print("Task Not Found")
    except FileNotFoundError:
        print("No Task File Found")

def delete_task():
    try:
        task_name = input("Enter Task Name : ")
        file = open("tasks.txt", "r")
        data = file.readlines()
        file.close()
        file = open("tasks.txt", "w")
        deleted = 0
        for line in data:
            task = line.strip().split(",")
            if task[0].lower() == task_name.lower():
                deleted = 1
            else:
                file.write(line)

        file.close()
        if deleted == 1:
            print("Task Deleted Successfully")
        else:
            print("Task Not Found")

    except FileNotFoundError:
        print("No Task File Found")


while True:
    print("\n========== TO DO LIST ==========")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Search Task")
    print("4. Update Task")
    print("5. Delete Task")
    print("6. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_tasks()
    elif choice == "3":
        search_task()
    elif choice == "4":
        update_task()
    elif choice == "5":
        delete_task()
    elif choice == "6":
        print("Thank You")
        break
    else:
        print("Invalid Choice")

        