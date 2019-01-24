import numpy as np
from requests import get
from xml.dom.minidom import parse, parseString
import string
import pymongo
import random
from src.main import db

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


	if (minplaytime == ''): minplaytime = 0


	return {'name':name,
			'average':float(average),
			'bayesaverage':float(bayesaverage),
			'minplaytime':int(minplaytime),
			'maxplaytime':int(maxplaytime),
			'minplayers':int(minplayers),
			'maxplayers':int(maxplayers),
			'id':int(id)}

def idToName(gameID):
	nameObj = db.Games.find_one({'id':gameID}, {'name':1})

	return nameObj['name']

def mapRange(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class WeightedList:


	#list needs to be [{e:Element, w:weight},...]
	def __init__(self,list):
		self.list = list
		self.totalWeight = 0
		self.fullNorm()


	def remove(self,index):
		self.list.remove(index)
		self.shortNorm(elem['w'])

	def get(self,index):
		return self.list[index]['e']

	def push(self, elem):
		self.list.append(elem)
		self.shortNorm(elem['w'])

	def fullNorm(self):
		for elem in self.list:
			self.totalWeight += elem['w']
		for elem in self.list:
			elem['w'] = elem['w']/self.totalWeight

	def shortNorm(self, weight):
		for elem in self.list:
			elem['w'] = elem['w']*self.totalWeight
		self.totalWeight += weight
		for elem in self.list:
			elem['w'] = elem['w']/self.totalWeight



	#Returns random element from list based on weighting
	def random(self):
		index = random.random()
		sum = 0
		for elem in self.list:
			sum += elem['w']
			if(sum > index):
				return elem['e']
