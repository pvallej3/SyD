


import pyglet
from pyglet.gl import *

import math

def vec(*args):
	return (GLfloat * len(args))(*args)




def id(x):
	return x

def triplet(chaine):
	coords = chaine.split()
	return (float(coords[0]), float(coords[1]), float(coords[2])) 

def quadruplet(chaine):
	coords = chaine.split()
	return (float(coords[0]), float(coords[1]), float(coords[2]), float(coords[3])) 

def getVal(attrs,fconv, nom,defaut):
	if attrs.has_key(nom):
		return fconv(attrs[nom])
	else:
		return defaut

def deg2rad(d):
	return math.pi*d/180.0
