
import socket, sys, threading
from collections import deque

class ThreadReception(threading.Thread):
	def __init__(self,conn,observateur,verrou):
		threading.Thread.__init__(self)
		self.connexion = conn
		self.observateur = observateur
		self.verrou = verrou


	def run(self):
		while 1 :
			message_recu = self.connexion.recv(1024)
		 	if message_recu != None :
				print "Message recu : " + message_recu
			else:
				print "-"
			if message_recu == '' or message_recu.upper() == 'FIN' :
				break
			self.observateur.verrou.acquire()
			self.observateur.recevoir(message_recu)
			self.observateur.verrou.release()
		print "Interruption de connexion"
		self.connexion.close()


class Connexion : 
	
	def __init__(self,host='127.0.0.1',port=50000):
		self.verrou = threading.Lock()
		self.horloge = 0.0
		self.lesCommandes = deque([])
		self.nbMessages = 0


		self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.connexion.connect((host,port))
		except socket.error :
			print "La connexion a echouee"
			sys.exit()
		print "Connexion etablie avec le serveur"

		self.thReception = ThreadReception(self.connexion,self,self.verrou)

		self.thReception.start()



	def emettre(self,message):
		self.connexion.send(message)

	def recevoir(self,uneCommande):
		self.lesCommandes.append(uneCommande)
		self.nbMessages = self.nbMessages + 1

	def consulter(self):
		self.verrou.acquire()
		if self.nbMessages>0 : 
			message = self.lesCommandes.pop()
			self.nbMessages = self.nbMessages - 1
		else:
			message = None
		self.verrou.release()
		return message
		



