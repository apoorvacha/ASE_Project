from Num import Num
from Sym import Sym
from Start import the
import Query
from Data import *
import Misc,math
from pathlib import Path
import os , csv
import Update
import io,re
import Cluster, Discretization
import Optimize as optimize

def test_nums(src):
    val = Num()
    val1 = Num()
    for i in range(1000):
        val.add(Misc.rand())
    for i in range(1000):
        val1.add(Misc.rand()**2)
    print("\nTest num : successful \n")
    print(1,Misc.rnd(val.mid()), Misc.rnd(val.div()))
    print(2,Misc.rnd(val1.mid()), Misc.rnd(val1.div())) 
    return .578 == Misc.rnd(val.mid()) and val.mid()> val1.mid() 


def test_sym(src):
    value = ['a', 'a', 'a', 'a', 'b', 'b', 'c']
    sym1 = Sym()
    for x in value:
        sym1.add(x)
    if("a"==sym1.mid() and 1.379 == Misc.rnd(sym1.div())):
        print("\nTest sym : successful \n")
    return "a"==sym1.mid() and 1.379 == Misc.rnd(sym1.div())

# def readCSV(sFilename, fun):
  
#     with open(sFilename, mode='r') as file:
#         csvFile = csv.reader(file)
#         for line in csvFile:
#             fun(line)

def coerce(v):
    types = [int, float]

    for t in types:
        try:
            return t(v)
        except ValueError:
            pass

    bool_vals = ["true", "false"]
    if v.lower() in bool_vals:
        return v.lower() == "true"

    return v

def readCSV(sFilename, fun):

    f = io.open(sFilename)
    while True:
        s = f.readline().rstrip()
        if s:
            t = []
            for s1 in re.findall("([^,]+)", s):
                t.append(coerce(s1))
            fun(t)
        else:
            return f.close()

def test_csv(src):

    global n
    def fun(t):
        n += len(t)
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    if(csv_content(csv_path) == 8 * 399):
        print("\n Test csv : successful \n")
    print(src)
    return csv_content(csv_path) == 8 * 399

def csv_content(src):
    with open(src, mode='r') as file:
        csvFile = csv.reader(file)
        l =0
        for row in csvFile:
            l += len(row)
        return l


def test_data(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    data = Data(csv_path)

    # data = data1.read_file(csv_path)
    col = data.cols.x[1].col
    print("\nTest data : successful \n")
    print(col.lo,col.hi, Query.mid(col), Query.div(col))
    print(Query.stats(data))
    return True



def test_clone(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    data = Data(csv_path)
    # data1 = data.read_file(csv_path)
   
    data2 = Data(data, data.rows)
    # data2 = data.clone(data,data.rows)
    print("\nTest clone : successful \n")
    Misc.oo(Query.stats(data))
    Misc.oo(Query.stats(data2))
    return True

def test_the(src):
    print("\nTest the : successful \n")
    print(str(the))
    return True

def test_half(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)

    data = Data(csv_path)
    # data = data1.read_file(csv_path)

    left, right, A, B, c , evals= Cluster.half(data)
    print("\nTest half : successful \n")
    print(len(left), len(right), len(data.rows))
    print(Misc.o(A), c)
    print(Misc.o(B))
    return True
  
    

def test_cliffs(src):
    if Misc.cliffs_delta([8, 7, 6, 2, 5, 8, 7, 3], [8, 7, 6, 2, 5, 8, 7, 3]):
        return False
    if not Misc.cliffs_delta([8, 7, 6, 2, 5, 8, 7, 3], [9, 9, 7, 8, 10, 9, 6]):
        return False

    t1, t2 = [], []
    for i in range(1000):
        t1.append(Misc.rand())
        t2.append(math.sqrt(Misc.rand()))
    if Misc.cliffs_delta(t1, t1):
        return False
    if not Misc.cliffs_delta(t1, t2):
        return False
    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x * j,t1))
        diff = Misc.cliffs_delta(t1, t3)
        print(">", Misc.rnd(j), diff)
        j *= 1.025
    print("\nTest cliff : successful \n")
    return True

def test_dist(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    data = Data(csv_path)

    # data = data1.read_file(csv_path)
    num = Num()
    for row in data.rows:
        Update.add(num, Query.dist(data, row, data.rows[1]))
    print("\nTest dist : successful \n")
    print({"lo": num.lo, "hi": num.hi, "mid": Misc.rnd(Query.mid(num)), "div": Misc.rnd(num.n)})
    return True

def test_tree(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    data = Data(csv_path)

    # data = data1.read_file(csv_path)
    print("\nTest tree : successful \n")
    Cluster.show_tree(Cluster.tree(data))

    return True


def test_sway(src):
  
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    data = Data(csv_path)
    # print(len(data.rows))
    # print(len(data.cols.all),len(data.cols.x),len(data.cols.y))

    # data = data1.read_file(csv_path)
    best, rest, evals = optimize.sway(data)
    print(Misc.o(Query.stats(data)))
    print("\nall ", Misc.o(Query.stats(data)))
    print("    ",  Misc.o( Query.stats(data, "div")))
    print("\nbest", Misc.o(Query.stats(best)))
    print("    ",   Misc.o(Query.stats(best, "div")))
    print("\nrest", Misc.o(Query.stats(rest)))
    print("    ",   Misc.o(Query.stats(rest, "div")))
    # print("\nall ~= best?", Misc.o(Misc.diffs(best.cols.y, data.cols.y)))
    # print("best ~= rest?", Misc.o(Misc.diffs(best.cols.y, rest.cols.y)))

    print("\nTest sway : successful \n")
    return True



def test_bins(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    data= Data(csv_path)

    # data = data1.read_file(csv_path)
    best, rest , evals= optimize.sway(data)
    print("all","","","",Misc.o({"best":len(best.rows), "rest": len(rest.rows)}))
    for k,t in enumerate(Discretization.bins(data.cols.x, {"best": best.rows, "rest": rest.rows})):
        for _, range in enumerate(t):
            print(range.txt, range.lo, range.hi,round(Query.value(range.y.has, len(best.rows), len(rest.rows), "best")),
                  range.y.has)
    
    print("\nTest bin : successful \n")
    return  True 

def test_explain(src):
    root = str(Path(__file__).parent.parent)
    csv_path = os.path.join(root, src)
    # data = Data1.Data1(csv_path)
    data = Data(csv_path)
    best, rest , evals = optimize.sway(data)

    rule, most= Discretization.xpln(data,best,rest)
    print("\n-----------\n\nexplain=", Discretization.showRule(rule))
   
    data1= Data(data,Discretization.selects(rule,data.rows))
    print("all               ",Query.stats(data),Query.stats(data,'div'))
    print(f"sway with {evals} evals",Query.stats(best),Query.stats(best,'div'))
    print(f"xpln on {evals} evals",Query.stats(data1),Query.stats(data1,'div'))
    top, _ = Query.betters(data, len(best.rows))
    top = Data(data, top)
    print(f"sort with {len(data.rows)} evals", Query.stats(top), Query.stats(top, 'div'))
    print("\nTest explain : successful \n")
    return True

