class InvalidMarksError(Exception):
    pass
try:
    choice=int(input("enter the marks:-"))
    if 0>=choice or choice>100:
        raise InvalidMarksError
    else:
        print("Marks enter successfully")
    
except InvalidMarksError:
    print("enter valid marks")
except ValueError:
    print("Enter only Number")
else:
    print("Thank you")