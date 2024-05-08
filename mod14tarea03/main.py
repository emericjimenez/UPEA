import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

import os
contenido = os.listdir('/app')
print(contenido)

df = pd.read_csv("data/dataset.csv")
X = np.array(df[["Brillo","Saturación"]])
y = np.array(df["Color"])
k = 3
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X, y)

test1 = np.array([50, 50])

prediction1 = knn.predict(test1.reshape(1, -1))

print("Prediction for test:", prediction1)


while True:
    strInput = input("Enter two values separated by comma or none for finish:  ")            
    if strInput == "":
        print("Finish")
        break
    else:        
        try:
            strList = strInput.split(",")
            intList = [int(x) for x in strList]
            print(intList)
            newArray = np.array(intList, dtype=int)
            prediction2 = knn.predict(newArray.reshape(1, -1))
            print("Prediction for new test:", prediction2)            
        except ValueError:
            print("Error: Invalid data.")        
