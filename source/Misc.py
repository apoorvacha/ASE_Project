import math, json
import re, copy
from Start import the
from Num import Num
import random
# from Data import *

def show(node, what, cols, nPlaces, lvl=None):
    if node:
        lvl = lvl or 0
        print("| " * lvl, str(len(node["data"].rows)), " ")
        if not node.get("left", None) or lvl == 0:
            print(o(node["data"].stats("mid", node["data"].cols.y, nPlaces)))
        else:
            print("")
        show(node.get("left", None), what, cols, nPlaces, lvl+1)
        show(node.get("right", None), what, cols, nPlaces, lvl+1)


def rint(lo, hi):
    return math.floor(0.5 + rand(lo, hi))

# def any(t):
#     return t[rint(len(t))]

# def many(t,n):
#     u = {}
#     for i in range(1,n):
#         u[1+len(u)] = any(t)
#     return u
# many = function(t,n,    u) u={}; for i=1,n do push(u, any(t)) end; return u end 

def rand(lo=0, hi=1):
    lo, hi = lo or 0, hi or 1
    Seed = (16807 * the["seed"]) % 2147483647
    return lo + (hi-lo) * Seed / 2147483647

def cosine(a, b, c):
    x1 = (a**2 + c**2 - b**2) / (2*c)
    x2 = max(0, min(1, x1))
    y  = (a**2 - x2**2)**.5
    return x2, y


def sort(t):
    #Doubt
    return t

def lt(x):
    def fun(a, b):
        return a[x] < b[x]

def keys(t):
    #Doubt
    pass

def push(t, x):
    t.append(x)

def any(t):
    return t[rint(0, len(t) - 1)]

def many(t, n):
    u = []
    for i in range(n):
        u.append(any(t))
    return u

# String Functions

def coerce(s): #Doubt
    if s == "true":
        return True
    elif s == "false":
        return False
    elif re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$", s) is not None:
        return float(s)
    else:
        return s

def rnd(n, nPlaces=3):
    mult = 10**(nPlaces or 3)
    return math.floor(n * mult + 0.5) / mult 


def map(t,fun):
    u = {}
    if isinstance(t, list):
        items = enumerate(t)
    else:
        items = t.items()
    # myDict = t.copy() ;
    for k, v in items:
    # for k,v in enumerate(t.values()):
        v,k = fun(v)
        u[k or (1+len(u))] = v
    return u

def kap(t, fun):
    u = {}
   
    if isinstance(t, list):
        items = enumerate(t)
    else:
        items = t.items()
    # myDict = t.copy() ;
    for k, v in items:
            v, k = fun(k, v)
            u[k or len(u)+1] = v
    return u

def oo(t):
    print(o(t))
    return t

def o(t, isKeys=None):
    return str(t)
# Main

# def settings(s, t):
#     return dict(re.findall(r"\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s))

# def transpose(t):
#     u = []
#     for i in range(len(t[0])):
#         row = []
#         for j in range(len(t)):
#             row.append(t[j][i])
#         u.append(row)
#     return u


def delta(i, other):
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / (math.sqrt(e + y.sd ** 2 / y.n + z.sd ** 2 / z.n))

def samples(t, n = None):
    u = []
    for i in range(n or len(t)):
        u.append(random.choice(t))
    return u

def bootstrap(y0, z0):
    x, y, z, yhat, zhat = Num(), Num(), Num(), [], []
    for y1 in y0:
        x.add(y1)
        y.add(y1)
    for z1 in z0:
        x.add(z1)
        z.add(z1)
    xmu, ymu, zmu = x.mu, y.mu, z.mu
    for y1 in y0: yhat.append(y1 - ymu + xmu)
    for z1 in z0: zhat.append(z1 - zmu + xmu)
    tobs = delta(y, z)
    n = 0
    for i in range(512):
        p = Num(samples(yhat))
        if (delta(Num(t=samples(yhat)), Num(t=samples(zhat))) > tobs):
            n += 1
    return n / 512 >= 0.05

def cliffs_delta(ns1, ns2):

    if len(ns1) > 256:
        ns1 = many(ns1, 256)
    if len(ns2) > 256:
        ns2 = many(ns2, 256)
    if len(ns1) > 10 * len(ns2):
        ns1 = many(ns1, 10 * len(ns2))
    if len(ns2) > 10 * len(ns1):
        ns2 = many(ns2, 10 * len(ns1))

    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n += 1
            if x > y:
                gt += 1
            if x < y:
                lt += 1

    return abs(lt - gt) / n > 0.147

def diffs(nums1, nums2):
    def kap(nums, fn):
        return [fn(k, v) for k, v in enumerate(nums)]
    return kap(nums1, lambda k, nums: (cliffs_delta(nums.col.has, nums2[k].col.has), nums.col.txt))

def merge(rx1, rx2):
    rx3 = RX([], rx1["name"])
    for t in (rx1["has"], rx2["has"]):
        for x in t:
            rx3["has"].append(x)
    rx3["has"].sort()
    rx3["n"] = len(rx3["has"])
    return rx3

def RX(t, s = None):
    t.sort()
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t}

def mid(t):
    t = t["has"] if "has" in t else t
    n = len(t) // 2
    return len(t) % 2 == 0 and (t[n] + t[n + 1]) / 2 or t[n + 1]

def div(t):
    t = t["has"] if "has" in t else t
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56

def scottKnot(rxs):
    def merges(i, j):
        out = RX([], rxs[i]["name"])
        for _ in range(i, j+1):
            out = merge(out, rxs[j])
        return out
    
    def same(lo, cut, hi):
        l, r = merges(lo, cut), merges(cut+1, hi)
        return cliffs_delta(l['has'], r['has']) and bootstrap(l['has'], r['has'])
    
    def recurse(lo, hi, rank):
        cut, b4, best = None, merges(lo, hi), 0
        for j in range(lo, hi+1):
            if j < hi:
                l, r = merges(lo, j), merges(j+1, hi)
                now = (l["n"] * (mid(l) - mid(b4)) ** 2 + r["n"] * (mid(r) - mid(b4)) ** 2) / (l["n"] + r["n"])
                if now > best:
                    if abs(mid(l) - mid(r)) >= cohen:
                        cut, best = j, now
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank  = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi + 1):
                rxs[i]["rank"] = rank
        return rank
    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(0, len(rxs) - 1)) * the['cohen']
    recurse(0, len(rxs) - 1, 1)
    return rxs

def tiles(rxs):
    huge, min_f, max_f, floor = float("inf"), min, max, math.floor
    lo, hi = huge, -huge
    for rx in rxs:
        lo = min_f(lo, rx["has"][0])
        hi = max_f(hi, rx["has"][-1])
    for rx in rxs:
        t, u = rx["has"], []
        def of(x, most): 
            return max(1, min_f(most, x))
        def at(x): 
            return t[of(int(len(t) * x), len(t) - 1)]
        def pos(x): 
            return floor(of(the['width'] * (x - lo) / (hi - lo + 1E-32) // 1, the['width']))
        
        for _ in range(the['width']): 
            u.append(" ")
        a, b, c, d, e= at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E= pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B):
            u[i] = "-"
        for i in range(D, E):
            u[i] = "-"
            
        u[the['width'] // 2] = "|"
        u[C] = "*"
        rx["show"] = "".join(u) + " { %6.2f" % a
        for x in (b, c, d, e):
            rx["show"] += ", %6.2f" % x
        rx["show"] += " }"
    return rxs
