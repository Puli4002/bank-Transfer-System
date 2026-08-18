import random
import time
i=random.randint(1,10)
f=3
start=time.time()
while f>0:
    guess=int(input("Enter yourt Guessing number between 1 to 10:"))
    if guess==i:
        print("you win the Game")
        break
    elif guess<i:
        print("Choose Bigger number")
    elif guess>i:
        print("Choose Smaller number")

    f-=1
    print("Remaining attempts:",f)
    
if f==0:
    print("You lose the Game")
    print("Thank You")
    print("The Guess number is:",i)
end=time.time()
print("Time taken:",end-start)

