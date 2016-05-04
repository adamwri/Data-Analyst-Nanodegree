# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:51:50 2016

@author: Adam
"""

import requests
from bs4 import BeautifulSoup
import csv

fin = open('edge_combine_college.csv', 'rb')
reader = csv.DictReader(fin, dialect = 'excel')
fout = open('edge_nfl_stats.csv', 'wb')
writer = csv.writer(fout, dialect = 'excel')

first_name = []
last_name = []

# read in names
for row in reader:
    first_name.append(row['first_name'])
    last_name.append(row['last_name'])

#print first_name
#print last_name

# write headers
writer.writerow(['first_name', 'last_name', 'sacks'])

# scrape NFL stats page and fill out table
for i in range(0, len(first_name)):
    query = {'search': first_name[i] + ' ' + last_name[i]}
    
    r = requests.get('http://www.pro-football-reference.com/search/search.fcgi?',
                     params = query)
    print r.url
    soup = BeautifulSoup(r.text, 'lxml')    

    try:
        sackt = []
        table = soup.find('tbody')
        for row in table.find_all('tr'):
            tds = row.find_all('td')
            
            if tds[17].get_text() == '':
                sackt.append(float(0.0))
            else:
                sackt.append(float(tds[17].get_text().strip()))          
                
        sacks = sum(sackt[:4])
        print sacks        
        
        writer.writerow([first_name[i], last_name[i], sacks])
   
    except:
        continue
        
fin.close()
fout.close()