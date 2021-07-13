n  = int(input())
x = "AEIOUaeiou"

while(n>0):
    n1=int(input())
    s = input()
    j=len(s)
    a=0
    y=0
    l=[]

    while (j>n1):
        print(j)
        print(n1)
        if (s[j] in x):
            x = x+1
            l.append
            y = 0

        else:
            y=y+1
            l.append(x)
            y=0
        j=j-1
    
    l1=len(l)
    print(l1)
    print(l)
    k=0
    item=l[k]

    while (k<l1-1):

        m=l[k+1]
        m=int[m]
        if m>item:
            item=m
        k=k+1
        print(item)
    n=n-1