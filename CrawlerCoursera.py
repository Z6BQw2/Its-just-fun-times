# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 13:43:49 2024

@author: Tommy
"""
from bs4 import BeautifulSoup as bs
import requests as rq
import re
import pandas as pd 

sca = rq.get("https://www.coursera.org/browse")
page = bs(sca.text, "html.parser")
subjects1 = page.findAll('img', class_='topic-image')

subjects2 = [sub.get('alt') for sub in subjects1]
subjects = []

for j, sub in enumerate(subjects2):
    pat = sub.split(' ')
    lopunny = ''
    for el in pat:
        if lopunny == '':
            lopunny = el
        else:
            lopunny += '-' + el
    lopunny = lopunny.lower()
    subjects.append(lopunny)
    lopunny = ''

dico = {}
for subject in subjects:
    
    sca = rq.get("https://www.coursera.org/browse/" + subject)
    page = bs(sca.text, "html.parser")
    popular1 = page.findAll('span', attrs={'class':'_1q9sh65'})
    popular = [pop.get_text() for pop in popular1]
    dico[subject]=popular
    
BDD = []

for key, val in dico.items():
    for el in val:
        
        sca = rq.get("https://www.coursera.org/courses?query=" + el)
        page = bs(sca.text, "html.parser")
        cours1 = page.findAll('a', attrs={'href':re.compile(r'/learn/')})
        cours = [pop.get('aria-label') for pop in cours1]
        
        for i, cour1 in enumerate(cours):
            if cour1 != None:
                cour = cour1.split(',') 
                lvl = cour1.split(' ')
                for i, mot in enumerate(lvl):
                    if mot == 'level':
                        break
                BDD.append((key, el, cour[0], cour[1], lvl[i-1] + ' ' + lvl[i]))

df = pd.DataFrame(BDD, columns=['Category', 'Popular Course', 'Course Name', 'Institution', 'Level'])

df.to_excel('coursera_courses2.xlsx', index=False)

print("Data has been successfully saved to 'coursera_courses2.xlsx'")
