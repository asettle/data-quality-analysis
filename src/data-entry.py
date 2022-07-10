#!/usr/bin/env python3

# modules
import pandas as pd
import numpy as np
from autocorrect import Speller

df = pd.read_csv("../data/SIS_Faculty-List.csv", skipinitialspace = True)

#set unique identifiers for each row
df['ID'].is_unique

#rename columns
new_names =  {'MAJOR TEACHING FIELD': 'Major Teaching Field',
              'DOCUMENT OTHER PROFESSIONAL CERTIFICATION CRITIERA Five Years Work Experience Teaching Excellence Professional Certifications': 'Relevant Experience',
              'All Qualifications from Profile': 'All Qualifications',
              'Join\nDate': 'Join Date',
              'Highest\nQualification\nLevel': 'Highest Qualification Level',
              'Courses Taught- Term 201510': 'Courses Taught'
              }
df.rename(columns=new_names, inplace=True)

#convert value 0 to NaN in ID column so that it can be dropped if empty
df.replace({'ID': '0'}, {'ID': None}, inplace=True)

#drop rows with empty values
df.dropna(subset=['ID',
                  'Name',
                  'Location',
                  'Join Date'], inplace=True)

#drop rows with duplication ID value
df.drop_duplicates(subset=['ID'], inplace=True)

#drop columns with duplications of data
to_drop = ['Grade',
           'Title',
           'Type',
           'Divison',
           'Highest Qualification Level']
df.drop(to_drop, inplace=True, axis=1)

#drop columns with less than 90% content
#todo/recommendation: calculate percentage full and apply to all
df.dropna(thresh=df.shape[0]*0.1,how='all',axis=1, inplace=True)

#correct spelling using spell_checker
#generic speller checker used, colloquial terms accepted
spell = Speller('en')
df["Highest Qualification"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['Highest Qualification']]
df["Major"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['Major']]
df["University"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['University']]
df["All Qualifications"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['All Qualifications']]
df["Courses Taught"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['Courses Taught']]
df["Major Teaching Field"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['Major Teaching Field']]
df["Relevant Experience"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['Relevant Experience']]
df["Criteria"] = [' '.join([spell(i) for i in str(x).split()]) for x in df['Criteria']]

#edit columns for ampersands
spec_chars = ["&"]
for char in spec_chars:
    df['Criteria'] = df['Criteria'].str.replace(char, 'and')
spec_chars = ["&"]
for char in spec_chars:
    df['Relevant Experience'] = df['Relevant Experience'].str.replace(char, 'and')
spec_chars = ["&"]
for char in spec_chars:
    df['Major Teaching Field'] = df['Major Teaching Field'].str.replace(char, 'and')
spec_chars = ["&"]
for char in spec_chars:
    df['Courses Taught'] = df['Courses Taught'].str.replace(char, 'and')
spec_chars = ["&"]
for char in spec_chars:
    df['All Qualifications'] = df['All Qualifications'].str.replace(char, 'and')
spec_chars = ["&"]
for char in spec_chars:
    df['Major'] = df['Major'].str.replace(char, 'and')

#edit columns for forward slashes
spec_chars = ["/"]
for char in spec_chars:
    df['Criteria'] = df['Criteria'].str.replace(char, ' and ')
spec_chars = ["/"]
for char in spec_chars:
    df['Highest Qualification'] = df['Highest Qualification'].str.replace(char, ' and ')
spec_chars = ["/"]
for char in spec_chars:
    df['Relevant Experience'] = df['Relevant Experience'].str.replace(char, ' and ')
spec_chars = ["/"]
for char in spec_chars:
    df['Major'] = df['Major'].str.replace(char, ' and ')
spec_chars = ["/"]
for char in spec_chars:
    df['Major Teaching Field'] = df['Major Teaching Field'].str.replace(char, ' and ')

#print result to new csv file
df.to_csv('updated-SIS_Faculty-List.csv', encoding='utf-8')
