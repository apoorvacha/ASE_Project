import math
import Misc

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
        self.has = {}
        self.w = -1 if '-' in self.txt else 1 
        self.sd = 0

    def add(self, x):
        if x != "?":
            self.n += 1
            self.lo, self.hi = min(x, self.lo), max(x, self.hi)
            all = len(self.has)

            if all < 512:
                loc = all+1
            else:
                if Misc.rand()<512 / self.n:
                    loc = Misc.rint(1,all)
                else:
                    loc = 0
            
            if loc:
                self.has[loc] = x
                self.ok = False

            d = x - self.mu
            self.mu = self.mu + d/self.n
            self.m2 = self.m2 + d*(x-self.mu)
            self.sd = 0 if self.n<2 else (self.m2/(self.n - 1))**.5

    def checkSort(self):
        self.ok = True
        A =sorted(self.has.items(), key=lambda x: x[1])
        A = dict(A)
        B = list(A.values())
        return B
    
    def mid(self):
        return self.mu

    def div(self): 
        if self.m2 < 0 or self.n < 2:
            return 0
        else:
            return pow((self.m2/(self.n-1)),0.5)