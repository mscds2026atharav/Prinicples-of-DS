a1=[2,3,4,5,6,7,9]
b1=[7,8,5,3,7,1,0]

a2=[[1,3,5],[2,4,5]]
b2=[[2,4,6],[1,3,5]]
b3=[[2,4],[6,1],[3,5]]

def addition1D(x,y):
    c=[0]*len(x)
    for i in range(0,len(x)):
        c[i] = x[i] + y[i]
    return c

def subtraction1D(x,y):
    d=[0]*len(x)
    for i in range(0,len(x)):
        d[i] = x[i] - y[i]
        return d

def multiply1D(x,y):
    e=[0]*len(x)
    for i in range(0,len(x)):
        e[i] = x[i] * y[i]
    return e

def addition2D(x,y):
    c=[[0]*len(a2[0]) for _ in range(len(a2))]
    for m in range(0,len(a2)):
        for n in range(0,len(a2[0])):
            c[m][n] = x[m][n] + y[m][n]
    return c

def subtraction2D(x,y):
    d=[[0]*len(a2[0]) for _ in range(len(a2))]
    for m in range(0,len(a2)):
        for n in range(0,len(a2[0])):
            d[m][n] = x[m][n] - y[m][n]
    return d

def multiply2D(x,y):
    e=[[0]*len(y[0]) for _ in range(len(x))]
    for i in range(len(x)):
        for j in range(len(y[0])):
            for k in range(len(y)):
                e[i][j] += x[i][k] * y[k][j]
    return e

print("c1:",addition1D(a1,b1))
print("d1:",subtraction1D(a1,b1))
print("e1:",multiply1D(a1,b1))

print("c2:",addition2D(a2,b2))
print("d2:",subtraction2D(a2,b2))
print("e2:",multiply2D(a2,b3))