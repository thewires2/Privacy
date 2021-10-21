import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from privacyHE import initialize, load_public_key, load_relin_keys, load_encrypted_value

initialize('float')
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')

#dataset = pd.read_csv('181105_missing-data.csv')
dataset = pd.read_csv('C:\\Users\\arnav\\Downloads\\EncryptedSalary_data.dat',index_col = False)
new_df = pd.DataFrame()
columns = list(dataset.columns)
for column in columns:
    # print(column)
    x=[]
    for entry in list(dataset[column]):
        decrypted = load_encrypted_value(float(entry)) 
        x.append(decrypted)
    new_df[column] = x
dataset = new_df
X = dataset.iloc[:, :-1].values #get a copy of dataset exclude last column
y = dataset.iloc[:, 1].values #get array of dataset in column 1st

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)

"""
# Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
"""

# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)

# Visualizing the Training set results
viz_train = plt
viz_train.scatter(X_train, y_train, color='red')
viz_train.plot(X_train, regressor.predict(X_train), color='blue')
viz_train.title('Salary VS Experience (Training set)')
viz_train.xlabel('Year of Experience')
viz_train.ylabel('Salary')
viz_train.show()

# Visualizing the Test set results
viz_test = plt
viz_test.scatter(X_test, y_test, color='red')
viz_test.plot(X_train, regressor.predict(X_train), color='blue')
viz_test.title('Salary VS Experience (Test set)')
viz_test.xlabel('Year of Experience')
viz_test.ylabel('Salary')
viz_test.show()