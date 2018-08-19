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



