from xml.dom.minidom import parse, parseString
import string
import pymongo

import utilities as util

def getStats (xml, name):
    average = util.xmlAttrib(xml, 'average', 'value')
    bayesaverage = util.xmlAttrib(xml, 'bayesaverage', 'value')
    minplaytime = util.xmlAttrib(xml, 'stats', 'minplaytime')
    maxplaytime = util.xmlAttrib(xml, 'stats', 'maxplaytime')
    minplayers = util.xmlAttrib(xml, 'stats', 'minplayers')
    maxplayers = util.xmlAttrib(xml, 'stats', 'maxplayers')
    id = xml.getAttribute('objectid')

    return {'name':name,
            'average':float(average),
            'bayesaverage':float(bayesaverage),
            'minplaytime':int(minplaytime),
            'maxplaytime':int(maxplaytime),
            'minplayers':int(minplayers),
            'maxplayers':int(maxplayers),
            'id':int(id)}
