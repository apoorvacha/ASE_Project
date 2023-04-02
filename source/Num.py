import math

from Misc import *

class Num:
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.lo = float('inf')
        self.hi = float('-inf')
        self.ok = True
        self.has = []
        self.w = -1 if '-' in self.txt else 1 

    def add(self, n):
        if n !="?":
            n = float(n)
            self.n = self.n + 1
            d = n - self.mu
            self.mu = self.mu + (d / self.n)
            self.m2 = self.m2 + (d * (n - self.mu))
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)


    def mid(self):
        return self.mu # n; return mean

    def div(self): 
        if self.m2 < 0 or self.n < 2:
            return 0
        else:
            return pow((self.m2/(self.n-1)),0.5)
        

