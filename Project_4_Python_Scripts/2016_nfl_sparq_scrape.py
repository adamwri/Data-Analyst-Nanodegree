# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 12:20:30 2016

@author: Adam
"""

import requests
from bs4 import BeautifulSoup
import csv

filedir = 'C:\Users\Adam\Udacity\Data_Analyst_Nanodegree\Project_4'
tables = ['https://docs.google.com/spreadsheets/d/1TceHPBxiz4UuOimkjptJueF5kMd5BdKoQ5Jw0oVRAH8/pubhtml?gid=484887406&amp;single=true&amp;widget=true&amp;headers=false',
          'https://docs.google.com/spreadsheets/d/1ga52s93wr85K6QZ7nW-YfpDjd8-FptzUsdeDW7qKUmI/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1iFATWc8mI5pKrz0LXdOY5E5OcK7ddpQBbLlUla_0zeY/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1AvYH2WVnnMlMVOVzL1cu81qAjDx1U0KgNerc1Ya_jdw/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1X1YOfu9_wf60BK9PTz9DELRY1hicvO_7UmDQhUnaSk4/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/10jLy0OqhvuMlT713Wj97EGWXds1cYLK1eki72h5c4L0/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1myQgX_afsqGaqA5J6f1af3XI-SnxZHFsjUNo9vicmng/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1BTwSvBUvT5OOi1kSVzZU0smJSuQ0VIb6aqmZTSq7nLQ/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1p-fTG6zAvxJEiN_RynhH2qCjKQg_AKyb2n3oLM5qEmk/pubhtml/sheet?headers=false&gid=484887406',
          'https://docs.google.com/spreadsheets/d/1uedO4wFW-THujdmrTdkXViUhlMWHWvWn20QUIRNCZ5w/pubhtml/sheet?headers=false&gid=484887406']

with open('2016_nfl_sparq.csv', 'wb') as f:
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
                    height = str(tds[6].get_text())
                    weight = str(tds[7].get_text())
                    forty_yard = str(tds[17].get_text())
                    shuttle = str(tds[20].get_text())
                    vertical_jump = str(tds[23].get_text())
                    bench_press = str(tds[22].get_text())
                    psparq = str(tds[8].get_text())
                except:
                    print 'Merged row'
                    continue                
                
            iter.writerow([name, pos, age, height, weight, forty_yard, 
                           shuttle, vertical_jump, bench_press, psparq])
                           
f.close()    
 