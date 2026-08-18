print("Fibonacci Series")
def num():
    n=int(input(" enter the positive number:"))
    n1,n2=0,1
    count=0
    if n<=0:
        print("please enter positive number and Greater than Zero")
    else:
        while count<=n:
           print(n1, end=" ")
           n1,n2=n2,n1+n2
           count+=1
num()
        
        

