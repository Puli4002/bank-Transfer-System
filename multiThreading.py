import threading
import time

def move():
    time.sleep(8)
    print("I am moving to office")
def act():
    time.sleep(2)
    print("I have interest in acting")
def bike():
    time.sleep(5)
    print("I have my dream bike to buy")
def car():
    time.sleep(18)
    print("car can reach in 18mins because of traffic")
def horse():
    time.sleep(9)
    print("the horse can run fast than dog")


head=threading.Thread(target=move)
head.start()
head1=threading.Thread(target=act)
head1.start()
head2=threading.Thread(target=bike)
head2.start()
head.join()
head1.join()
head2.join()

