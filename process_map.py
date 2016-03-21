# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 14:40:45 2016

@author: Adam
"""
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from improve_streets import update_name, is_street_name

file_in = 'santa-cruz_california.osm'

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POS = ['lat', 'lon']


def shape_element(element):
    node = {}
    if element.tag == 'node' or element.tag == 'way':
        created = {}
        for e in element.attrib.keys():
        # cycle through keys of each element
            if e in CREATED:
                created[e] = element.attrib[e]
            elif element.attrib[e] == element.get('lat') or element.attrib[e] == element.get('lon'):
                # populate pos list with lat and lon
                pos = []
                pos.append(float(element.get('lat')))
                pos.append(float(element.get('lon')))
                node['pos'] = pos
            else:
                node[e] = element.get(e)                
                
        node['type'] = element.tag
        node['created'] = created            

        node_refs = []
        address = {}
        for subtag in element:
            if subtag.tag == 'tag':
                # if tag has problem characters ignore
                if re.search(problemchars, subtag.get('k')):
                    continue
                # if tag structure is word:word:word ignore
                elif re.search(r'\w+:\w+:\w+', subtag.get('k')):
                    continue
                # ignore tags with 'tiger:' as key
                elif subtag.get('k').startswith('tiger:'):
                    continue
                # ignore tags with 'gnis:' as key
                elif subtag.get('k').startswith('gnis:'):
                    continue
                # add and fix streets if a street; add all address keys, values to address dictionary
                elif subtag.get('k').startswith('addr:'):
                    key = subtag.get('k')[5:]
                    if key == 'street':
                        address[key] = update_name(subtag.get('v'))
                    if key == 'postcode':
                        address[key] = re.sub(r'\D', '', subtag.get('v'))[:5]
                    else:
                        address[key] = subtag.get('v')
                        node['address'] = address
                else:
                    node[subtag.get('k')] = subtag.get('v')
            # if tag nd append refs to node_refs list
            else:
                if subtag.tag == 'nd':
                    node_refs.append(subtag.get('ref'))                    
                else:
                    pass
        # add node_refs list to node dictionary
        if node_refs:
            node['node_refs'] = node_refs
            
        return node
    else:
        return None

def process_map(file_in, pretty = False):
    # Process .osm file and output .json to load into MongoDB
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

process_map(file_in, pretty = False)