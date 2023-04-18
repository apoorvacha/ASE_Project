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

        best, rest = optimize.sway(data, reuse, halves)
        rule, _ = Discretization.xpln(data, best, rest, conf_interval)

        answer['all'].append(data)
        if rule:
            data1 = Data(data, Discretization.selects(rule, data.rows))

            answer['sway'].append(best)
            answer['xpln'].append(data1)

            top2, _ = Query.betters(best)
            top = Data(data, top2)
            answer['top'].append(top)

            flag = True
       
    else:
        best, rest = optimize.sway2(data, reuse, halves)
        rule, _ = Discretization.xpln(data, best, rest, conf_interval)

        if rule:
            data1 = Data(data, Discretization.selects(rule, data.rows))

            answer['sway2'].append(best)
            answer['xpln2'].append(data1)

            flag = True
        
    return flag

def update_conj_table(table, answer, data):
    global iterations
    for i in range(len(table)):
        [comp1, comp2], result = table[i]

        if not result:
            table[i][1] = ["=" for _ in range(len(data.cols.y))]

        for k in range(len(data.cols.y)):
    
            if table[i][1][k] == "=":
                # print(len(answer[comp1]))
                comp1_val, comp2_val = answer[comp1][len(answer[comp1])-1].cols.y[k].col, answer[comp2][len(answer[comp2])-1].cols.y[k].col
                # comp1_val, comp2_val = answer[comp1][iterations].cols.y[k].col, answer[comp2][iterations].cols.y[k].col
                check1 = Misc.bootstrap(comp1_val.check(), comp2_val.check()) 
                check2 = Misc.cliffs_delta(comp1_val.check(), comp2_val.check())
                if not (check1 and check2):
                    table[i][1][k] = "≠"
    iterations += 1
top_table = []
conjunction=[]
def get_Table(titles,answer, stats_rx):
        for k,v in answer.items():
            stats, stats_rx = get_stats(v, k, stats_rx)
            stats_list = [k] + [stats[y] for y in titles]
                
            top_table.append(stats_list)
        return top_table

def test_project():
    answer = {"all": [], "sway": [], "xpln": [], "sway2": [], "xpln2" : [], "top": []}
    print('The code is running. Please wait.....')
    conjunction_table = [[["all", "all"], None], 
                    [["all", "sway"], None],
                    [["all", "sway2"], None],  
                    [["sway", "sway2"], None],  
                    [["sway", "xpln"], None],
                    [["sway2", "xpln2"], None],
                    [["sway", "top"], None],
                    ]
                
    stats_rx = defaultdict(defaultdict)
    
    data = Data(the["file"])

    for col in data.cols.y:
            if col.col.txt not in stats_rx:
                stats_rx[col.col.txt] = defaultdict(list)

    while iterations < the["n_iter"]:

        the["seed"] = random.randint(1, 999999999)
        flag = get_data("baseline", answer, data, the["halves"], the["reuse"], the["conf_interval"])
        flag2 = get_data("new_model", answer, data, the["halves"], the["reuse"], the["conf_interval"])
        if flag and flag2:
            update_conj_table(conjunction_table, answer, data)
        

    titles = [y.col.txt for y in data.cols.y]
    print(" \nThe mean results over 20 repeated runs:\n")
    print(tabulate(get_Table(titles, answer, stats_rx), headers=titles, numalign="left"))
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
        
        sk = Misc.scottKnot(temp)
        tiles_sk = Misc.tiles(sk)
        for rx in tiles_sk:
            print(rx["name"], rx["rank"], rx["show"])
    return True