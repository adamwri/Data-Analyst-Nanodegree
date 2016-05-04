# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 14:42:54 2016

@author: Adam
"""

import requests
from bs4 import BeautifulSoup
import csv

filedir = 'C:\Users\Adam\Udacity\Data_Analyst_Nanodegree\Project_4'
tables = ['https://docs.google.com/spreadsheets/d/1OKEv_W69y5e8meJU4tHF-j9e_RkvUZEN66rcao5gpug/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1vzFK2lXYco024CPVpMBgftjtWkyYrjtenowCdgFW7PE/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1jqwTPRgiejcWjnR8bm8YSMQ9MZwPzgqNzyGqYpvjiMk/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1CNYYA9-T01NMo9NiiIbeSizfQd5R2nDCo_DA2YEuRNY/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1fIgxmCM-JhaYWiqydugcbKJW9Cqq_Lm9wJCxdugB_v4/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1lYqKF0rCOKbUzEpySyMuZiHEb6aKgykE_G-F4B2UtXU/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/17Yg3GCGwLla1XT22R2TZkmAW8RbNfARMUKLMRFAIEGk/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/12nAZPVGXHLqCxocRdOwrqDxoDjiC0_6E0LijogPwGCk/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/18qpHBu9MQkzUJtf0Os4CqruqUS6qH0RZMoxWpk1rMKw/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1WForHrbQjormaMR7AaKnwNh8_AHLyw5uRc0nWgXt2mE/pubhtml/sheet?headers=false&gid=484887406']

with open('2015_nfl_sparq.csv', 'wb') as f:
    # iterate through google spreadsheets    
    for page in tables:
        r = requests.get(page)
        soup = BeautifulSoup(r.text, 'lxml')
        
        iter = csv.writer(f, dialect = 'excel')
        
        # write header
        iter.writerow(['name', 'pos', 'age', 'height', 'weight', 'forty_yard',
                       'shuttle', 'vertical_jump', 'bench_press', 'psqarq'])
                       
        table = soup.find('tbody')
        for row in table.find_all('tr'):
            tds = row.find_all('td')
            if tds[1].get_text() == 'Name':
                pass
            else:
                try:
                    age = str(tds[4].get_text())                    
                    name = str(tds[1].get_text())
                    pos = str(tds[2].get_text())
                    height = str(tds[7].get_text())
                    weight = str(tds[8].get_text())
                    forty_yard = str(tds[18].get_text())
                    shuttle = str(tds[21].get_text())
                    vertical_jump = str(tds[24].get_text())
                    bench_press = str(tds[23].get_text())
                    psparq = str(tds[9].get_text())
                except:
                    print 'Merged row'
                    continue                
                
            iter.writerow([name, pos, age, height, weight, forty_yard, 
                           shuttle, vertical_jump, bench_press, psparq])
                           
f.close()        
        
     