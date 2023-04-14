import Misc
from Cols import COLS
import Rows, Examples
import Update

# def csv_content(src):
#     res = []
#     with open(src, mode='r') as file:
#         csvFile = csv.reader(file)
#         for row in csvFile:
#             res.append(row)
#     return res

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

    def read_file(self, content):
        data = Data()
        callback_function = lambda t: Update.row(data, t)
        Examples.readCSV(content, callback_function)
        return data

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

