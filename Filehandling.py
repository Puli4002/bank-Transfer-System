with open("num.txt","r") as file:
    print(file.read())
delete_line = int(input("Enter the line number to delete: "))
with open("num.txt", "r") as file:
    lines = file.readlines()

with open("num.txt", "w") as file:
    for index, line in enumerate(lines, start=1):
        if index != delete_line:
            file.write(line)

print("deleted successfully.")