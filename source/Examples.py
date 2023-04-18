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

def test_project():
    answer = {"all": [], "sway": [], "xpln": [], "sway2": [], "xpln2" : [], "top": []}

    conjunction_table = [[["all", "all"],None], 
                    [["all", "sway"],None],  
                    [["sway", "xpln"],None],  
                    [["sway", "top"],None]]
                
    n_evals = {"all": 0, "sway": 0, "xpln": 0, "sway2":0, "xpln2": 0, "top": 0}
    stats_rx = defaultdict(defaultdict)

    count = 0

    while count < the["n_iter"]:
        the["seed"] = random.randint(1, 999999999)
        data = Data(the["file"])
        for col in data.cols.y:
            if col.col.txt not in stats_rx:
                stats_rx[col.col.txt] = defaultdict(list)
       
        the["rest"] = 4 
        reuse =True
        halves = 512

        best, rest, evals_sway = optimize.sway(data, reuse, halves)
        the["rest"] = 8 
        reuse = False
        halves = 1024
        
        best2, rest2, evals_sway2 = optimize.sway(data, reuse, halves)

        conf_interval = 0.05

        rule, _ = Discretization.xpln(data, best, rest, conf_interval)
        rule2, _ = Discretization.xpln(data, best2, rest2, conf_interval)
        
        if rule != -1:
            data1 = Data(data, Discretization.selects(rule, data.rows))
            data2 = Data(data, Discretization.selects(rule2, data.rows))

            answer['all'].append(data)
            answer['sway'].append(best)
            answer['xpln'].append(data1)
            answer['sway2'].append(best2)
            answer['xpln2'].append(data2)

            top2,_ = Query.betters(best)
            top = Data(data,top2)
            answer['top'].append(top)

            n_evals["all"] += 0
            n_evals["sway"] += evals_sway

            n_evals["xpln"] += evals_sway
            n_evals["top"] += len(data.rows)


            for i in range(len(conjunction_table)):
                [base, diff], result = conjunction_table[i]

                if result == None:
                    conjunction_table[i][1] = ["=" for _ in range(len(data.cols.y))]
 
                for k in range(len(data.cols.y)):
           
                    if conjunction_table[i][1][k] == "=":
                 
                        base_y, diff_y = answer[base][count].cols.y[k].col,answer[diff][count].cols.y[k].col
                        equals = Misc.bootstrap(base_y.check(), diff_y.check()) and Misc.cliffs_delta(base_y.check(), diff_y.check())
                        if not equals:
                            if i == 0:
                       
                                print("WARNING: all to all {} {} {}".format(i, k, "false"))
                                print(f"all to all conjunction_table failed for {answer[base][count].cols.y[k].col.txt}")
                            conjunction_table[i][1][k] = "≠"
            count += 1

        highlight = True
        titles = [y.col.txt for y in data.cols.y]
        top_table = []
        for k,v in answer.items():
        
            stats, stats_rx = get_stats(v, k, stats_rx)
            stats_list = [k] + [stats[y] for y in titles]
            stats_list += [n_evals[k]/the["n_iter"]]
            
            top_table.append(stats_list)
        
        if highlight:
            for i in range(len(titles)):
                header_vals = [v[i+1] for v in top_table]
                fun = max if titles[i][-1] == "+" else min
                top_table[header_vals.index(fun(header_vals))][i+1] = '\033[92m' + str(top_table[header_vals.index(fun(header_vals))][i+1]) + '\033[0m'
        print(tabulate(top_table, headers=titles+["Avg evals"],numalign="right"))
        print()

        conjunction=[]
    
        for [base, diff], result in conjunction_table:
            conjunction.append([f"{base} to {diff}"] + result)
        print(tabulate(conjunction, headers=titles,numalign="right"))
    
    for key, val in stats_rx.items():
        temp = []
        for k, v in val.items():
            # print("Printing list:", v)
            temp.append(Misc.RX(v, k))
        
        sk = Misc.scottKnot(temp)
        tiles_sk = Misc.tiles(sk)
        for rx in tiles_sk:
            print(rx["name"], rx["rank"], rx["show"])