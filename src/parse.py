from xml.dom import minidom
import misc
import grapheScene as gs
import annuaire

def getAttributs(node):
	attributs = node.attributes
	res = {}
	for cle in attributs.keys():
		attr = attributs[cle]
		res[cle] = attr.value
	return res 

def parse(node,unAnnuaire):

	nomBalise = node.tagName
	attributs = getAttributs(node)
	lesFils = [parse(e,unAnnuaire) for e in node.childNodes if e.nodeType==e.ELEMENT_NODE]
	
	print "La balise : ", nomBalise
	print "Les fils : ", lesFils
	print "Les attributs : ", attributs
	print "==============================================================="

	
	if nomBalise == "Scene" : 
		valeurLook = misc.getVal(attributs,misc.triplet,"look",(10.0,1.6,0.0))
		valeurAngle = misc.getVal(attributs,float,"dir",0.0)
		valeurUp = misc.getVal(attributs,misc.triplet,"up",(0.0,1.0,0.0))
		objet =  gs.Scene(fils=lesFils,look=valeurLook,angle=valeurAngle,up=valeurUp)

	elif nomBalise == "SkyBox" : 
		valeurTexture = misc.getVal(attributs,str,"texture","../data/skyboxes/miramar_large.jpg")
		valeurSize = misc.getVal(attributs,float,"size",500)
		objet = gs.SkyBox(texture=valeurTexture,size=valeurSize)

	elif nomBalise == "Obj" : 
		valeurUrl = misc.getVal(attributs,str,"url","../data/obj/porte1.obj")
		objet = gs.Obj(url=valeurUrl)

	elif nomBalise == "Transform" : 
		vT = misc.getVal(attributs,misc.triplet,"translation",(0.0,0.0,0.0))
		vR = misc.getVal(attributs,misc.triplet,"rotation",(0.0,0.0,0.0))
		vE = misc.getVal(attributs,misc.triplet,"echelle",(1.0,1.0,1.0))
		objet = gs.Transform(lesFils,translation=vT,rotation=vR,echelle=vE)

	elif nomBalise == "DisplayList" : 
		objet = gs.DisplayList(lesFils)

	elif nomBalise == "Tableau" : 
		valeurTexture = misc.getVal(attributs,str,"texture","../data/skyboxes/miramar_large.jpg")
		valeurHauteur = misc.getVal(attributs,float,"hauteur",1.0)
		valeurLargeur = misc.getVal(attributs,float,"largeur",1.0)
		objet = gs.Tableau(valeurLargeur, valeurHauteur, valeurTexture)

	elif nomBalise == 'Sol' :
		valeurTaille = misc.getVal(attributs,float,"taille",100.0)
		valeurTexture = misc.getVal(attributs,str,"texture","../data/textures/sol.png")
		objet = gs.Sol(texture=valeurTexture, taille=valeurTaille)

	
	if attributs.has_key('name'):
		unAnnuaire.ajouter(attributs['name'],objet)

	return objet

def parser(nomFichier, annuaire):
	fichier = open(nomFichier)
	xmldoc = minidom.parse(fichier)
	#print xmldoc.toxml()
	fichier.close()

	print '\n\n'

	racine = xmldoc.childNodes[0]

	return parse(racine, annuaire)	

if __name__ == "__main__":
	fichier = open('scene.xml')
	xmldoc = minidom.parse(fichier)
	#print xmldoc.toxml()
	fichier.close()

	print '\n\n'

	racine = xmldoc.childNodes[0]

	parse(racine)

