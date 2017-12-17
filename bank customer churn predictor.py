# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 21:49:54 2017

@author: Ajay
"""

#Artificial Neural Network

#Installing Theano

#Installing Tensorflow

#Installing Keras


#Part1- Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

# Encoding categorical data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])

onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X=X[:,1: ]

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Fitting classifier to the Training set
#Part2-Making the ANN

#Importing the keras library
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

#Initialising the ANN
classifier= Sequential()

#Adding the input layer adn the first hidden layer with dropout
classifier.add(Dense(output_dim=6,init='uniform',activation='relu',input_dim=11))
classifier.add(Dropout(p=0.1))
#Adding the second hidden layer
classifier.add(Dense(output_dim=6,init='uniform',activation='relu'))
classifier.add(Dropout(p=0.1))
#Adding the output layer

classifier.add(Dense(output_dim=1,init='uniform',activation='sigmoid'))
#Compiling the ANN
classifier.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

#Fitting the ANN to the training set
classifier.fit(X_train,y_train,batch_size=25,epochs=500)

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred= (y_pred> 0.5)

#Predict a single prediction i.e a new customer of the bank
new_prediction = classifier.predict(sc.transform(np.array([[0.0,0,600,1,40,3,60000,2,1,1,50000]])))
new_prediction=(new_prediction>0.5)
# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

#Evaluating the  ANN
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
def build_classifier():
   
    
    
    classifier= Sequential()
    classifier.add(Dense(output_dim=6,init='uniform',activation='relu',input_dim=11))
    classifier.add(Dense(output_dim=6,init='uniform',activation='relu'))
    classifier.add(Dense(output_dim=1,init='uniform',activation='sigmoid'))
    classifier.compile(optimizer='adam', loss='binary_crossentropy',metrics=['accuracy'])
    return classifier
classifier=KerasClassifier(build_fn=build_classifier,batch_size=10,nb_epoch=100)
accuracies=cross_val_score(estimator=classifier, X=X_train,y=y_train,cv=10)
print (accuracies.mean())
print (accuracies.var())
#Improving the ANN

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
def build_classifier(optimizer):
   
    
    
    classifier= Sequential()
    classifier.add(Dense(output_dim=6,init='uniform',activation='relu',input_dim=11))
    classifier.add(Dense(output_dim=6,init='uniform',activation='relu'))
    classifier.add(Dense(output_dim=1,init='uniform',activation='sigmoid'))
    classifier.compile(optimizer=optimizer, loss='binary_crossentropy',metrics=['accuracy'])
    return classifier
classifier=KerasClassifier(build_fn=build_classifier)

parameters= {'batch_size':[25,32],
             'epochs':[100,500],
             'optimizer':['adam','rmsprop']}
grid_search=GridSearchCV(estimator=classifier,param_grid=parameters,
                         scoring='accuracy',cv=10)

grid_search=grid_search.fit(X_train,y_train)
best_parameters=grid_search.best_params_
best_accuracy=grid_search.best_score_




















