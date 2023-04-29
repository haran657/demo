# -*- coding: utf-8 -*-
"""modelapp

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-uWpii5ZisMVjbs3Zv9zM9kzvoYAd2Xo
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('/content/spam.csv',encoding = "ISO-8859-1")

# Clean data 

df.rename(columns={
    'v1': 'label',
    'v2': 'message',
}, inplace=True)

df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)

# Encode labels

le = LabelEncoder()
le.fit(df['label'])
df['label'] = le.transform(df['label'])

df.to_csv('/content/spam.csv', encoding='ISO-8859-1')

joblib.dump(le, '/content/encoder.joblib')

import numpy as np
import pandas as pd
import joblib
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

df = pd.read_csv('/content/spam.csv', encoding = "ISO-8859-1")

# Splits training/test sets

X = df['message']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Builds model

clf = Pipeline(steps=[
    ('tfidf', TfidfVectorizer()),
    ('scaler', StandardScaler(with_mean=False)),
    ('lr', LogisticRegression())
])

# Trains model

clf.fit(X_train, y_train)

# Evaluates model

predictions = clf.predict(X_test)
accuracy = metrics.accuracy_score(y_test, predictions)
print(f"Logistic Regression Model Accuracy: {(accuracy * 100).round(2)}%")

# Saves model

joblib.dump(clf, '/content/model.joblib')

from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

model = joblib.load('/content/model.joblib')
encoder = joblib.load('/content/encoder.joblib')

@app.route('/')
def main():
    return render_template("/content/index.html")

@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        message = request.form['submission']
        prediction = model.predict([message])
        classification = encoder.inverse_transform(prediction)

        return render_template('/content/index.html', message=message, classification=classification)

if __name__ == "__main__":
    app.run(debug=True)