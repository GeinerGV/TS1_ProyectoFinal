from pygame import sprite, surface, Color, draw

class CeldasTablero(sprite.Group):
	COLORS = ("#b6c25a", "#afbc54", "brown")
	def __init__(self, sizeCelda, dimension, colors = dict(), estructura = None):
		sprite.Group.__init__(self)
		colors.setdefault("impar", self.COLORS[0])
		colors.setdefault("par", self.COLORS[1])
		colors.setdefault("obs", [self.COLORS[2]])
		self.colores = [colors["par"], colors["impar"], colors["obs"]]
		self.dimension = (dimension[0], dimension[1])
		self.actualizar = False
		self.filas = []
		self.columnas = []
		self.sizeCelda = sizeCelda
		self.estructura = estructura
		celda = None
		for y in range(self.dimension[1]):
			self.filas.append(FilaTablero())
			for x in range(self.dimension[0]):
				if len(self.columnas) < x+1: self.columnas.append(ColumnaTablero())
				if self.estructura == None:
					celda = Celda(self.sizeCelda, pos=(x, y), color=self.colores[(y+x)%2])
				self.add(celda)
				self.filas[y].add(celda)
				self.columnas[x].add(celda)
	
	def getCelda(self, pos):
		for celda in sprite.groupcollide(self.columnas[pos[0]], self.filas[pos[1]], False, False):
			return celda
				
class FilaTablero(sprite.Group):
	pass

class ColumnaTablero(sprite.Group):
	pass

class Celda(sprite.Sprite):
	def __init__(self, base, **kargs):
		sprite.Sprite.__init__(self)
		kargs.setdefault("tipo", 1)
		self.tipo = kargs["tipo"] # 1: habitable, -1: no habitable, 3: serpiente
		if isinstance(base, surface.Surface):
			self.image = base
		else:
			if isinstance(base, (tuple, list)):
				self.image = surface.Surface(base)
			elif isinstance(base, int):
				self.image = surface.Surface((base, base))
			self.image.fill(Color(kargs["color"]))
		self.rect = self.image.get_rect()
		if "pos" in kargs:
			self.rect.move_ip(self.image.get_width()*kargs["pos"][0], self.image.get_height()*kargs["pos"][1])
		self.actualizar = False
	
	def getNext(self, direccion):
		posx, posy = self.getPos()
		siguiente = self
		if direccion == 0: return None
		for grupo in self.groups():
			if (direccion == 1 or direccion == 3) and isinstance(grupo, ColumnaTablero):
				siguientePosY = posy
				for celda in grupo.sprites():
					celdaY = celda.getPos()[1]
					if direccion == 1:
						if celdaY<posy and (siguientePosY>=posy or celdaY>siguientePosY):
							siguiente = celda
							siguientePosY = celdaY
							if siguientePosY + 1 == posy: return siguiente
						elif siguientePosY>=posy and celdaY > siguientePosY:
							siguiente = celda
							siguientePosY = celdaY

					elif celdaY>posy and (siguientePosY<=posy or celdaY<siguientePosY):
							siguiente = celda
							siguientePosY = celdaY
							if siguientePosY - 1 == posy: return siguiente
					elif siguientePosY<=posy and celdaY<siguientePosY:
						siguiente = celda
						siguientePosY = celdaY
				else: return siguiente
			if (direccion==2 or direccion==4) and isinstance(grupo, FilaTablero):
				siguientePosX = posx
				for celda in grupo.sprites():
					celdaX = celda.getPos()[0]
					if direccion == 2:
						if celdaX > posx and (siguientePosX<=posx or celdaX < siguientePosX) :
							siguiente = celda
							siguientePosX = celdaX
							if celdaX -1 == posx: return siguiente
						elif siguientePosX <= posx and celdaX < siguientePosX:
							siguiente = celda
							siguientePosX = celdaX

					elif celdaX<posx and (siguientePosX>=posx or celdaX > siguientePosX) :
						siguiente = celda
						siguientePosX = celdaX
						if celdaX + 1 == posx: return siguiente
					elif siguientePosX>=posx and celdaX > siguientePosX:
						siguiente = celda
						siguientePosX = celdaX
				else: return siguiente
	def getPos(self):
		posRect = self.rect.topleft
		size = self.image.get_size()
		return (int(posRect[0]/size[0]), int(posRect[1]/size[1]))
	
	def update(self):
		if self.actualizar:
			for group in self.groups():
				if isinstance(group, CeldasTablero):
					group.Actualizar(self)
					break

class BloqueSerpiente(Celda):
	def __init__(self, celda, orden, direccion, lenInit, faltante):
		Celda.__init__(self, celda.image, tipo=3, pos=celda.getPos())#, pos=celda.rect.topleft)
		self.dibujar(lenInit, faltante)

	def dibujar(self, lenInit, faltante):
		w = faltante if faltante + lenInit <= self.image.get_width() else self.image.get_width() - lenInit
		draw.rect(self.image, Color("blue"), (lenInit, 0, w, self.image.get_height()))
""" TEmporales """

class Bloque(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)