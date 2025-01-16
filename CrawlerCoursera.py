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
sca.raise_for_status()

page = bs(sca.text, "html.parser")
subjects1 = page.findAll('img', class_='topic-image')

subjects2 = [sub.get('alt') for sub in subjects1 if sub.get('alt')]
subjects = ['-'.join(sub.lower().split()) for sub in subjects2]

dico = {}

for subject in subjects:
    sca = rq.get(f"https://www.coursera.org/browse/{subject}")
    sca.raise_for_status()
    page = bs(sca.text, "html.parser")
    popular1 = page.findAll('span', class_='_1q9sh65')
    popular = [pop.get_text() for pop in popular1 if pop.get_text()]
    dico[subject] = popular

BDD = []

for key, val in dico.items():
    for el in val:
        sca = rq.get(f"https://www.coursera.org/courses?query={el}")
        sca.raise_for_status()
        page = bs(sca.text, "html.parser")
        cours1 = page.findAll('a', attrs={'href': re.compile(r'/learn/')})
        
        for cour in cours1:
            cour_label = cour.get('aria-label')
            if cour_label:
                parts = cour_label.split(',')
                course_name = parts[0].strip()
                
                institution = parts[1].strip()
                
                level_match = re.search(r'(Beginner|Intermediate|Advanced)', cour_label, re.IGNORECASE)
                level = level_match.group(0) if level_match else "Unknown"
                
                BDD.append((key, el, course_name, institution, level))

df = pd.DataFrame(BDD, columns=['Category', 'Popular Course', 'Course Name', 'Institution', 'Level'])

df.to_excel('coursera_courses4_fixed.xlsx', index=False)
print("Les données ont été sauvegardées avec succès dans 'coursera_courses4_fixed.xlsx'.")
