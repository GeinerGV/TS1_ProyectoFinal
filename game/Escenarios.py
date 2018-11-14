from pygame import sprite, surface, time, Color, draw, Rect, font
from game.Tableros import AreaTablero

# Escenarios de Prueba
class simpleEscenario(sprite.Sprite):
	pass

class testEscenario(sprite.Sprite):
	def __init__(self, screen):
		sprite.Sprite.__init__(self)
		self.image = surface.Surface(screen)
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.complete = True
		self.actualizar = False

### FIN DE Escenarios de prueba
class Escena(sprite.Group):
	def __init__(self, screen, bgcolor, escena):
		sprite.Group.__init__(self)
		self.escena = escena
		self.espacios = {"tab": (screen, (0,0))}
		self.add(AreaTablero(self.espacios["tab"][0], self.espacios["tab"][1], bgcolor, self.getEstructura()))

	def getEstructura(self):
		from game.Estructuras import Estructuras_Escenarios as StructSce
		estructuras = StructSce
		estructura = dict()
		for escena in self.escena:
			if ("color" in estructuras[escena]):
				estructura["color"] = estructuras[escena]["color"]
			if "celdas" in estructuras[escena]:
				estructura["celdas"] = estructuras[escena]["celdas"]
			if "vel" in estructuras[escena]:
				estructura["vel"] = estructuras[escena]["vel"]
			if "estructuras" in estructuras[escena]:
				estructuras = estructuras[escena]["estructuras"]
			else:
				break
		return estructura
		

class Escenario(sprite.Sprite):
	def __init__(self, screen, escena = "0"):
		sprite.Sprite.__init__(self)
		self.code = 4
		self.start = time.get_ticks()
		self.subcode = escena
		self.image = surface.Surface(screen)
		from game.Estructuras import Fondos_de_escenas as Fondos
		self.fondo = Fondos[self.getSubCodeList()[0]]
		del Fondos
		self.image.fill(Color(self.fondo))
		self.escena = Escena(screen, self.fondo, self.getSubCodeList())
		self.escena.draw(self.image)
		self.rect = self.image.get_rect()
		self.complete = True
		self.actualizar = False

	def getSubCodeList(self):
		return tuple(map(lambda seccion: int(seccion), self.subcode.split(".")))
	
	def update(self):
		self.escena.update(self.escena.pause)

class ListaNivelEscenario(sprite.Sprite):
	def __init__(self, screen):
		sprite.Sprite.__init__(self)
		self.code = 2
		self.start = time.get_ticks()
		self.image = surface.Surface(screen)
		self.image.fill(Color("white"))
		font.init()
		self.label = font.Font.render("Niveles", True, Color("yellow"))

class MenuEscenario(sprite.Sprite):
	def __init__(self, screen):
		sprite.Sprite.__init__(self)
		self.image = surface.Surface(screen)
		self.image.fill((255, 255, 255))
		self.rect = self.image.get_rect()
		self.playButton = surface.Surface([int(screen[1]*0.5), int(screen[1]*0.5)])
		self.playButton.fill(Color("white"))
		rect = self.playButton.get_rect()
		rect.center = self.rect.center
		draw.circle(self.playButton, Color("yellow"), [int(self.playButton.get_width()/2), int(self.playButton.get_width()/2)], int(self.playButton.get_width()/2))
		rect = self.playButton.get_size()
		rect = Rect([(int(rect[0]*0.25), int(rect[1]*0.35)), (int(rect[0]*0.5), int(rect[1]*0.3))])
		# rect = (self.rect.centerx, int(screen[1]*0.5*0.25), self.rect.centery, int(screen[1]*0.5*0.15))
		# rect = Rect(rect[0]-rect[1], rect[2]-rect[3], rect[1]*2, rect[3]*2)
		draw.polygon(self.playButton, Color("orange"), [rect.topleft, (rect.x+0.25*rect.w, rect.centery), rect.bottomleft, rect.midright])
		self.image.blit(self.playButton, tuple(map(lambda val: int(val - self.playButton.get_width()/2), self.rect.center)))
		del rect
		self.complete = True
		self.actualizar = False
		self.code = 1
	def getCenterPlayButton(self):
		return self.rect.center

class EscenarioInicio(sprite.Sprite):
	def __init__(self, screen, animation, start = time.get_ticks()):
		sprite.Sprite.__init__(self)
		self.complete = False
		self.start = start
		self.animation = animation
		self.color = Color("yellow")
		self.image = surface.Surface((int(screen[1]*0.4), int(screen[1]*0.4)))
		self.rect = self.image.get_rect()
		self.rect.center = (int(screen[0]*0.5), int(screen[1]*0.5))
		self.actualizar = False
		self.code = 0

	def update(self):
		progress = (time.get_ticks() - self.start)/self.animation
		if progress < 1:
			import math
			rect = (*self.image.get_abs_offset(), *self.image.get_size())
			draw.arc(self.image, self.color, rect, 0, math.pi*2*progress, int(rect[3]/2))
			self.actualizar = True
			del math, rect
		elif not self.complete:
			import math
			pos = tuple(map(lambda val: int(val/2), self.image.get_size()))
			draw.circle(self.image, self.color, pos, pos[1])
			del math, pos
			self.actualizar = True
			self.complete = True

class EscenarioCnt(sprite.GroupSingle):
	def __init__(self, screen):
		sprite.GroupSingle.__init__(self)
		self.timeInitScreen = time.get_ticks()
		self.timeNextScreen = 2000
		self.screen = screen
		self.escenerio = EscenarioInicio(self.screen, self.timeNextScreen*4/5)
		self.nextEscenario = MenuEscenario(self.screen)
		self.add(self.escenerio)
		self.actualizar = False
		self.forzarCambio = False

	def changeEscenario(self, escenario, forzar = False):
		self.nextEscenario = escenario
		if forzar: self.forzarCambio = True
		self.timeNextScreen = 0

	def ReRender(self, ventana):
		self.update()
		superficie = self.sprites()[0]
		if superficie.actualizar:
			self.actualizar = True
			superficie.actualizar = False
		if superficie.complete or self.forzarCambio:
			if self.timeNextScreen >= 0 and self.timeInitScreen + self.timeNextScreen - time.get_ticks() <= 0 and self.nextEscenario.complete:
				# self.add(self.nextEscenario)
				if self.forzarCambio: self.forzarCambio = False
				self.escenerio = self.nextEscenario
				self.add(self.escenerio)
				self.timeInitScreen = time.get_ticks()
				self.escenerio.start = self.timeInitScreen
				if isinstance(self.escenerio, MenuEscenario):
					self.nextEscenario = testEscenario(self.screen)
					self.timeNextScreen = -1
				elif isinstance(self.escenerio, Escenario):
					pass
				else:
					self.timeNextScreen = -1
				self.actualizar = True
		if self.actualizar:
			self.draw(ventana)