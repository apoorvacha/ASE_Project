from sklearn import preprocessing, tree
from Sym import Sym
from Data import Data
from sklearn.ensemble import RandomForestClassifier


def xpln2(data, best, rest):
    
    training_data_X = []
    training_data_Y = []

    all_data = [[row.cells[col.col.at] for col in data.cols.x] for row in data.rows]

    encoder = preprocessing.LabelEncoder()
    for i, col in enumerate(data.cols.x):
        if isinstance(col.col, Sym):
            encoded_col = encoder.fit_transform([x[i] for x in all_data])
            for j, val in enumerate(all_data):
                val[i] = encoded_col[j]

    flag = False
    for r in best.rows:
        best_temp = []
        for col in best.cols.x:
            val = r.cells[col.col.at]
            if val == "?":
                flag = True
                break
            best_temp.append(val)
        if not flag:
            training_data_X.append(best_temp)
            training_data_Y.append(0)
        else:
            flag = False

    for r in rest.rows:
        rest_temp = []
        for col in rest.cols.x:
            val = r.cells[col.col.at]
            if val == "?":
                flag = True
                break
            rest_temp.append(val)
        if not flag:
            training_data_X.append(rest_temp)
            training_data_Y.append(1)
        else:
            flag = False

    encoder = preprocessing.LabelEncoder()
    for i, col in enumerate(data.cols.x):
        if isinstance(col.col, Sym):
            encoded_col = encoder.fit_transform([x[i] for x in training_data_X])
            for j, val in enumerate(training_data_X):
                val[i] = encoded_col[j]

    classifier = tree.DecisionTreeClassifier(max_depth=4)
    classifier.fit(training_data_X, training_data_Y)

    best = []
    for i, x in enumerate(all_data):
        if "?" not in x:
            res = classifier.predict([x])
            if res == 0:
                best.append(data.rows[i])

    return Data(data, best)