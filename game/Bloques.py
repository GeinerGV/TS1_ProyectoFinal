from pygame import sprite, surface, Color, time
from pygame import time

class AreaTablero(sprite.Sprite):
	def __init__(self, size, bgcolor):
		sprite.Sprite.__init__(self)
		self.image = surface.Surface(size)
		self.image.fill(Color(bgcolor))
		self.rect = self.image.get_rect()
		self.tableroCnt = TableroCnt()
		tablero = Tablero([42, 48], size)
		tablero.rect.center = self.rect.center
		self.tableroCnt.add(tablero)
		self.tableroCnt.draw(self.image)
		print(sprite.groupcollide(tablero.celdas.filas[2], tablero.celdas.columnas[3], False, False))
		self.actualizar = False

class TableroCnt(sprite.GroupSingle):
	pass

class Tablero(sprite.Sprite):
	def __init__(self, rangoCelda, maxSize, estructura = None):
		sprite.Sprite.__init__(self)
		self.rangeSize = (rangoCelda[0], rangoCelda[1])
		self.sizeCelda = self.rangeSize[0]
		self.dimension = (int(maxSize[0]/self.sizeCelda), int(maxSize[1]/self.sizeCelda))
		self.celdas = CeldasTablero(self.sizeCelda, self.dimension)
		sizeSurf = tuple(map(lambda val: val*self.sizeCelda, self.dimension))
		self.image = surface.Surface(sizeSurf)
		del sizeSurf
		self.celdas.draw(self.image)
		self.rect = self.image.get_rect()

	def update(self):
		pass

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
		for idFila in range(self.dimension[0]):
			self.filas.append(FilaTablero())
			for idCol in range(self.dimension[1]):
				if len(self.columnas) < idCol+1: self.columnas.append(ColumnaTablero())
				celda = None
				if self.estructura == None:
					celda = Celda(self.sizeCelda, pos=(idFila, idCol), color=self.colores[(idFila+idCol)%2])
				self.add(celda)
				self.filas[idFila].add(celda)
				self.columnas[idCol].add(celda)
				
class FilaTablero(sprite.Group):
	pass

class ColumnaTablero(sprite.Group):
	pass

class Celda(sprite.Sprite):
	def __init__(self, base, **kargs):
		sprite.Sprite.__init__(self)
		kargs.setdefault("tipo", 1)
		self.tipo = kargs["tipo"] # 1: habitable, -1: no habitable
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
	
	def getNext(self, dir):
		posx, posy = self.getPos()
		siguiente = None
		for grupo in self.groups():
			if (dir == 1 or dir == 3) and isinstance(grupo, ColumnaTablero):
				for celda in grupo.sprites():
					celdaY = celda.getPos()[1]
					if dir == 1:
						if celdaY<posy:
							siguiente = celdaY
							if celdaY + 1 == posy: return siguiente
					elif  celdaY > posy:
						siguiente = celda
						if celdaY - 1 == posy: return siguiente
				else: return siguiente
			if (dir==2 or dir==4) and isinstance(grupo, FilaTablero):
				for celda in grupo.sprites():
					celdaX = celda.getPos[0]
					if dir == 2:
						if celdaX > posx:
							siguiente = celda
							if celdaX + 1 == posx: return siguiente
					elif celdaX<posx:
						siguiente = celda
						if celdaX - 1 == posx: return siguiente
				else: return siguiente
	def getPos(self):
		posPix = self.image.get_offset()
		size = self.image.get_size()
		return (int(posPix[0]/size[0]), int(posPix[1]/size[1]))
	
	def update(self):
		for group in self.groups():
			if isinstance(group, CeldasTablero):
				self.actualizar = group.actualizar
				if group.actualizar:
					group.Actualizar(self)
				break

class Snake(sprite.Group):
	def __init__(self, tablero, items, longitud, direccion = 0):
		import math
		sprite.Group.__init__(self)
		self.longitudBase = items * 2
		self.longitud = longitud
		self.direccion = direccion
		self.items = items
		self.celdas = math.ceil(self.getLongitud()/self.items)
		self.tablero = tablero.celdas
		celdaInicial = self.getCelda(self.getPosAndDireccionInit())
		self.add(BloqueSerpiente(celdaInicial, 0, self.direccion, self.items, 0))
		longitudRestante = self.getLongitud() - 1*self.items
		for nCelda in range(1, self.celdas):
			if self.direccion == 1:
				siguiente = celdaInicial.getNext(3)
			elif self.direccion == 3:
				siguiente = celdaInicial.getNext(1)
			elif self.direccion == 2:
				siguiente = celdaInicial.getNext(4)
			elif self.direccion == 4:
				siguiente = celdaInicial.getNext(2)
			self.add(BloqueSerpiente(siguiente, nCelda, self.direccion, longitudRestante))

	def getLongitud(self):
		return self.longitudBase + self.longitud

	def getCelda(self, pos):
		for celda in sprite.groupcollide(self.tablero.filas[pos[0]], self.tablero.columnas[pos[1]], False, False):
			return celda
		
	def getPosAndDireccionInit(self, newDir = False):
		if newDir: self.direccion = 0
			self.direccion = 2
		return (self.celdas, 0)

	def posYDireccionList(self):
		pass

class BloqueSerpiente(sprite.Sprite):
	def __init__(self, celda, pos, direccion, longitud, porcentaje):
		sprite.Sprite.__init__(self)


""" TEmporales """
class BloqueCuerpoSerpiente(sprite.Group):
	colors = ["blue", "yellow", "orange"]
	def __init__(self, tablero, lenInit):
		sprite.Group.__init__(self)
		self.tablero = tablero
		self.template = surface.Surface([self.tablero.sizeCelda, self.tablero.sizeCelda])

	def getTemplates(self):
		pass

class PiezaSerpiente(sprite.Sprite):
	def __init__(self, direction, puesto, lenPiezas, **kargs):
		sprite.Sprite.__init__(self)
		self.direction = direction
		self.puesto = puesto
		# self.image = base
		self.rect = self.image.get_rect()
		if "pos" in kargs:
			base = self.image.get_size()
			self.rect.move_ip(base[0] * kargs["pos"][0], base[1] * kargs["pos"][1])

class Bloque(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)