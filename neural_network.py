from pandas import read_csv
import numpy as np
from sklearn.preprocessing import LabelEncoder
def neural_network(dF,dT,E):
    dataframe = read_csv("data.csv", header=None)
    dataset = dataframe.values
    X = dataset[:,0:3].astype(float)
    y = dataset[:,3]

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    from sklearn.neural_network import MLPClassifier
    #mlp=MLPClassifier(hidden_layer_sizes=(10,10,10), max_iter=500, alpha=0.0001,
    #                    solver='adam', random_state=21,tol=0.000000001)
    mlp = MLPClassifier(hidden_layer_sizes=(6,6,6,6),solver='lbfgs',max_iter=6000)
    mlp.fit(X_train,y_train)

    X = scaler.transform([[dF,dT,E]])
    predictions_str = mlp.predict(X)
    print(predictions_str[0])
    predictions = mlp.predict_proba(X)

    return predictions[0,0]*100,predictions[0,1]*100,predictions[0,2]*100,predictions_str[0]
    #predictions = mlp.predict(X_test)
    #from sklearn.metrics import classification_report
    #print(classification_report(y_test,predictions))
