# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 12:47:34 2016

@author: Adam
"""

import requests
from bs4 import BeautifulSoup
import csv
import re


fin = open('prospects_2016.csv', 'rb')
reader = csv.DictReader(fin, dialect = 'excel')
fout = open('prospects_2016_college.csv', 'wb')
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
writer.writerow(['first_name', 'last_name', 'draft', 'games', 'tfls', 'sacks',
               'production_ratio'])

# scrape CFB stats page and fill out table
for i in range(0, len(first_name)):
    query = {'search': first_name[i] + ' ' + last_name[i]}    
    r = requests.get('http://www.sports-reference.com/cfb/search/search.fcgi?',
                     params = query)
    print r.url
    soup = BeautifulSoup(r.text, 'lxml')    

    try:
        cgames = []
        ctfls = []
        csacks = []
        table = soup.find('tbody')
        for row in table.find_all('tr'):
            tds = row.find_all('td')
            
            try:
                cgames.append(float(tds[5].get_text().strip()))
                ctfls.append(float(tds[9].get_text().strip()))
                csacks.append(float(tds[10].get_text().strip()))
            except:
                pass
            
        m = re.search('(?<=Draft: )\d+', soup.get_text())
        
        try:
            draft = m.group()
        except:
            draft = 'NA'

        games = sum(cgames[-2:])
        tfls = sum(ctfls[-2:])
        sacks = sum(csacks[-2:])
        production_ratio = round(((tfls + sacks) / games), 2)
        
        print games, tfls, sacks, production_ratio

        writer.writerow([first_name[i], last_name[i], draft, games, tfls, 
                       sacks, production_ratio])
   
    except:
        continue
       
fin.close()
fout.close()