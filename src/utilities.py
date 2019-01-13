import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo

def xmlTag(xml, tag):
	return xml.getElementsByTagName(tag)[0].firstChild.nodeValue

def xmlAttrib(xml, tag, attrib):
	return xml.getElementsByTagName(tag)[0].getAttribute(attrib)


def filterText(text):
	printable = set(string.printable)
	return "".join(list(filter(lambda x: x in string.printable, text)))

def getStats (xml, name):
	average = xmlAttrib(xml, 'average', 'value')
	bayesaverage = xmlAttrib(xml, 'bayesaverage', 'value')
	minplaytime = xmlAttrib(xml, 'stats', 'minplaytime')
	maxplaytime = xmlAttrib(xml, 'stats', 'maxplaytime')
	minplayers = xmlAttrib(xml, 'stats', 'minplayers')
	maxplayers = xmlAttrib(xml, 'stats', 'maxplayers')
	id = xml.getAttribute('objectid')

	return {'name':name,
			'average':float(average),
			'bayesaverage':float(bayesaverage),
			'minplaytime':int(minplaytime),
			'maxplaytime':int(maxplaytime),
			'minplayers':int(minplayers),
			'maxplayers':int(maxplayers),
			'id':int(id)}