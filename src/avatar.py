


import grapheScene as gs


class Avatar :

	def __init__(self,url=None,position=(0.0,0.0,0.0),orientation=0.0,vitesse=0.0):
		if url != None :
			self.model = gs.Transform(fils=[gs.Obj(url=url)], translation=position, rotation=(0.0,orientation,0.0),echelle=(1.0,1.0,1.0))
		self.position=position
		self.orientation=orientation
		self.vitesse=vitesse

	def setPosition(self,position):
		self.position=position

	def setOrientation(self,orientation):
		self.orientation = orientation

	def setVitesse(self,vitesse):
		self.vitesse = vitesse

	def draw(self):
		if self.model != None :
			self.model.draw()

	def update(self,dt):
		if self.model != None :
			r = 0.0, self.orientation, 0.0
			self.model.setTranslation(self.position)
			self.model.setRotation(r)

class Avatars : 

	def __init__(self):
		self.annuaire = {}

	def draw(self):
		for avatar in self.annuaire.values() :
			avatar.draw() 
			
	def membre(self,nom):
		return self.annuaire.has_key(nom)
 
	def fromName(self,nom):
		if self.annuaire.has_key(nom):
			return self.annuaire[nom]
		else:
			return None

	def ajouter(self,nom,unAvatar):
		if not self.annuaire.has_key(nom):
			self.annuaire[nom] = unAvatar
			return unAvatar
		else:
			return self.annuaire[nom]

	def update(self,dt):
		pass 
			
