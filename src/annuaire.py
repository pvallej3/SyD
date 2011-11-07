
class Annuaire : 

	def __init__(self):
		self.annuaire = {}

	def ajouter(self,nom,valeur):
		
		if self.annuaire.has_key(nom):
			return None
		else:
			self.annuaire[nom] = valeur
			return nom

	def chercher(self,nom):
		if not self.annuaire.has_key(nom):
			return None
		else:
			return self.annuaire[nom]
	
