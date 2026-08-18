order=[]
menu={
      "Chicken Dum Biriyani" : 300,
      "Samosa" : 20,
      "Butter Chicken" : 400,
      "paneer Butter Masala" : 350,
      "paneer rice": 150}
while True:
    print("------Food Ordering System------")
    print("1. Display Items")
    print("2. Order Food")
    print("3. Display Order")
    print("4. Display Bill")
    print("5. Exit")

    choice =int(input("Choose the Option from Above:"))


    if choice == 5:
        print("Thank You And Visit Again")
        break
    elif choice == 1:
        print("----Menu for Food----")
        print("1.Chicken Dum Biriyani : 300rs")
        print("2.Samosa : 20rs")
        print("3.Butter Chicken : 400rs")
        print("4.paneer Butter Masala : 350rs")
        print("5. paneer rice: 150rs")
    elif choice == 2:
        food=input("Choose the Food Items:")
        if food in menu:
            order.append(food)
            print("Successfully Add your order")
        else:
            print("item not found in menu")
    elif choice == 3: 
        print("Displaying your Order")
        for food in order:
            print(food)
    elif choice == 4:
        print("----Bill For What you Ordered----")
        total=0
        for food in order:
            total += menu[food]
            print(f"{food}-- {menu[food]}rs")
        print(f"Total Bill:-{total}rs")
    else:
        print("Invalid Choice")

        

