import numpy as np
import pandas as pd
from sklearn import tree

from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
dataset=pd.read_csv('trainset_judged.csv')
dataset_encoded = dataset.iloc[:,0:8] #placeholder
le=LabelEncoder()
for i in dataset_encoded:
    dataset_encoded[i]=le.fit_transform(dataset_encoded[i])

print(dataset)
print(dataset_encoded)

#Feature Set
X=dataset_encoded.iloc[:,0:7].values
#Expected result Set
Y=dataset_encoded.iloc[:,7].values

X_train,X_test,Y_train,Y_test=train_test_split(X,Y, test_size = 0.2)

model=DecisionTreeClassifier(criterion='gini')
model.fit(X_train,Y_train)
print(model.score(X_test, Y_test))
text_representation = tree.export_text(model)
print(text_representation)
#model.predict(["carrot", "sandy", 0.01, "no", -5, "morning", 90])
#print(le.fit(["carrot", "sandy", 0.01, "no", -5, "morning", 90]))


