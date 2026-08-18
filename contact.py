class Contacts():
    def __init__(self,name,mobile_number):
        self.name=name
        self.mobile_number=mobile_number

def add_contact():
    try:
        name=input("Enter the Name:").strip()
        mobile_number=input("Enter the Mobile number:")
        if name.strip()==" ":
            print("Add name with out spaces")
        if len(mobile_number)==10:
            print("successfully Added") 

        contact=Contacts(name,mobile_number)
        file=open("contact.txt","a")
        file.write(f"{contact.name},{contact.mobile_number}\n")
        file.close()

    except ValueError:
        print("Enter the valid Number")

def view_contact():
    try:
        file=open("contact.txt","r")
        data=file.readlines()
        if len(data)==0:
            print("No Contact Found")
        else:
            print("-------Contact Book-------")
            for lines in data:
                contact = lines.strip().split(",")     
                print("Name          :",contact[0])
                print("Mobile Number :",contact[1])
                print("--------------------------")
        file.close()        
    except FileNotFoundError:
        print("Contact file not found")
def search_contact():
    name=input("Enter the name :")
    if name==name.strip().lower():
        return
    try:
        file = open("contact.txt", "r")
        for line in file:
            contact = line.strip().split(",")
    
            if contact[0] == name:
                print("\nContact Found")
                print("----------------------------")
                print("Name            :", contact[0])
                print("Mobile Number   :", contact[1])
                print("-----------------------------")

        print("Contact Not Found")
    except FileNotFoundError:
        print("Contact File Not Found")
def delete_contact():
    name = input("Enter the name : ")
    try:
        file = open("contact.txt", "r")
        lines = file.readlines()
        file.close()
    
        file = open("contact.txt", "w")
        for line in lines:
            contact = line.strip().split(",")
            if contact[0] == name:
                for remaining_line in lines[lines.index(line) + 1:]:
                    file.write(remaining_line)
                file.close()
                print("Contact deleted Sucessfully")
                return
    
            else:
                file.write(line)
    
            file.close()
            print("Contact Not Found")
    
    except FileNotFoundError:
        print("Contact File Not Found")
while True:
    print("---------Contact Store---------")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

    choose=int(input("Enter the Number:-"))

    if choose == 5:
        print("Thanks Using")
        break
    elif choose == 1:
        add_contact()
    elif choose == 2:
        view_contact()
    elif choose == 3:
        search_contact()
    elif choose == 4:
        delete_contact()
    else:
        print("Invalid Choose Or Choose correct option")

  

