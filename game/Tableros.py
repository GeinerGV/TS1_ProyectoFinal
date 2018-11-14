from pygame import sprite, surface, Color
from game.Bloques import CeldasTablero
from game.Snake import Snake

class AreaTablero(sprite.Sprite):
	def __init__(self, size, pos, bgcolor, estructura = None):
		sprite.Sprite.__init__(self)
		self.image = surface.Surface(size)
		self.image.fill(Color(bgcolor))
		self.rect = self.image.get_rect()
		self.rect.move_ip(pos)
		self.tableroCnt = TableroCnt()
		tablero = Tablero([42, 48], size, estructura)
		self.tableroCnt.add(tablero)
		
		# self.tableroCnt.add(Snake(tablero, 0, pos=(3,0)))
		
		self.tableroCnt.draw(self.image)
		# print(sprite.groupcollide(tablero.celdas.filas[2], tablero.celdas.columnas[3], False, False))
		self.actualizar = False
	
	def update(self, *args):
		self.tableroCnt.update(*args)

class TableroCnt(sprite.GroupSingle):
	pass

class Tablero(sprite.Sprite):
	def __init__(self, rangoCelda, maxSize, estructura = dict()):
		sprite.Sprite.__init__(self)
		self.rangeSize = (rangoCelda[0], rangoCelda[1])
		self.sizeCelda = self.rangeSize[0]
		self.dimension = (int(maxSize[0]/self.sizeCelda), int(maxSize[1]/self.sizeCelda))
		color = estructura["color"] if "color" in estructura else dict()
		bgcolor = color.pop("0") if len(color) and "0" in color else "gray"
		self.celdas = CeldasTablero(self.sizeCelda, self.dimension, colors=color, estructura=estructura["celdas"] if "celdas" in estructura else None)
		del color
		sizeSurf = tuple(map(lambda val: val*self.sizeCelda, self.dimension))
		self.image = surface.Surface(sizeSurf)
		self.image.fill(Color(bgcolor))
		del sizeSurf, bgcolor
		self.celdas.draw(self.image)
		self.rect = self.image.get_rect()
		self.rect.center = (int(maxSize[0]/2), int(maxSize[1]/2))

		# Draw Serpiente
		self.snake = Snake(self, 0, pos=(5,5), velocidad=estructura["vel"] if "vel" in estructura else None)
		self.snake.draw(self.image)

	def update(self, *args):
		self.snake.update(*args)