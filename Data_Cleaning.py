# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 14:32:22 2024

@author: Tommy
"""

import pandas as pd

df = pd.read_excel('coursera_courses2.xlsx')
df = df[df['Institution'].str[1].str.isdigit()]
df['Institution'] = df['Institution'].apply(lambda x: x[1:4])

df.to_excel('coursera_courses4_fixed.xlsx', index=False)
print("Les données ont été sauvegardées avec succès dans 'coursera_courses4_fixed.xlsx'.")
