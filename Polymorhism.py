class Animal:
    def sound(self):
        pass
class Dog(Animal):
    def sound(self):
        print("Bark")

class Cat(Animal):
    def sound(self):
        print("Meow")
class Horse(Animal):
    def sound(self):
        print("Horse Horse")

d=Dog()
c=Cat()
h=Horse()
d.sound()
c.sound()
h.sound()