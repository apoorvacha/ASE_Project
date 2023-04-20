import Misc
from Cols import COLS
import Rows, Examples
import Update

class Data:

    def __init__(self, src, rows = None):
        self.rows = []
        self.cols = None
        #add = lambda t: Update.row(self, t)
        if isinstance(src, str):
            Examples.readCSV(src, self.add)
        else:
            self.cols = COLS(src.cols.names)
            if rows:
                for row in rows:
                    self.add(row)

    def add(self, t):

        if self.cols:
            if isinstance(t, Rows.Rows):
                t = t
            else:
                t = Rows.Rows(t)

            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)
