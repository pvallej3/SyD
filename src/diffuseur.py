
import socket, sys, threading

#host = '127.0.0.1'
#port = 50000

class ThreadClient(threading.Thread):
	def __init__(self,conn,conn_clients,annuaire):
		threading.Thread.__init__(self)
		self.connexion = conn
		self.conn_clients = conn_clients
		self.annuaire = annuaire

	def send(self,msg):
		self.connexion.send(msg)

	def concatener(self,listeDeMots):
		res = ""
		for mot in listeDeMots :
			res = res + " " + mot
		return res
		

	def run(self):

		encore = True

		while encore : 
			msgClient = self.connexion.recv(1024)
			if msgClient.upper() == 'FIN' : 
				encore = False
				break

			print "[1] ", msgClient

			tokens = msgClient.split()
			if len(tokens) == 0 :
				pass
			elif tokens[0] == 'ID' :
				print "ID = " + tokens[1]  
				self.annuaire[tokens[1]] = self

			else:
				for client in self.annuaire.values() : 
					if client != self:
						client.send(msgClient)

		# Fermeture de la connexion
		self.connexion.close()
		del self.conn_clients[nom]
		print "Client %s deconnecte" % nom
		sys.exit(0)

 


class Serveur : 
	def __init__(self,host='127.0.0.1',port=50000):

		print "Hote : %s - Port : %d \n" % (host,port)

		self.conn_clients = {}

		self.annuaire = {}



		mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			mySocket.bind((host,port))
		except socket.error:
			print "Echec de la connexion"
			sys.exit()
		print "Serveur pret en attente de requete"
		mySocket.listen(10)

		while 1 :
			connexion, adresse = mySocket.accept()


			th = ThreadClient(connexion,self.conn_clients,self.annuaire)
			th.start()
			it = th.getName()
			
			self.conn_clients[it] = connexion
			
			print "Client %s connecte, adresse IP %s, port %s" % (it,adresse[0], adresse[1])
			# Dialogue avec le client
			connexion.send("OK")

	

if __name__ == "__main__" : 
	print sys.argv
	if len(sys.argv)==2 :
		port = int(sys.argv[1])
	else:
		port = 50000
	leserveur = Serveur(port=port)

