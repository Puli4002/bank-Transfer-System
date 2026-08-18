class BoardVersionConflictError(Exception):
    pass
class TaskValidationError(Exception):
    pass
class TeamBoardClient:
    def __init__(self):
        self.tasks:list[dict]= []
        self.version :int= 0
    def get_tasks(self) -> tuple[list[dict],int]:
        return list(self.tasks), self.version
    def add_task(self, *, title, assign, expected_version):
        if expected_version != self.version:
            raise BoardVersionConflictError(f"Board version conflict. Expected{expected_version}, But the current version is {self.version}")
        task = {
            "Title": title,
            "Assign": assign
        }
        self.tasks.append(task)
        self.version += 1
        return self.version
def validate_task(title, assign):
    if title.strip() == "":
        raise TaskValidationError("Title cannot be empty.")
    if len(title) > 100:
        raise TaskValidationError("Title must be less than 100 characters.")
    if assign.strip() == "":
        raise TaskValidationError("Assignment cannot be empty.")
def sync_task_to_board(title, assign, board_client=None):
    validate_task(title, assign)
    if board_client is None:
        board_client = TeamBoardClient()
    tasks, version = board_client.get_tasks()
    try:
        new_version = board_client.add_task(
            title=title,
            assign=assign,
            expected_version=version
        )
    except BoardVersionConflictError:
        tasks, version =  board_client.get_tasks()
        new_version = board_client.add_task(
            title=title,
            assign=assign,
            expected_version=version
        )
    return{
        "Title":title,
        "Assign":assign,
        "success":True,
        "New_Version":new_version
    }

board = TeamBoardClient() 
check=0
while True:
    print("\n------Task Board------")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Exit")
    
    choose= int(input("Enter the number: "))

    if choose == 1:
        if check == 5:
            print("You have reached the limit for adding tasks.")
            continue
        title = input("Enter Task Title: ")
        assign = input("Enter Whom to Assign: ")
        
        try:
            result =sync_task_to_board(
                title,
                assign,
                board
                )
            print("Task Added Successfully")
            print(result)
        except TaskValidationError:
            print("Title / Assign can't be empty And Title must be less than 100 charaters.")
        check +=1     
    elif choose == 2:
        tasks, version = board.get_tasks()
        print("\n------Tasks------")
        for task in tasks:
            print("Title       :", task["Title"])
            print("Assign      :", task["Assign"])
            print("Verson      :",version)
            print("-----------------------")
    elif choose == 3:
        print("Thank you for Using Task board.")
        break
    else:
        print("Choose a Valid Option.")


