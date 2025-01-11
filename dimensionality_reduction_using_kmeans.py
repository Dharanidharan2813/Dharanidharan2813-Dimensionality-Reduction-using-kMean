# -*- coding: utf-8 -*-
"""Dimensionality Reduction using kMeans.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b7N-DxJ8kKpsYFKK-itmDn9OXToNU41i
"""

import requests
from bs4 import BeautifulSoup
import zipfile
import io
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
import time

# Function to download and load dataset
def load_data():
    page_url = 'https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones'
    page_response = requests.get(page_url)
    if page_response.status_code == 200:
        soup = BeautifulSoup(page_response.content, 'html.parser')
        download_link = soup.select_one('a[href$=".zip"]')['href']
        full_download_url = 'https://archive.ics.uci.edu' + download_link
        response = requests.get(full_download_url)
        if response.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(response.content)) as outer_zip:
                inner_zip_name = 'UCI HAR Dataset.zip'
                with outer_zip.open(inner_zip_name) as inner_zip_file:
                    with zipfile.ZipFile(io.BytesIO(inner_zip_file.read())) as inner_zip:
                        with inner_zip.open('UCI HAR Dataset/train/X_train.txt') as myfile:
                            df = pd.read_csv(myfile, delim_whitespace=True, header=None)
                        with inner_zip.open('UCI HAR Dataset/train/y_train.txt') as myfile_y:
                            y = pd.read_csv(myfile_y, delim_whitespace=True, header=None)
    else:
        raise Exception("Failed to download or parse the dataset.")
    return df, y

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.cluster import KMeans
import numpy as np
import time

# Load dataset
df, y = load_data()

#TASK 1 - DO EDA and understand a little about the data.
#Only important thing is to know that it has a lot of features that don't make sense, just a
#bunch of readings from sensors.
#We think many of these features are redundant or irrelevant, and we want to find good features.

print(df.head())

print(y.head())

print(y.info())

print(df.describe())

print(df.isnull().sum())

# Task 2: Encode class labels
# YOUR CODE HERE: Use LabelEncoder to encode class labels
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
encoded_y = label_encoder.fit_transform(y.values.ravel())

# Task 3: Scale the features using StandardScaler
# YOUR CODE HERE: Apply StandardScaler to df
from sklearn.preprocessing import StandardScaler

scaler =StandardScaler() # YOUR CODE HERE
df_scaled =scaler.fit_transform(df)# YOUR CODE HERE

# Task 4: Split the data into training and testing sets
# YOUR CODE HERE: Use train_test_split to split the data
from sklearn.model_selection import train_test_split
X=df_scaled
y=encoded_y
X_train_full, X_test_full, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import time

star_ti= time.time()

pipeline = Pipeline([
    ('naive_bayes', GaussianNB())
])

pipeline.fit(X_train_full, y_train)

y_pred = pipeline.predict(X_test_full)
end_ti=time.time()
print(f"Time taken: {end_ti-star_ti} seconds")
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# TASK 7 - K-Means for dimensionality reduction

n_clusters = 3
# Use random_state instead of random
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(df_scaled.T)  # Transpose to treat features as data points
selected_features_indices = [np.random.choice(np.where(kmeans.labels_ == i)[0]) for i in range(n_clusters)] #FILL
selected_features = df_scaled[:, selected_features_indices] #FILL

#TASK 8 - Train another model (GaussianNB) on the new dataset, and report time taken and accuracy
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import time

star_ti= time.time()

pipeline = GaussianNB()

pipeline.fit(X_train_full, y_train)

y_pred = pipeline.predict(X_test_full)
end_ti=time.time()
print(f"Time taken: {end_ti-star_ti} seconds")
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")