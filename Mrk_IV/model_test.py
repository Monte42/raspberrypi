import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

filename = "./files/models/model_1.sav"
saved_model = pickle.load(open(filename, "rb")) if os.path.isfile(filename) else None
best_model = saved_model['model'] if saved_model else None
best_acc = saved_model['accuracy'] if saved_model else 0
model_type = saved_model['model_type'] if saved_model else ''

df = pd.read_csv('./files/datasets/full.csv')

X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)

# RUN UN SCALED FOR BETTER RESULTS in forests
sc = StandardScaler()
X_train_std = sc.fit_transform(X_train)
X_test_std = sc.transform(X_test)

# print("Logistic Regression")
# for e in range(1,101):
#     lr_ovr = LogisticRegression(C=float(e), solver='lbfgs', multi_class='ovr')
#     lr_ovr.fit(X_train_std, y_train)
#     acc = round(lr_ovr.score(X_test_std, y_test)*100, 2)
#     print(f'"ovr" - ACC: {acc}%\tc: {float(e)}')
#     if acc > best_acc:
#         best_model = lr_ovr
#         best_acc = acc
#         model_type = 'lr_ovr'
#         print(f'Best Set LR OVR {acc}%')

#     lr_multin = LogisticRegression(C=float(e), solver='lbfgs', multi_class='multinomial', max_iter=10000)
#     lr_multin.fit(X_train_std, y_train)
#     acc = round(lr_multin.score(X_test_std, y_test)*100, 2)
#     print(f'"multinomial" ACC: {acc}%\tc: {float(e)}')
#     if acc > best_acc:
#         best_model = lr_multin
#         best_acc = acc
#         model_type = 'lr_multin'
#         print(f'Best Set LR multiN {acc}%')

# print('\n\nDecision Tree')
# for e in range(1,51):
#     tree_model = DecisionTreeClassifier(criterion='entropy', max_depth=e)
#     tree_model.fit(X_train, y_train)
#     acc = round(tree_model.score(X_test, y_test)*100, 2)
#     print(f'tree - ACC: {acc}%\tbranches: {float(e)}')
#     if acc > best_acc:
#         best_model = tree_model
#         best_acc = acc
#         model_type = 'tree'
#         print(f'Best Set tree {acc}%')

# print('\n\nForest')
# for e in range(10, 101):
#     forest = RandomForestClassifier(n_estimators=e, n_jobs=2)
#     forest.fit(X_train, y_train)
#     acc = round(forest.score(X_test, y_test)*100, 2)
#     print(f'Forest - ACC: {acc}%\ttrees: {float(e)}')
#     if acc > best_acc:
#         best_model = forest
#         best_acc = acc
#         model_type = 'forest'
#         print(f'Best Set forest {acc}%')

print('\n\nKNN')
for e in range(5,101):
    knn = KNeighborsClassifier(n_neighbors=e, p=1, metric='minkowski')
    knn.fit(X_train, y_train)  
    acc = round(knn.score(X_test, y_test)*100, 2)
    print(f'knn - ACC: {acc}%\tneighborhs: {float(e)}')
    if acc > best_acc:
        best_model = knn
        best_acc = acc 
        model_type = 'neighborh'
        print(f'Best Set neighborh {acc}%')


print(f'Best Model: {model_type}, with an accuracy of {best_acc}%')
model_data = {'accuracy': best_acc, 'model_type':model_type, 'model': best_model}

# save model
pickle.dump(model_data, open(filename, "wb"))
# load model
loaded_model_data = pickle.load(open(filename, "rb"))
loaded_model = loaded_model_data['model']
acc = round(loaded_model.score(X_test, y_test)*100, 2)
print(f'Loaded Model - ACC: {acc}%')