# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:32:22 2024

@author: Tommy
"""

import pandas as pd
import torch
from transformers import BertTokenizer, BertModel

df = pd.read_excel('coursera_courses2.xlsx')
df = df[df['Institution'].str[1].str.isdigit()]
df['Institution'] = df['Institution'].apply(lambda x: x[1:4])

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    
    return cls_embedding

df['Course Name Vectorized'] = df['Course Name'].apply(get_bert_embedding)

print(df)



df.to_excel('coursera_courses4_cleaned.xlsx', index=False)
print("Les données ont été sauvegardées avec succès dans 'coursera_courses4_cleaned.xlsx'.")

