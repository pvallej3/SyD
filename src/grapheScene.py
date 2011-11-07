import math
import vec3
import misc
import wavefront

import pyglet
from pyglet.gl import *



class CatalogueTextures : 

	def __init__(self):
		self.catalogue = {}

	def chargerTexture(self,nom):

		if self.catalogue.has_key(nom):
			return self.catalogue[nom]
		else:
			image = pyglet.image.load(nom)
			print ">>>>> TEXTURE ", nom, " CHARGEE"
			texture = image.get_texture()
			glBindTexture(GL_TEXTURE_2D,texture.id)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
			glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
			self.catalogue[nom] = texture
			return texture

catalogueTextures = CatalogueTextures()

class Node : 
	def __init__(self):
		pass

	def draw(self):
		pass



class Obj(Node):
	def __init__(self,url=None):
		self.url = url
		self.model = wavefront.WavefrontModel()
		self.model.LoadFile(self.url)

	def draw(self):
		self.model.Draw()


class Scene : 

	def __init__(self,fils,**attributs):
		self.lesFils = fils
		self.look = attributs['look']
		self.angle = attributs['angle'] 
		self.angle = self.angle * math.pi / 180.0
		self.up = attributs['up']

	def __call__(self):
		return self.lesFils

	def lookAt(self,look,angle, up):
		self.look = look
		self.angle = angle
		self.up = up

	def getLookAt(self):
		return (self.look,self.angle,self.up)

	def append(self,x):
		self.lesFils.append(x)

	def draw(self):
		x1, y1, z1 = self.look
		x2, y2, z2 = x1 + math.cos(self.angle), y1, z1 + math.sin(self.angle)
		x3, y3, z3 = self.up

		glLoadIdentity()
		gluLookAt(x1,y1,z1,x2,y2,z2,x3,y3,z3)

		for fils in self.lesFils : 
			fils.draw()

	

class Group(Node):

	def __init__(self,fils=[]):
		Node.__init__(self)
		self.fils = fils

	def draw(self):
		for f in self.fils:
			f.draw()

class DisplayList:

	def __init__(self,fils):
		self.lesFils = fils
		self.displayListID = None

	def draw(self):
		if self.displayListID == None :
			self.displayListID = glGenLists(1)
			glNewList(self.displayListID, GL_COMPILE)
			for obj in self.lesFils : 
				obj.draw()
			glEndList()
		else:
			glCallList(self.displayListID)


class Transform :

	def __init__(self,fils=[],**attributs):
		self.fils = fils
		tx, ty, tz = attributs['translation']
		rx, ry, rz = attributs['rotation']
		sx, sy, sz = attributs['echelle']

		self.tx = tx
		self.ty = ty
		self.tz = tz

		self.rx = rx
		self.ry = ry
		self.rz = rz

	def setTranslation(self,t):
		self.tx, self.ty, self.tz = t

	def setRotation(self,r):
		self.rx, self.ry, self.rz = r

	def setTx(self,v):
		self.tx = v

	def setTy(self,v):
		self.ty = v

	def setTz(self,v):
		self.tz = v

	def setRx(self,v):
		self.rx = v

	def setRy(self,v):
		self.ry = v

	def setRz(self,v):
		self.rz = v

	def draw(self):

		

		glPushMatrix()		
		glTranslatef(self.tx, self.ty, self.tz)
		glRotatef(self.ry,0.0,1.0,0.0)

		for f in self.fils : 
			f.draw()

		glPopMatrix()


