#!/usr/bin/env python3

# modules
import pandas as pd
import numpy as np

# helpful modules
import fuzzywuzzy
from fuzzywuzzy import process
import chardet

df = pd.read_csv("SIS_Faculty-List.csv")

#set unique identifiers for ID
df['ID'].is_unique

#drop columns with duplications of data
to_drop = ['Grade',
           'Title',
           'Type',
           'Divison']
df.drop(to_drop, inplace=True, axis=1)

#drop columns with less than 90% content
to_drop = ['LWD']
df.drop(to_drop, inplace=True, axis=1)

#rename columns
new_names =  {'MAJOR TEACHING FIELD': 'Major Teaching Field',
              'DOCUMENT OTHER PROFESSIONAL CERTIFICATION CRITIERA Five Years Work Experience Teaching Excellence Professional Certifications': 'Relevant Experience',
              'All Qualifications from Profile': 'All Qualifications',
              'Highest' \
              'Qualification' \
              'Level': 'Highest Qualification Level'
              }
df.rename(columns=new_names, inplace=True)

spec_chars = ["&"]
for char in spec_chars:
    df['Criteria'] = df['Criteria'].str.replace(char, 'and')

spec_chars = ["/"]
for char in spec_chars:
    df['Criteria'] = df['Criteria'].str.replace(char, ' and ')

print(df)
