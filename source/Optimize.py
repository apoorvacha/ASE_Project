import List, Query
from Start import the
from Cluster import half
import Data

def worker(data, rows, worse, evals0, reuse, halves, above = None):
    if len(rows) <= len(data.rows)**(0.5):
        return rows, List.many(worse, the["rest"] * len(rows)), evals0
    else:
        # l , r, A, B,c, evals = half(data, rows, None,  above)
        # l , r, A, B,c, evals = half(data, rows, None,  above)
        l , r, A, B,c, evals = half(data, reuse, halves, rows, None,  above)
        if Query.better(data, B, A):
            l, r, A, B = r, l, B, A
        for row in r:
            worse.append(row)
        return worker(data, l, worse,evals+evals0, reuse, halves, A)
        
def sway(data, reuse,halves = 512):

      best, rest , evals = worker(data, data.rows, [], 0, reuse, halves)
      return Data.Data(data, best), Data.Data(data, rest), evals
    #   return data.clone(data, best), data.clone(data, rest), evals


def sway2(data, reuse,halves = 512):
    
    best1, rest1, _ = worker(data, data.rows[:len(data.rows)//4], [], 0, reuse, halves)
    best2, rest2, _ = worker(data, data.rows[len(data.rows)//4:2*(len(data.rows)//4)], [], 0, reuse, halves)
    best3, rest3, _ = worker(data, data.rows[2*(len(data.rows)//4):3*(len(data.rows)//4)], [], 0, reuse, halves)
    best4, rest4, _ = worker(data, data.rows[3*(len(data.rows)//4):], [], 0, reuse, halves)
    
    best_all, rest_all, evals  = worker(data, best1 + best2 + best3 + best4, [] ,0, reuse, halves)

    return Data.Data(data, best_all), Data.Data(data, rest_all), evals