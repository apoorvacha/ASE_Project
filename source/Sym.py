import math

class Sym:
     
    def __init__(self, at =0, txt =""):
        self.at = at
        self.txt = txt
        self.n = 0
        self.most = 0
        self.has = {}
        self.isSym = True
        self.mode = None
        # self.w = -1 if '-' in self.txt else 1 

    def add(self, x:str, n=1):
        if x != '?':
            self.n+=1
            if x in self.has:
                self.has[x] = n+self.has[x] + 1
            else: 
                self.has[x] =0
        
            if self.has[x] > self.most:
                self.most,self.mode = self.has[x],x
        return x

    # def add(self, x: str, n=1):
    #     if x != "?":
    #         self.n = self.n + n
    #         self.has[x] = n + (self.has[x] if x in self.has else 0)
    #         if self.has[x] > self.most:
    #             self.most = self.has[x]
    #             self.mode = x
    #     return x

    def mid(self):
        return self.mode

    def div(self):
        def fun(p):
            return p*math.log(p,2)
        e = 0
        for k, v in self.has.items():
            e = e + fun(v/self.n)
        return -e
    
