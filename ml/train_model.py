import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

#================================
# Import the dataset
#================================
df=pd.read_csv('ml/ObesityDataSet_raw_and_data_sinthetic.csv')
print(df.head())
df["history"]=df["family_history_with_overweight"].apply(lambda x: 1 if x=="yes" else 0)

#================================
# Test train split 
#================================

X=df[['Age','Height','Weight','history']]
y=df['NObeyesdad']
X_train , X_test, y_train, y_test= train_test_split(X,y,test_size=0.2, random_state=42)
#print(X_train.shape,X_test.shape, y_train.shape, y_test.shape)

#================================
# Model training
#================================

model=RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train,y_train)
y_pred=model.predict(X_test)
accuracy=accuracy_score(y_test,y_pred)
print(f'Accuracy: {accuracy*100:.2f}%')
print(classification_report(y_test,y_pred))
# joblib.dump(model,'ml/obesity_model.pkl')


