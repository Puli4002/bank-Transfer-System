class Student:

    def __init__(self, name):
        self.name = name
        self.__marks = 0

    def set_marks(self, marks):
        self.__marks = marks

    def get_marks(self):
        print("Name:", self.name)
        print("Marks:", self.__marks)

s = Student("Sai")
s.self__marks=0 # we can't access the value out side the class 
s.set_marks(47)
s.get_marks()