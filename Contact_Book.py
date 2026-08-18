import json

class ContactValidationError(Exception):
    pass

class DuplicateContactError(Exception):
    pass

def read_contacts():
    try:
        file = open("contacts.json", "r")
        try:
            contacts = json.load(file)
        except json.JSONDecodeError:
            contacts = []
        file.close()
        return contacts

    except FileNotFoundError:
        return []
def write_contacts(contacts):
    file = open("contacts.json", "w")
    json.dump(contacts, file, indent=4)
    file.close()
def validate_contact(name, phone):
    if name.strip() == "":
        raise ContactValidationError("Name cannot be blank.")
    if len(phone) != 10 or not phone.isdigit():
        raise ContactValidationError("Phone number must be exactly 10 digits.")
def add_contact(name, phone):
    validate_contact(name, phone)
    contacts = read_contacts()
    for contact in contacts:
        if (contact["phone"] == phone) or (contact["name"] == name):
            raise DuplicateContactError("Contact already exists.")
    new_contact = {
        "name": name,
        "phone": phone
    }
    contacts.append(new_contact)
    write_contacts(contacts)

while True:
    print("\n------ Contact Book ------")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Exit")
    choice = input("Enter your choice : ")
    if choice == "1":
        name = input("Enter Name : ")
        phone = input("Enter Phone Number : ")
        try:
            add_contact(name, phone)
            print("Contact Added Successfully.")
        except ContactValidationError:
            print("ContactValidationError")
        except DuplicateContactError:
            print("DuplicateContactError")
    elif choice == "2":
        contacts = read_contacts()
        if len(contacts) == 0:
            print("No Contacts Found.")
        else:
            print("\n------ Contacts ------")
            for contact in contacts:
                print("Name :", contact["name"])
                print("Phone:", contact["phone"])
                print("----------------------")
    elif choice == "3":
        print("Thank You")
        break
    else:
        print("Invalid Choice")