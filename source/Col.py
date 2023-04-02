from Num import *
from Sym import *
import re

class COL:
    def __init__(self, n, s):

        self.col = Num(n, s) if re.match("^[A-Z]",s) else Sym(n, s)
        self.isIgnored = self.col.txt.endswith("X")
        self.isKlass = self.col.txt.endswith("!")
        self.isGoal = self.col.txt[-1] in ["!", "+", "-"]


     
    
