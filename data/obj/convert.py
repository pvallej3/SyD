


sommets  = []
normales = []
textures = []
faces = []
groupes = {}
nomGroupe = ''

def lireSommet(l):
    global sommets
    x = float(l[1])
    y = float(l[2])
    z = float(l[3])
    sommets.append((x,y,z))

def lireNormale(l):
    global normales
    nx = float(l[1])
    ny = float(l[2])
    nz = float(l[3])
    normales.append((nx,ny,nz))


def lireCoordsTextures(l):
    global textures
    s = float(l[1])
    t = float(l[2])
    textures.append((s,t))

def lireFaces(l):
    global faces
    l1 = [s.split('/') for s in l[1:len(l)]]
    uneFace = []
    for sommet in l1:
        uneFace.append([int(i)-1 for i in sommet])
          
    
    faces.append(uneFace)

def lireGroupes(l):
    pass


def lire_fichier(nomFicIn):
    f = open(nomFicIn,"r")
    for ligne in f :
        l = ligne.split()
        if l == [] :
            pass
        else:
            if   l[0] == 'v'  : lireSommet(l)
            elif l[0] == 'vn' : lireNormale(l)
            elif l[0] == 'vt' : lireCoordsTextures(l)
            elif l[0] == 'f'  : lireFaces(l)
            elif l[0] == 'g'  : lireGroupes(l)
            else:               pass
    f.close()

def ecrire_scheme(nomFicOut,faces, sommets, normales,textures):
	pass

lire_fichier('venus.obj')

print faces
