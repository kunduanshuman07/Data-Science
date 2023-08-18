# -*- coding: utf-8 -*-
"""MLR_Template&Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZvD3OKZzVDpurz0x_c0Xo8Dohx2UJHFR

# Multiple Linear Regression

## Importing the Libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## Importing the Dataset"""

dataset = pd.read_csv('Data.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

print(X)

print(y)

"""## Splitting the Dataset into Training and Test sets"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

"""## Training the Multiple Linear Regression Model on the Training set."""

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

"""## Predicting Test Set Results"""

y_pred = regressor.predict(X_test)
np.set_printoptions(precision=2)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""## Evaluating the Model Performance"""

from sklearn.metrics import r2_score
r2_score(y_test, y_pred)