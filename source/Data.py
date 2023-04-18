import Misc
from Cols import COLS
import Rows, Examples1
import Update

class Data:

    def __init__(self, src, rows = None):
        self.rows = []
        self.cols = None
        #add = lambda t: Update.row(self, t)
        if isinstance(src, str):
            Examples1.readCSV(src, self.add)
        else:
            self.cols = COLS(src.cols.names)
            if rows:
                for row in rows:
                    self.add(row)

    def add(self, t):

        if self.cols:
            t = t if isinstance(t, Rows.Rows) else Rows.Rows(t)

            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)

    def clone(self, data, ts=None):
        data1 = Update.row(Data(), data.cols.names)
        # for t in ts or []:
        for t in (ts or []):
            Update.row(data1, t)
        return data1

