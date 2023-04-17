from Col import COL
from Query import *

from Data import *
import Update as upd
import copy as cp
import math
import copy
from Range import *
import Misc as misc
from Rule import *

def bins(cols, rowss):

    out = []
    
    for _, col in enumerate(cols):

            ranges = {}
            n = 0
            for y, rows in rowss.items():
                for _, row in enumerate(rows):

                    x = row.cells[col.col.at]

                    if x != '?':
                        n = n + 1
                        ranges[bin(col.col,x)] = ranges.get(bin(col.col,x), RANGE(col.col.at,col.col.txt,x))
                        upd.extend(ranges[bin(col.col,x)], x, y)

            def getVal(x):
                return x

            ranges = sorted(list(map(getVal, ranges.values())),key = lambda x: x.lo)
            if   type(col.col) == Sym:
                out.append(ranges) 
            else:
                out.append(mergeAny(ranges))

    return out

# We can change the number of bins
def bin(col, x):

    if x=="?" or hasattr(col, "isSym"):
        return x
    tmp = (col.hi - col.lo)/(16 - 1)
    
    if col.hi == col.lo:
        return 1 
    else:
        return  math.floor(x/tmp+0.5)*tmp

min = -float("inf")
max = float("inf")

def mergeAny(ranges0):

    def noGaps(t):
        if not t:
            return t
        for j in range(1,len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo  = min
        t[len(t)-1].hi =  max
        return t


    def try2Merge(left,right,j):
        y = merged(left.y, right.y)
        if y: 
            j = j+1 
            left.hi, left.y = right.hi, y 
        return j , left 
 
    ranges1,j,left = [],0, None
    while j < len(ranges0):
        left = ranges0[j]
        if j < len(ranges0)-1:
            j,left = try2Merge(left, ranges0[j+1], j)
        j=j+1
        ranges1.append(left)
    return noGaps(ranges0) if len(ranges0)==len(ranges1) else mergeAny(ranges1)


def merged(col1,col2):
    new = merge2(col1, col2)

    if div(new) <= (div(col1)*col1.n + div(col2)*col2.n)/new.n:
        return new

def merge2(col1, col2):

    new = copy.deepcopy(col1)
    if hasattr(col1, "isSym") and col1.isSym:
        for x, n in col2.has.items():
            upd.add(new, x, n)
    else:
        for n in col2.has:
            new.add(new, n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)

    return new


def xpln(data, best, rest, conf_interval):
    print('xpln called')
    def v(has):
        return value(has, len(best.rows) , len(rest.rows), "best")
    def score(ranges):
        rule = Rule(ranges, maxSizes)

        if rule:
            #Misc.oo(showRule(rule))
            bestr= selects(rule, best.rows)
            restr= selects(rule, rest.rows)
            if len(bestr)+ len(restr) >0 :
                return v({"best" : len(bestr), "rest" : len(restr)}),rule
        
        return None, None

    tmp, maxSizes = [], {}
    for _, ranges in enumerate(bins(data.cols.x,{"best":best.rows, "rest":rest.rows})):
        maxSizes[ranges[0].txt] = len(ranges)
        print("")

        for _,range in enumerate(ranges):
            print(range.txt, range.lo, range.hi)
            tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has)})
   
    rule, most = firstN(sorted(tmp, key=lambda x: x["val"], reverse=True), score, conf_interval)
    return rule, most

def firstN(sortedRanges, scoreFun, conf_interval):
    
    first = sortedRanges[0]["val"]
    def useful(range):
        if range["val"] > conf_interval and range["val"] > first / 10:
            return range

    sortedRanges = [ls for ls in sortedRanges if useful(ls)]
    most, out = -1, None

    for n in range(len(sortedRanges)):
        tmp, rule = scoreFun([r["range"] for r in sortedRanges[:n + 1]])
        if tmp and tmp > most:
            out, most = rule, tmp
    
    return out, most

def showRule(rule):

    def pretty(range):
        return range["lo"] if range["lo"] == range["hi"] else [range["lo"], range["hi"]]

    def merges(attr, ranges):
        # print("iterable",misc.map(merge(sorted(ranges, key=lambda r: r['lo'])),pretty)))
        return list(map(pretty,merge(sorted(ranges, key=lambda r: r['lo'])))), attr

    def merge(t0):
        t, j = [], 0
        while j < len(t0):
            left, right = (t0[j], t0[j+1]) if j+1 < len(t0) else (t0[j], None)
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j += 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j += 1
        
        return t if len(t0) == len(t) else merge(t)
    
    if not rule:
        return
    return Misc.kap(rule, merges)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo = range['lo']
            hi = range['hi']  
            at = range['at']
            x = row.cells[at]
            if x == '?' or (lo == hi and lo == x) or (lo <= x and x< hi):
                return True
        return False
    
    def conjunction(row):
        for ranges in rule.values():
            if not disjunction(ranges, row):
                return False
        return True

    return [r for r in rows if conjunction(r)] if rule else rows
