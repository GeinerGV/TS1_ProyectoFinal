from pygame import sprite, surface, Color
from game.Bloques import CeldasTablero
from game.Snake import Snake

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
		
		# self.tableroCnt.add(Snake(tablero, 0, pos=(3,0)))
		
		self.tableroCnt.draw(self.image)
		# print(sprite.groupcollide(tablero.celdas.filas[2], tablero.celdas.columnas[3], False, False))
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

		# Draw Serpiente
		self.snake = Snake(self, 0, pos=(3,0))
		self.snake.draw(self.image)

	def update(self):
		pass