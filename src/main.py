#! /usr/bin/python

import pyglet
from pyglet.gl import *

import math
import sys


import camera
import parse
import reseau
import contexte
import vec3



leContexte = None


try:
	config = Config(sample_buffer=1, samples=4, \
          depth_size=16, double_buffer=True)
	window = pyglet.window.Window(resizable=True, config=config)
except:
	window = pyglet.window.Window(resizable=True)

def setup():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)
	glAlphaFunc(GL_GREATER,0.4)
	glEnable(GL_ALPHA_TEST)

def init():
	global leContexte
	setup()
	leContexte = contexte.Contexte(sys.argv[1],"../data/scene.xml")

	# Test de comportement d'agents
	#contexte.testComportement(leContexte)


@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50.0, width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
	global scene
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glClearColor(1.0,1.0,1.0,1.0)

	glColor3f(1.0,0.0,0.0)

	leContexte.draw()

@window.event
def on_key_press(symbol,modifiers):
	if symbol == pyglet.window.key.Q:
		pass
	elif symbol == pyglet.window.key.LEFT : # Fleche gauche 
		leContexte.camera.enArriere()
	elif symbol == pyglet.window.key.RIGHT : # Fleche droite 
		leContexte.camera.enAvant()
	elif symbol == pyglet.window.key.UP : # Fleche haut
		leContexte.camera.accelerer(0.5)
	elif symbol == pyglet.window.key.DOWN : # fleche bas
		leContexte.camera.deccelerer(0.5)
	elif symbol == pyglet.window.key.SPACE :
		leContexte.camera.pilerSurPlace()


@window.event
def on_mouse_press(x,y,bouton,modifiers):
	pass


@window.event
def on_mouse_drag(x,y,dx,dy,boutons,modifiers):
	#print x, " ", y, " ", dx, " ", dy
	leContexte.camera.rotationCamera(dx)
	leContexte.camera.rotationCameraY(dy)

@window.event
def on_mouse_motion(x, y, dx, dy):
	print ">> ", x, y

def update(dt):
	leContexte.update(dt)
	#messageRecu = leContexte.connexionPrincipale.consulter()
	#if messageRecu != None :
		#print "MESSAGE : ", messageRecu


def updateLent(dt):
	leContexte.updateLent(dt)
	#messageRecu = leContexte.connexionPrincipale.consulter()
	#if messageRecu != None :
	#	print "MESSAGE : ", messageRecu
	




if __name__ == '__main__' : 
	print "Hello World"

	init()
	# La fonction update sera appelee toutes les 30eme de seconde
  #       pyglet.clock.schedule_interval(update, 1.0/30.0)
	pyglet.clock.schedule_interval(updateLent, 1.0)


	pyglet.app.run()


