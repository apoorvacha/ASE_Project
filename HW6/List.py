
import math, random

def any(t):
    return random.choice(t)
    
def many(t,n):
    u = []
    for i in range(1, n + 1):
        u.append(any(t))
    return u



def per(t, p):
    p = math.floor(((p or 0.5) * len(t)) + 0.5)
    return t[max(1, min(len(t), p))]

def kap(listOfCols, fun):
    u = {}
    for k, v in enumerate(listOfCols):
        v, k = fun(k, v)
        u[k or len(u)+1] = v
    return u
