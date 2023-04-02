import Query , List
from Start import the
from Data import Data
import Misc

def half(data, rows= None, cols = None ,above = None):
    
    left =[]
    right =[]
    def gap(r1,r2):
        return Query.dist(data, r1, r2, cols) 
    def cos(a,b,c):
        return (a**2 + c**2 - b**2)/(2*c) 
    def proj(r) :
        return {"row":r, "x":cos(gap(r,A), gap(r,B),c)}
    
    rows =  rows or data.rows
    some = List.many(rows,512)
    A    = above or List.any(some)
    tmp = sorted([{"row": r, "d": gap(r, A)} for r in some], key=lambda x: x["d"])
    far = tmp[int(len(tmp)*0.95)//1 ]
    B,c = far["row"], far["d"]
    # evals = 1 if (hasattr(util.args, "Reuse") and above) else 2
    for n, two in enumerate(sorted(map(proj, rows), key=lambda x: x["x"])):
            if n <= (len(rows)) / 2:
                left.append(two["row"])
            else:
                right.append(two["row"])
    return left, right, A, B, c, 1


def tree(data, rows=None, cols=None, above=None):
    rows = rows or data.rows
    here = {"data": data.clone(data, rows)}
    if len(rows) >= 2 * (len(data.rows) ** 0.5):
        left, right, A, B, _, evals = half(data, rows, cols, above)
        here["left"] = tree(data, left, cols, A)
        here["right"] = tree(data, right, cols, B)
    return here

def show_tree(tree, lvl=0, post=None):
    if tree:
        print("{}[{}]".format("|.. " * lvl, len(tree["data"].rows)), end="")
        if lvl == 0 or ("left" not in tree):
            print(Misc.o(Query.stats(tree["data"])))
        else:
            print("")
        show_tree(tree["left"] if "left" in tree else None, lvl + 1)
        show_tree(tree["right"] if "right" in tree else None, lvl + 1)