class SkyBox :
        def __init__(self,texture=None,size=500):
                self.size = size
                textureName = texture
                image = pyglet.image.load(textureName)
                print ">>>>> TEXTURE ", textureName, " LOADED"
                imageSeq = pyglet.image.ImageGrid(image, 3, 4)
                self.textureUP = imageSeq[9].get_texture()
                self.textureDN = imageSeq[1].get_texture()
                self.textureLT = imageSeq[4].get_texture()
                self.textureFT = imageSeq[5].get_texture()
                self.textureRT = imageSeq[6].get_texture()
                self.textureBK = imageSeq[7].get_texture()
                print ">>>>> TEXTURE ", textureName, " SPLIT"
                self.textureFactor = 1.0	
	
        def draw(self):
                size = self.size
                halfsize = (size/2)
                halfsizec = halfsize*1.01 #halfsize corrected
                tf = self.textureFactor
        
                # Up
                glBindTexture(GL_TEXTURE_2D,self.textureUP.id)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0,0.0)
                glVertex3f(-halfsizec,halfsize,-halfsizec)
                glTexCoord2f(1.0,0.0)
                glVertex3f(halfsizec,halfsize,-halfsizec)
                glTexCoord2f(1.0,1.0)
                glVertex3f(halfsizec,halfsize,halfsizec)
                glTexCoord2f(0.0,1.0)
                glVertex3f(-halfsizec,halfsize,halfsizec)
                glEnd()
                # Down
                glBindTexture(GL_TEXTURE_2D,self.textureDN.id)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0,0.0)
                glVertex3f(-halfsizec,-halfsize,halfsizec)
                glTexCoord2f(1.0,0.0)
                glVertex3f(halfsizec,-halfsize,halfsizec)
                glTexCoord2f(1.0,1.0)
                glVertex3f(halfsizec,-halfsize,-halfsizec)
                glTexCoord2f(0.0,1.0)
                glVertex3f(-halfsizec,-halfsize,-halfsizec)
                glEnd()
                # Left
                glBindTexture(GL_TEXTURE_2D,self.textureLT.id)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0,0.0)
                glVertex3f(-halfsize,-halfsizec,halfsizec)
                glTexCoord2f(1.0,0.0)
                glVertex3f(-halfsize,-halfsizec,-halfsizec)
                glTexCoord2f(1.0,1.0)
                glVertex3f(-halfsize,halfsizec,-halfsizec)
                glTexCoord2f(0.0,1.0)
                glVertex3f(-halfsize,halfsizec,halfsizec)
                glEnd()
                # Front
                glBindTexture(GL_TEXTURE_2D,self.textureFT.id)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0,0.0)
                glVertex3f(-halfsizec,-halfsizec,-halfsize)
                glTexCoord2f(1.0,0.0)
                glVertex3f(halfsizec,-halfsizec,-halfsize)
                glTexCoord2f(1.0,1.0)
                glVertex3f(halfsizec,halfsizec,-halfsize)
                glTexCoord2f(0.0,1.0)
                glVertex3f(-halfsizec,halfsizec,-halfsize)
                glEnd()
                # Right
                glBindTexture(GL_TEXTURE_2D,self.textureRT.id)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0,0.0)
                glVertex3f(halfsize,-halfsizec,-halfsizec)
                glTexCoord2f(1.0,0.0)
                glVertex3f(halfsize,-halfsizec,halfsizec)
                glTexCoord2f(1.0,1.0)
                glVertex3f(halfsize,halfsizec,halfsizec)
                glTexCoord2f(0.0,1.0)
                glVertex3f(halfsize,halfsizec,-halfsizec)
                glEnd()
                # Back
                glBindTexture(GL_TEXTURE_2D,self.textureBK.id)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0,0.0)
                glVertex3f(halfsizec,-halfsizec,halfsize)
                glTexCoord2f(1.0,0.0)
                glVertex3f(-halfsizec,-halfsizec,halfsize)
                glTexCoord2f(1.0,1.0)
                glVertex3f(-halfsizec,halfsizec,halfsize)
                glTexCoord2f(0.0,1.0)
                glVertex3f(halfsizec,halfsizec,halfsize)
                glEnd()




class Tableau : 
	def __init__(self,largeur,hauteur,nomTexture):
		self.largeur = largeur
		self.hauteur = hauteur
		self.texture = catalogueTextures.chargerTexture(nomTexture)
		
	def draw(self):
	
		glPushMatrix()
	
		glScalef(self.largeur/2.0, self.hauteur, 1.0)

		#glDisable(GL_TEXTURE_2D)

		glBindTexture(GL_TEXTURE_2D,self.texture.id)
		glBegin(GL_QUADS)

		# Affichage du recto

	
		glTexCoord2f(0.0, 0.0)
		glVertex3f(-0.5, 0.0, 0.0)
		glTexCoord2f(1.0, 0.0)
		glVertex3f( 0.5, 0.0, 0.0)
		glTexCoord2f(1.0,1.0)
		glVertex3f( 0.5, 1.0, 0.0)
		glTexCoord2f(0.0,1.0)
		glVertex3f(-0.5, 1.0, 0.0)

		glEnd()

	

		glDisable(GL_TEXTURE_2D)	

		glBegin(GL_QUADS)
		
		# Affichage du verso

		glColor3f(1.0,0.0,0.0)
		glVertex3f(-0.5, 0.0, -0.02)
		glVertex3f(-0.5, 1.0, -0.02)
		glVertex3f( 0.5, 1.0, -0.02)
		glVertex3f( 0.5, 0.0, -0.02)

		glColor3f(1.0,1.0,1.0)

		# Cote droit
		glVertex3f(0.5,0.0,0.0)
		glVertex3f(0.5,0.0,-0.02)
		glVertex3f(0.5,1.0,-0.02)
		glVertex3f(0.5,1.0,0.0)

		# Cote gauche
		glVertex3f(-0.5,0.0,0.0)
		glVertex3f(-0.5,1.0,0.0)
		glVertex3f(-0.5,1.0,-0.02)
		glVertex3f(-0.5,0.0,-0.02)

		# Cote haut
		glVertex3f(-0.5, 1.0, 0.0)
		glVertex3f( 0.5, 1.0, 0.0)
		glVertex3f( 0.5, 1.0,-0.02)
		glVertex3f(-0.5, 1.0,-0.02)

		# Cote bas
		glVertex3f(-0.5, 0.0, 0.0) 
		glVertex3f(-0.5, 0.0,-0.02)
		glVertex3f( 0.5, 0.0,-0.02)
		glVertex3f( 0.5, 0.0, 0.0)

		glEnd()

		glEnable(GL_TEXTURE_2D)
		glPopMatrix()


		
class Sol : 
	def __init__(self,**attributs):
		self.taille = attributs['taille']
		nomTexture = attributs['texture']
		self.texture = catalogueTextures.chargerTexture(nomTexture)
		# self.facteurTexture = getVal(attr,float,"facteurTexture",1.0)
	
	def draw(self):

		taille = self.taille
		fz = 1.0
		
		glBindTexture(GL_TEXTURE_2D,self.texture.id)
		glBegin(GL_QUADS)
		glTexCoord2f(0.0,0.0)
		glVertex3f(-taille,0.0,taille)
		glTexCoord2f(taille,0.0)
		glVertex3f(taille,0.0, taille)
		glTexCoord2f(taille,taille)
		glVertex3f(taille,0.0,-taille)
		glTexCoord2f(0.0,taille)
		glVertex3f(-taille,0.0,-taille)
		glEnd()

