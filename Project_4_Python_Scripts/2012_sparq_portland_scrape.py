# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 14:39:31 2016

@author: Adam
"""

import requests
from bs4 import BeautifulSoup
import csv

filedir = 'C:\Users\Adam\Udacity\Data_Analyst_Nanodegree\Project_4'

with open('2012_sparq_portland.csv', 'wb') as f:
    
    iter = csv.writer(f, dialect = 'excel')
    # write header
    iter.writerow(['name', 'pos', 'height', 'weight', 'forty_yard',
                       'shuttle',' vertical_jump', 'powerball', 'sparq'])
                       
    for i in range(1, 13):
        query = {'page': i}
        r = requests.get('http://espn.go.com/high-school/football/events/nike-sparq-combines/2012/portland/results/_/id/110',
                      params = query)

        print r.url
        soup = BeautifulSoup(r.text, 'lxml')      
    
        for tr in soup.find_all('table')[1].find_all('tr'):
            tds = tr.find_all('td')
            if tds[1].get_text() == 'NAME':
                pass
            else:
                name = str(tds[1].get_text())
                pos = str(tds[4].get_text())
                height = str(tds[5].get_text())
                weight = str(tds[6].get_text())
                forty_yard = str(tds[7].get_text())
                shuttle = str(tds[8].get_text())
                vertical_jump = str(tds[9].get_text())
                powerball = str(tds[10].get_text())
                sparq = str(tds[11].get_text())
                
                iter.writerow([name, pos, height, weight, forty_yard,
                            shuttle, vertical_jump, powerball, sparq]) 

f.close()