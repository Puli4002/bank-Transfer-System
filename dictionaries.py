# Concession Stand Program
menu = {
    "rice ": 3.00,
    "roti": 10.00,
    "fruits": 6.00,
    "popcorn": 2.25,
    "wheat": 4.25
}

cart = []
total = 0

print("------ Menu ------")

for key, value in menu.items():
    print(f"{key}: {value}rs")

print("------------------")

while True:

    food = input("Enter the food item (Enter 'quit' to exit): ").lower()
    
    if food == "quit":
        break

    elif food in menu:
        cart.append(food)

    else:
        print("Food item not available!")

print("\nYou Ordered:")

for food in cart:
    print(food)
    total += menu[food]

print("------------------")
print(f"Total is: {total}rs")

