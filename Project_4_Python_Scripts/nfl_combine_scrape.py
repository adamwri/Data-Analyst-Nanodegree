# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:41:12 2016

@author: Adam
"""

import requests
from bs4 import BeautifulSoup
import csv

query = {'year': 'all'}
r = requests.get('http://nflcombineresults.com/nflcombinedata.php',
                 params = query)

soup = BeautifulSoup(r.text, 'lxml')

f = csv.writer(open('nfl_combine.csv', 'wb'), dialect = 'excel')

# write column headers
f.writerow(['year', 'name', 'college', 'pos', 'height', 'weight',
            'wonderlic', 'forty_yard', 'bench_press', 'vert_leap', 
            'broad_jump', 'shuttle', 'three_cone'])

table = soup.find('tbody')

for row in table.find_all('tr'):
    tds = row.find_all('td')
    
    year = str(tds[0].get_text())
    name = str(tds[1].get_text())
    college = str(tds[2].get_text())
    pos = str(tds[3].get_text())
    height = str(tds[4].get_text())
    weight = str(tds[5].get_text())
    wonderlic = str(tds[6].get_text())
    forty_yard = str(tds[7].get_text())
    bench_press = str(tds[8].get_text())
    vert_leap = str(tds[9].get_text())
    broad_jump = str(tds[10].get_text())
    shuttle = str(tds[11].get_text())
    three_cone = str(tds[12].get_text())
    
    f.writerow([year, name, college, pos, height, weight, wonderlic,
                forty_yard, bench_press, vert_leap, broad_jump, shuttle,
                three_cone])


    
