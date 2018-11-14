from pygame import sprite
from game.Bloques import BloqueSerpiente

class Snake(sprite.Group):
	longitudBase = "2"
	defDirection = 2
	def __init__(self, tablero, longitud, direccion = 0, velocidad = None, pos = None, inicio = 0):
		sprite.Group.__init__(self)
		self.tablero = tablero
		self.direccion = self.defDirection if direccion == 0 else direccion
		self.longitud = self.getLongitud(longitud)
		self.inicioCelda = 0
		self.getValInicioCelda(inicio)
		self.velocidad = ["1", 1000] if velocidad == None else velocidad
		if pos == None:
			self.pos = [0, 0]
		else:
			self.pos = pos
		celda = self.tablero.celdas.getCelda(self.pos)
		self.add(BloqueSerpiente(celda, 0, self.direccion, self.inicioCelda, self.getLongitud()))
		restante = self.getLongitud() - (self.tablero.sizeCelda - self.inicioCelda)
		for orden in range(1, self.getNumCeldas()):
			celda = celda.getNext(self.getOpositeDireccion())
			self.add(BloqueSerpiente(celda, orden, self.direccion, 0, restante))
			restante = restante - self.tablero.sizeCelda
		self.prevDireccion = self.direccion
		self.actualizar = False

	def getOpositeDireccion(self, direccion = None):
		if direccion == None: return self.getOpositeDireccion(self.direccion)
		if direccion == 1: return 3
		if direccion == 2: return 4
		if direccion == 3: return 1
		if direccion == 4: return 2

	def getValInicioCelda(self, valor):
		self.inicioCelda = self.getLongitud(valor)
		if self.inicioCelda >= self.tablero.sizeCelda:
			self.movePos(int(self.inicioCelda/self.tablero.sizeCelda))
			self.inicioCelda = self.inicioCelda % self.tablero.sizeCelda

	def movePos(self, val):
		if val == 0: return None
		celda = self.tablero.celdas.getCelda(self.pos)
		for i in range(val):
			celda = celda.getNext(self.direccion)
		self.pos = celda.getPos()

	def getEje(self, valor = None):
		if valor == None:
			return self.getEje(self.direccion)
		if valor == 1 or valor == 3:
			return "y"
		elif valor == 2 or valor == 4:
			return "x"
		return ""

	def getNumCeldas(self):
		import math
		return math.ceil((self.getLongitud()+self.inicioCelda)/self.tablero.sizeCelda)

	def getLongitud(self, valor = None):
		if valor == None:
			return self.longitud + self.getLongitud(self.longitudBase)
		return valor if isinstance(valor, int) else int(valor)*self.tablero.sizeCelda















class SnakeTmp:
	"""
	Esta es la serpiente de nuestro juego
	"""
	default_color = "verde"
	def __init__(self, posX, posY, longitud, direccion, vidas):
		self.x = posX
		self.y = posY
		self.longitud = longitud
		self.direccion = direccion
		self.vidas = vidas
		self.alimentos = 0

	def comerAlimento(self):
		self.alimentos += 1
	
	def moverX(self, newPosX):
		self.x = newPosX
	
	def moverY(self, newPosY):
		self.y = newPosY

	def conVida(self):
		return True if self.vidas > 0 else False

	def perderVida(self):
		if self.conVida():
			self.vidas -= 1

	
