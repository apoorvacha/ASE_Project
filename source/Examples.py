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
from xpln2 import *

iterations = 0

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
    for val in arr:
        stats = Query.stats(val)
        for key,value in stats.items():
            d[key] = d.get(key,0) + value
            if key in stat_dic:
                stat_dic[key][model_name].append(value)

    for key,val in d.items():
        d[key] /= the["iterations"]
    return d, stat_dic

def get_data(algorithm, answer, data, halves, reuse, conf_interval):
    flag = False

    if algorithm == "baseline":

        best, rest = optimize.sway(data, reuse, halves)
        rule, _ = Discretization.xpln(data, best, rest, conf_interval)

        answer['all'].append(data)
        if rule:
            data1 = Data(data, Discretization.selects(rule, data.rows))

            answer['sway'].append(best)
            answer['xpln'].append(data1)

            top, _ = Query.betters(best)
            top = Data(data, top)
            answer['top'].append(top)

            flag = True
       
    else:
        best, rest = optimize.sway2(data, reuse, halves)
        #rule, _ = Discretization.xpln(data, best, rest, conf_interval)
        best1 = xpln2(data,best,rest)
        answer['sway2'].append(best)
        answer['xpln2'].append(best1)

        flag = True
    
    return flag

def update_conj_table(table, answer, data):
    global iterations
    for i in range(len(table)):
        [comp1, comp2], result = table[i]

        if not result:
            table[i][1] = ["="]*len(data.cols.y)

        for k in range(len(data.cols.y)):
    
            if table[i][1][k] == "=":
                # print(len(answer[comp1]))
                comp1_val = answer[comp1][len(answer[comp1])-1].cols.y[k].col
                comp2_val = answer[comp2][len(answer[comp2])-1].cols.y[k].col
                check1 = Misc.bootstrap(comp1_val.check(), comp2_val.check()) 
                check2 = Misc.cliffs_delta(comp1_val.check(), comp2_val.check())
                if (check1 and check2):
                    table[i][1][k] = "≠"
    iterations += 1

conjunction=[]

def get_table(titles,answer, stats_rx):
        final_table = []
        for key,val in answer.items():
            stats, stats_rx = get_stats(val, key, stats_rx)
            stats_list = [key] + [stats[y] for y in titles]
                
            final_table.append(stats_list)
        return final_table

def test_project():
    answer = {"all": [], "sway": [], "xpln": [], "sway2": [], "xpln2" : [], "top": []}
    print('The code is running. Please wait.....')
    conjunction_table = [[("all", "all"), None], 
                    [("all", "sway"), None],
                    [("all", "sway2"), None],  
                    [("sway", "sway2"), None],  
                    [("sway", "xpln"), None],
                    [("sway2", "xpln2"), None],
                    [("sway", "top"), None],
                    ]
                
    stats_rx = defaultdict(defaultdict)
    
    data = Data(the["file"])

    for col in data.cols.y:
            if col.col.txt not in stats_rx:
                stats_rx[col.col.txt] = defaultdict(list)

    while iterations < the["iterations"]:

        the["seed"] = random.randint(1, 999999999)
        flag = get_data("baseline", answer, data, the["halves"], the["reuse"], the["conf_interval"])
        flag2 = get_data("new_model", answer, data, the["halves"], the["reuse"], the["conf_interval"])
        if flag and flag2:
            update_conj_table(conjunction_table, answer, data)
        

    titles = [y.col.txt for y in data.cols.y]
    print(" \nThe mean results over 20 repeated runs:\n")
    print(tabulate(get_table(titles, answer, stats_rx), headers=titles, numalign="left"))
    print()
    for [comp1, comp2], result in conjunction_table:
        conjunction.append([f"{comp1} to {comp2}"] + result)
    print("Table shows the CONJUNCTION of a effect size test and a significance test that compares 20  results to 20 results from some other treatment")
    print(" ")
    print(tabulate(conjunction, headers=titles))
    print()
    for key, val in stats_rx.items():
        temp = []
        print('\nScott-Knott for Objective: ',key,'\n')
        for k, v in val.items():
            temp.append(Misc.RX(v, k))
        print("Printing temp:", temp)
        sk = Misc.scottKnot(temp)
        tiles_sk = Misc.tiles(sk)
        for rx in tiles_sk:
            print(rx["name"], rx["rank"], rx["show"])
    return True