from Col import COL
from Query import *

from Data import *
import Update as upd

import math
from copy import deepcopy
from Range import *
import Misc as misc
from Rule import *

def bins(cols, rowss):
    
    for _, col in enumerate(cols):
        ranges = {}
        index = 0 
        n_ranges = {}
        n_ranges_list = []
        for y, rows in rowss.items():
            for _, row in enumerate(rows):

                if (isinstance(col, COL)):
                   col = col.col
                   
                x = row[col.at]

                if x != '?':
                    k = int(bin(col, float(x) if x != "?" else x ))
                    ranges[k] = ranges[k] if k in ranges else RANGE(col.at, col.txt, float(x) if x != "?" else x)
                    upd.extend(ranges[k], float(x), y)
        ranges = {key: value for key, value in sorted(ranges.items(), key=lambda x: x[1].lo)}
        newRanges = {}
        out = []
        i = 0
        for r in ranges:
            n_ranges[index] = ranges[r]
            index = index+1

        if(hasattr(col, "isSym") and col.isSym):
            for item in n_ranges.values():
                n_ranges_list.append(item)
        out.append(n_ranges_list if hasattr(col, "isSym") and col.isSym else mergeAny(n_ranges))

    return out

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
        for j in range(1, len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo = min
        t[-1].hi = max
        return t

    ranges1, j = [], 0
    while j < len(ranges0):
        left = ranges0[j]
        if j + 1 < len(ranges0):
            right = ranges0[j+1]
        else:
            right = None
        if right:
            y = merge2(left.y, right.y)
            if y:
               j = j+1
               left.hi, left.y = right.hi, y
        ranges1.append(left)
        j = j+1

    return noGaps(ranges0) if (len(ranges1)==len(ranges0)) else mergeAny(ranges1)

def merge2(col1, col2):

    new = merge(col1, col2)

    # if div(new) <= (div(col1)*col1.n + div(col2)*col2.n)/new.n:
    return new

def merge(col1, col2):

    new = deepcopy(col1)
    if hasattr(col1, "isSym") and col1.isSym:
        for x, n in col2.has.items():
            upd.add(new, x, n)
    else:
        for n in col2.has:
            upd.add(new, n)

        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)

    return new

def xpln(data, best, rest):
    def v(has):
        return value(has, len(best.rows) , len(rest.rows), "best")
    def score(ranges):
        rule = Rule(ranges, maxSizes)

        if rule:
            Misc.oo(showRule(rule))
            bestr= selects(rule, best.rows)
            restr= selects(rule, rest.rows)
            if len(bestr)+ len(restr) >0 :
                return v({"best" : len(bestr), "rest" : len(restr)}),rule

    tmp, maxSizes = [], {}
    for _, ranges in enumerate(bins(data.cols.x,{"best":best.rows, "rest":rest.rows})):
        maxSizes[ranges[0].txt] = len(ranges)
        print("")

        for _,range in enumerate(ranges):
            print(range.txt, range.lo, range.hi)
            tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has)})
   
    rule, most = firstN(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
    return rule, most

def firstN(sortedRanges, scoreFun):
    print("")
    for r in sortedRanges:
        print(r["range"].txt, r["range"].lo, r["range"].hi, round(r["val"], 2), r["range"].y.has)
    first = sortedRanges[0]["val"]
    def useful(range):
        if range["val"] > 0.05 and range["val"] > first / 10:
            return range

    sortedRanges = list(filter(useful, sortedRanges))
    most, out = -1, None
    for n in range(len(sortedRanges)):
        
       
        tmp, rule = scoreFun([r["range"] for r in sortedRanges[:n + 1]]) or (None, None)
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
    
    return Misc.kap(rule, merges)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo = int(range['lo'])
            hi = int(range['hi'])
            at = int(range['at'])
            x = row[at]
            if x == "?":
                return True
            x = float(x)
            if lo == hi and lo == x:
                return True
            if lo <= x and x < hi:
                return True
        return False

    def conjunction(row):
        for ranges in rule.values():
            if not disjunction(ranges, row):
                return False
        return True

    return [r for r in rows if conjunction(r)]
