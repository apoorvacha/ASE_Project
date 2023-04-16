from Col import *

class COLS:
    def __init__(self, ss):
      
        self.names = ss
        self.all = []
        self.x = []
        self.y = []
        self.klass = None

        for n,s in enumerate(ss):
            col = COL(n,s)
            self.all.append(col)

            if not col.isIgnored:
                # if col.isKlass
                if hasattr(col, 'isKlass') and col.isKlass:
                    # col.isKlass = col
                    self.klass = col

                if col.isGoal:
                    self.y.append(col)
                else:
                    self.x.append(col)

    def add(self, row) -> None:

        for _, t in enumerate([self.x, self.y]):
            for _, col in enumerate(t):
                col.col.add(row.cells[col.col.at])
       
      