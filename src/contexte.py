
import annuaire
import parse
import camera
import reseau
import avatar

class Contexte :
	
	def __init__(self,nomUtilisateur,nomFichier):
		self.id = nomUtilisateur
		self.horloge = 0.0
		self.annuaire = annuaire.Annuaire()
		self.scene = parse.parser(nomFichier, self.annuaire)

		self.camera = camera.Camera(scene=self.scene)
		look, angle, up = self.scene.getLookAt()
		self.camera.setLookAt(look,angle,up)

		self.avatars = avatar.Avatars()
		unAvatar = avatar.Avatar(url="../data/obj/penguin.obj")
		self.avatars.ajouter("pingouin",unAvatar)

		# init de la connexion reseau
		self.connexionPrincipale = reseau.Connexion(host='127.0.0.1',port=50000)
		self.connexionPrincipale.emettre("ID %s" % (self.id))

	def getTime(self):
		return self.horloge

	def draw(self):
		self.avatars.draw()
		self.scene.draw()
		
	def update(self,dt):
		self.horloge = self.horloge + dt
		self.camera.update(dt)
		self.connexionPrincipale.emettre("Bonjour je suis %s" % (self.id))
		msg = self.connexionPrincipale.consulter()
		if msg != None :
			print "--> ", msg
			
	def updateLent(self,dt):
		self.horloge = self.horloge + dt
		self.camera.update(dt)
		self.connexionPrincipale.emettre("Status id = %s, position = %s, orientation = %s, speed = %s" % (self.id, self.camera.positionOeil,self.camera.directionVisee, self.camera.vitesseOeil))
		msg = self.connexionPrincipale.consulter()
		if msg != None :
			#print "--> ", msg
			self.createAvatar(msg)
			
	def createAvatar(self,msg):
		if msg.startswith("Status"):
			tmp=msg.split('=')
			#Hacerlo mas dinamico sin los indices
			name=tmp[1].split(',',1)
			print "name", name
			position=tmp[2].split(',',1)
			print "position",position
			orientation=tmp[3].split(',',1)
			print "orit", orientation
			vitesse=tmp[4]
			print "vitesse", vitesse
			#unAvatar=self.avatars.fromName(name)
			#if unAvatar != None :
				#unAvatar.setPosition(position)
				#unAvatar.setOrientation(orientation)
				#unAvatar.setVitesse(vitesse)
			#else :
				#unAvatar=avatar.Avatar(url="../data/obj/penguin.obj",position=position,orientation=orientation, vitesse=vitesse)
				#self.avatars.ajouter(name,unAvatar)
		else:
			pass



def testComportement(unContexte):
	unAgent = agents.Agent(unContexte)
	unAgent.setNomForme("guide",unContexte)
	unContexte.agents.ajouter("le_guide",unAgent)
	
	
