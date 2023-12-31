# -*- coding: utf-8 -*-
"""Multiple Linear Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oldqXV_kIDh7R7gvMCypxtjw9dHVbUco

# Multiple Linear Regression

## Importing the Libraries
"""

import numpy as np
import pandas as pd

"""## Importing tha Dataset"""

dataset = pd.read_csv('50_Startups.csv')
X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values

print(X)

print(y)

"""## Encoding the Categorical Data"""

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [3])], remainder='passthrough')
X = ct.fit_transform(X)
X = np.array(X)
print(X)

"""## Splitting the dataset into training and test sets"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""## Training the Multiple Regression Model"""

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

"""## Predicting the test set results"""

y_pred = regressor.predict(X_test)
results = np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1)
print(results)

"""## Questions

### 1. Making a single prediction (for example the profit of a startup with R&D Spend = 160000, Administration Spend = 130000, Marketing Spend = 300000 and State = 'California')
"""

print(regressor.predict([[1,0,0,160000,130000,300000]]))

"""## 2. Getting the final linear regression equation with the values of the coefficients"""

print(regressor.coef_)
print(regressor.intercept_)