# -- ## Query
import math, Sym
from List import *


def has(col):
    if (not hasattr(col, "isSym") and not col.ok):
        
        if isinstance(col.has, dict):
            temp = sorted(col.has.items(), key = lambda item: item[1])
            col.has = dict(temp)

    col.ok = True
    return col.has



def mid(col):
    
    if hasattr(col, "isSym") :
        return col.mode 
    else :
        return per(has(col), 0.5)


def div(col):
    if hasattr(col, "isSym"):
        e = 0

        for n in col.has.values():
            e = e - n/col.n * math.log(n/col.n, 2)
    
    else:
        return (per(has(col),.9) - per(has(col), .1)) / 2.58


def stats(data, fun = "mid", cols = None, nPlaces = 1):
    cols = cols or data.cols.y
    def callBack_function(k, col):
        col = col.col
        return round(getattr(col, fun)(), nPlaces), col.txt
    parameter = callBack_function
    tmp = kap(cols, parameter)

    tmp["N"] = len(data.rows)

    return tmp


def norm(num, n):
    max = float('inf')
    
    try:
        if(n == '?'):
            return n     
        else: 
            return (float(n)-num.lo) / (num.hi - num.lo + 1 / max)

    except:
        return 0


def dist(data, row1, row2, cols=None):
    n, d = 0, 0

    def dist1(col, x, y):
        if x == "?" and y == "?":
            return 1
        if hasattr(col, "isSym"):
            if x==y :
                return 0
            else:
                return 1
        else:
            x, y = norm(col, x), norm(col, y)
            
            if x == "?":
                if y<0.5:
                 x =1
                else:
                    x = 0
                    
            if y == "?":
                if x<0.5 :
                    y=1
                else:
                    y = 0
        
        return abs(x - y)
    
    for _, col in enumerate(cols or data.cols.x):
        n = n + 1
        val = dist1(col.col,row1.cells[col.col.at], row2.cells[col.col.at])
        d = d + val ** 2
    return (d / n) ** (1 / 2)



def value(has, nB = 1, nR = 1, sGoal = True, b =0 , r =0):
    b, r = 0, 0
    max = float('inf')
    min = -float('inf')
    # for x, n in enumerate(has):
    for x, n in has.items():
        if x == sGoal:
            b = b + n
        else:
            r = r + n
    b,r = b/(nB+1/max), r/(nR+1/max)
    return (b ** 2) / (b + r)

# -- A query that returns true if `row1` is better than another.
# -- This is Zitzler's indicator predicate that
# -- judges the domination status 
# -- of pair of individuals by running a “what-if” query. 
# -- It checks what we lose if we (a) jump from one 
# -- individual to another (see `s1`), or if we (b) jump the other way (see `s2`).
# -- The jump that losses least indicates which is the best row.


def better(data,row1,row2, s1 =0, s2 =0):
    ys,x,y = data.cols.y, None, None

    for _,col in enumerate(ys) :
        x = norm(col.col, row1.cells[col.col.at])
        y = norm(col.col, row2.cells[col.col.at])
        # print("txt in btter",col.col.txt)
        s1 = s1 - math.exp(col.col.w * (x - y) / len(ys))
        s2 = s2 - math.exp(col.col.w * (y - x) / len(ys))
    return s1/len(ys) < s2/len(ys) 

def betters(data, n=None):
    def quicksort(arr, cmp_func):
        if len(arr) <= 1:
            return arr

        pivot = arr[0]
        left = []
        right = []

        for item in arr[1:]:
            if cmp_func(data, item, pivot):
                left.append(item)
            else:
                right.append(item)

        return quicksort(left, cmp_func) + [pivot] + quicksort(right, cmp_func)

    tmp = quicksort(data.rows, better)
    return tmp[:n], tmp[n:] if n else tmp