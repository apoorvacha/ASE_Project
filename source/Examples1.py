import Query
from Data import *
import Misc
import csv
import Discretization
import Optimize as optimize
from Query import *
from tabulate import tabulate
from Start import the
from Misc import *
from collections import defaultdict

count = 0

def readCSV(src, fun):
    with open(src, mode='r') as file:
        csvFile = csv.reader(file)
        for row in csvFile:
            t= []
            for s1 in row:
                t.append(coerce(s1))
            fun(t)
        
def get_stats(arr, model_name, stat_dic):
    d = {}
    for item in arr:
        stats = Query.stats(item)
        for k,v in stats.items():
            d[k] = d.get(k,0) + v
            if k in stat_dic:
                stat_dic[k][model_name].append(v)

    for k,v in d.items():
        d[k] /= the["n_iter"]
    return d, stat_dic

def get_data(algorithm, answer, data, halves, reuse, conf_interval):
    flag = False

    if algorithm == "baseline":

        best, rest, evals_sway = optimize.sway(data, reuse, halves)
        rule, _ = Discretization.xpln(data, best, rest, conf_interval)

        answer['all'].append(data)
        if rule:
            data1 = Data(data, Discretization.selects(rule, data.rows))

            answer['sway'].append(best)
            print("value at best",type(best))
            answer['xpln'].append(data1)

            top2, _ = Query.betters(best)
            top = Data(data, top2)
            answer['top'].append(top)

            flag = True
       
    else:
        best, rest, evals_sway = optimize.sway2(data, reuse, halves)
        rule, _ = Discretization.xpln(data, best, rest, conf_interval)

        if rule:
            data1 = Data(data, Discretization.selects(rule, data.rows))
            # data2 = Data(data, Discretization.selects(rule2, data.rows))

            answer['sway2'].append(best)
            answer['xpln2'].append(data1)

            flag = True
        
    return flag

def update_conj_table(table, answer, data):
    global count
    for i in range(len(table)):
        [base, diff], result = table[i]

        if not result:
            table[i][1] = ["=" for _ in range(len(data.cols.y))]

        for k in range(len(data.cols.y)):
    
            if table[i][1][k] == "=":
            
                base_y, diff_y = answer[base][count].cols.y[k].col, answer[diff][count].cols.y[k].col
                equals = Misc.bootstrap(base_y.check(), diff_y.check()) and Misc.cliffs_delta(base_y.check(), diff_y.check())
                # if base == diff:
                #     print("CHECKING FOR ALL TO ALL:", equals)
                if not equals:
                    if i == 0:
                        print("WARNING: all to all {} {} {}".format(i, k, "false"))
                        print(f"all to all conjunction_table failed for {answer[base][count].cols.y[k].col.txt}")
                    table[i][1][k] = "≠"
    count += 1

def test_project():
    answer = {"all": [], "sway": [], "xpln": [], "sway2": [], "xpln2" : [], "top": []}

    conjunction_table = [[["all", "all"], None], 
                    [["all", "sway"], None],
                    [["all", "sway2"], None],  
                    [["sway", "sway2"], None],  
                    [["sway", "xpln"], None],
                    [["sway2", "xpln2"], None],
                    [["sway", "top"], None],
                    ]
                
    stats_rx = defaultdict(defaultdict)

    while count < the["n_iter"]:

        the["seed"] = random.randint(1, 999999999)
        data = Data(the["file"])
        for col in data.cols.y:
            if col.col.txt not in stats_rx:
                stats_rx[col.col.txt] = defaultdict(list)

        flag = get_data("baseline", answer, data, the["halves"], the["reuse"], the["conf_interval"])
        flag2 = get_data("new_model", answer, data, the["halves"], the["reuse"], the["conf_interval"])

        if flag:
            update_conj_table(conjunction_table, answer, data)

        titles = [y.col.txt for y in data.cols.y]
        top_table = []
        for k,v in answer.items():
            stats, stats_rx = get_stats(v, k, stats_rx)
            stats_list = [k] + [stats[y] for y in titles]
            
            top_table.append(stats_list)
        
        print(tabulate(top_table, headers=titles, numalign="left"))
        print()

        conjunction=[]
    
        for [base, diff], result in conjunction_table:
            conjunction.append([f"{base} to {diff}"] + result)
        print(tabulate(conjunction, headers=titles))
    
    for key, val in stats_rx.items():
        temp = []
        for k, v in val.items():
            # print("Printing list:", v)
            temp.append(Misc.RX(v, k))
        
        sk = Misc.scottKnot(temp)
        tiles_sk = Misc.tiles(sk)
        for rx in tiles_sk:
            print(rx["name"], rx["rank"], rx["show"])