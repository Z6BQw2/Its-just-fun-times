# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 12:25:17 2024

@author: Tommy
"""

import pandas as pd
import torch
from transformers import BertTokenizer, BertModel
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from Data_Cleaning import get_bert_embedding

df = pd.read_excel('coursera_courses4_cleaned.xlsx')


#Je sais pas si ça sert à quelque chose, y'a surrement des infos viable même si, si j'avais plus d'un demi-cerveau, j'aurais utilisé un truc plus cohérent que du clustering (Transfo ou que sais-je...). Mais bon, FLEMME. Je sais pas comment j'en suis venu à penser que stemming et clustering feraient bon ménage, mais YOLO.
kmeans = KMeans(n_clusters=10, random_state=42) #Chais pas, 10 ça semble pas mal vu que Coursera est pas très diversifié (très très IA, etc surtout) et que mon PC est trop vieux pour ces conneries.
clusters = kmeans.fit_predict(list(df['Course Name Vectorized']))

df['Cluster'] = clusters

X = df[['Institution', 'Difficulty', 'Cluster']]
y = df['Course Name']

X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

decision_tree = DecisionTreeClassifier(random_state=42)
decision_tree.fit(X_train, y_train)

y_pred = decision_tree.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision de l'arbre de décision : {accuracy * 100:.2f}%")

def recommend_course(user_input):
    user_cluster = kmeans.predict([get_bert_embedding(user_input)])
    cluster_courses = df[df['Cluster'] == user_cluster[0]]
    recommendations = cluster_courses['Course Name'].head(5)
    return recommendations

user_input = "Introduction to Machine Learning"
recommendations = recommend_course(user_input)
print("Cours recommandés :", recommendations)
