import math

class Vec3:

	def __init__(self,x=0.0,y=0.0,z=0.0):
		self.x = x
		self.y = y
		self.z = z

	def __repr__(self):
		return "<%f %f %f" % (self.x, self.y, self.z) 

	def setCoordonnees(self,x=0.0,y=0.0,z=0.0):
		self.x = x
		self.y = y
		self.z = z

	def getCoordonnees(self):
		return self.x, self.y, self.z

	def soit(self,v):
		self.x = v.x
		self.y = v.y
		self.z = v.z

	def vers(self,de,a):
		self.x = a.x - de.x
		self.y = a.y - de.y
		self.z = a.z - de.z

	def moins(self,u,v):
		self.x = u.x - v.x
		self.y = u.y - v.y
		self.z = u.z - v.z


	def accumuler(self,k,v):
		self.x += k*v.x
		self.y += k*v.y
		self.z += k*v.z

	def scale(self,k):
		self.x *= k
		self.y *= k
		self.z *= k

	def oppose(self):
		self.x = - self.x
		self.y = - self.y
		self.z = - self.z

	def produitVectoriel(self,u,v):
		self.x = u.y*v.z - u.z*v.y
		self.y = u.z*v.x - u.x*v.z
		self.z = u.x*v.y - u.y*v.x

	def distance(self,v):
		x,y,z = v.getCoordonnees()
		return math.sqrt((self.x-x)*(self.x-x)+(self.y-y)*(self.y-y)+(self.z-z)*(self.z-z))

	def norme(self):
		l = math.sqrt(self.x*self.x + \
                              self.y*self.y + \
                              self.z*self.z)
		return l

	def normer(self):
		l = self.norme()
		self.scale(1.0/l)

	def tronquer(self,lmax):
		l = self.norme()
		if l > lmax:
			self.scale(lmax/l)

if __name__ == "__main__" :
	v = Vec3(x=3.0,y=2.0,z=1.0)
	print v
