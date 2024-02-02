import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

filename = "test_model.sav"

def confirm_test_acc(X , y , learning_model):
    correct = 0
    for i in range(len(X)):
        prediction = learning_model.predict(X[i].reshape(1,-1))
        actual = y[i]
        if actual == prediction:
            correct += 1
    return round(correct/len(X)*100, 4)


df = pd.read_csv('./datasets/oval_track.csv')

X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# tree_model = DecisionTreeClassifier(criterion='entropy', max_depth=6, random_state=1)
# tree_model.fit(X_train, y_train)
# print(tree_model.score(X_train, y_train))
# print(f'ACC: {round(confirm_test_acc(X_test, y_test, tree_model))}%') 

best_model = pickle.load(open(filename, "rb")) if os.path.isfile(filename) else None
best_acc = 0
for i in range(40,70):
    forest = RandomForestClassifier(n_estimators=i, n_jobs=2)
    forest.fit(X_train, y_train)
    acc = confirm_test_acc(X_test, y_test, forest)
    print(f'Train set score: {forest.score(X_train, y_train)*100}%\nTest set confirmed Acc: {acc}%')
    if not best_model:
        best_model = forest
    if acc > best_acc:
        best_model = forest
    best_acc = max(acc, best_acc)
    

# save model
pickle.dump(best_model, open(filename, "wb"))
# load model
loaded_model = pickle.load(open(filename, "rb"))
print(f'\n======\n BEST \n {confirm_test_acc(X_test, y_test, loaded_model)}')