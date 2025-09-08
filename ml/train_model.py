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
#FCVC – Frequency of vegetable consumption (scale from 1 to 3).
#NCP – Number of main meals per day.
#CAEC – Frequency of consuming food between meals (Never, Sometimes, Frequently, Always)
#CH2O – Daily water intake (scale from 1 to 3).
#FAF – Physical activity frequency (scale from 0 to 3).
#TUE – Time spent using technology (scale from 0 to 3).
#CALC – Frequency of alcohol consumption (Never, Sometimes, Frequently, Always).
df['CAEC']=df['CAEC'].map({'no':0,'Sometimes':1,'Frequently':2,'Always':3})
df['CALC']=df['CALC'].map({'no':0,'Sometimes':1,'Frequently':2,'Always':3})
X=df[['Age','Height','Weight','history','FCVC','NCP','CH2O','FAF','TUE','CALC']]
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
joblib.dump(model,'ml/obesity_model.pkl')
#Enregistrer les données du modèle dans un fichier json
import json
model_info = {
    "model_name": "Obesity Classification Model",
    "model_version": "1.0",
    "features": ['Age','Height','Weight','history','FCVC','NCP','CH2O','FAF','TUE','CALC'],
    "classes": list(y.unique()),
    "last_training_date": "2025-09-08",
    "accuracy": accuracy
}
with open('ml/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=4)

#Enregistrer la matrice de métriques dans un fichier json
metrics = classification_report(y_test, y_pred, output_dict=True)
with open('ml/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=4)
