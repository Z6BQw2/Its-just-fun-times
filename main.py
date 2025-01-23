# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 21:36:22 2025

@author: Tommy
"""
import pandas as pd
import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from Data_Cleaning import get_bert_embedding

df = pd.read_excel('coursera_courses4_cleaned.xlsx')

def convert_to_vector(vector_string):
    vector = np.array(vector_string)
    return vector

df['Course Name Vectorized'] = df['Course Name Vectorized'].apply(convert_to_vector)

vector_matrix = np.stack(df['Course Name Vectorized'])

kmeans = KMeans(n_clusters=10) #Chais pas, 10 ça semble pas mal vu que Coursera est pas très diversifié (très très IA, etc surtout) et que mon PC est trop vieux pour ces conneries.
clusters = kmeans.fit_predict(vector_matrix)

df['Cluster'] = clusters

X = df[['Institution', 'Difficulty', 'Cluster']]
y = df['Course Name']

X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)

y_pred = decision_tree.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Précision de l'arbre : ", accuracy * 100)

def recommend_course(user_input):
    user_cluster = kmeans.predict([get_bert_embedding(user_input)])
    cluster_courses = df[df['Cluster'] == user_cluster[0]]
    recommendations = cluster_courses['Course Name'].head(5)
    return recommendations

user_input = "Introduction to Machine Learning"
recommendations = recommend_course(user_input)
print("Cours recommandés :", recommendations)
