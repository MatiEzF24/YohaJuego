from pygame import *
from yoha_const import *

class Fondo:
    def __init__(self, imagen) -> None:
        self.imagen = image.load(imagen)

    def mostrar(self, pantalla):
        pantalla.blit(self.imagen, (0, 0))


class Titulo:
    def __init__(self, imagen) -> None:
        self.imagen = image.load(imagen)

    def mostrar(self, pantalla):
         pantalla.blit(self.imagen, POSISION_TITULO)

class JugadorYoha:
    def __init__(self, imagen, imagen2, imagen3, posicion_inicial) -> None:
        self.sprites = []
        self.sprites.append(image.load(imagen))
        self.sprites.append(image.load(imagen2))
        self.sprites.append(image.load(imagen3))
        self.sprite_actual = 0
        self.imagen = self.sprites[self.sprite_actual]
        self.posicion = list(posicion_inicial)
        self.rect = self.imagen.get_rect()
        self.rect.topleft = posicion_inicial
        self.salud = 6
        self.salud_maxima = 6
        self.corazon = image.load("corazon.png")
        self.sonido_disparo = mixer.Sound("disparo.mp3")
    
    def mover_derecha(self, nivel_3 = False):
        if nivel_3:
            if self.rect.right < ANCHO_VENTANA_NV_3:      
                self.posicion[0] += VELOCIDAD_YOHANE
                self.rect.topleft = self.posicion
        else:
            if self.rect.right < ANCHO_VENTANA:      
                self.posicion[0] += VELOCIDAD_YOHANE
                self.rect.topleft = self.posicion

    def mover_izquierda(self):
        if self.rect.left > 0:
            self.posicion[0] -= VELOCIDAD_YOHANE
            self.rect.topleft = self.posicion

    def mostrar(self, pantalla):
        pantalla.blit(self.imagen, self.posicion)

    def disparar(self, lista_proyectiles = list):
        proyectil = Proyectil("proyectil.png", self.posicion, 1, "arriba", "jugador")
        lista_proyectiles.append(proyectil)
        self.sonido_disparo.play()

    def recibir_daño(self):
        if self.salud > 0:
            self.salud -= 1

    def recibir_salud(self):
        if self.salud < self.salud_maxima:
            self.salud += 1

    def vida(self, pantalla):
        for corazon in range(self.salud):
            pantalla.blit(self.corazon,(corazon * 40, 10))

    def morir(self):
        muerto = False
        if self.salud == 0:
            muerto = True
        return muerto
    
    def mover_forzado(self, posicion):
        self.posicion = list(posicion)
        self.rect.topleft = list(posicion)

    def actualizar_sprite(self):
        self.sprite_actual += 1

        if self.sprite_actual >= len(self.sprites):
            self.sprite_actual = 0

        self.imagen = self.sprites[self.sprite_actual]
    

class Enemigo:
    def __init__(self, imagen, posicion_inicial) -> None:
        self.imagen = image.load(imagen)
        self.posicion = list(posicion_inicial)
        self.rect = self.imagen.get_rect()
        self.rect.topleft = tuple(posicion_inicial)

    def mostrar(self, pantalla):
        pantalla.blit(self.imagen, self.posicion)

    def disparar(self, lista_proyectiles = list):
        proyectil = Proyectil("proyectil.png", self.posicion, 0.5, "abajo", "enemigo")
        lista_proyectiles.append(proyectil)

class Proyectil:
    def __init__(self, imagen = str, posicion_inicial = tuple, velocidad = int, direccion = str, tipo = str) -> None:
        self.imagen = image.load(imagen)
        self.posicion = list(posicion_inicial).copy()
        if tipo == "jugador":
            self.posicion[0] += 80 #Se centra la posision en medio del jugador
        elif tipo == "enemigo":
            self.posicion[0] += 40 #Se centra la posision en medio del enemigo
        self.velocidad = velocidad
        self.direccion = direccion
        self.rect = self.imagen.get_rect()
        self.rect.topleft = self.posicion

    def mover(self):
        if self.direccion == "arriba":
            self.posicion[1] -= self.velocidad 
            self.rect.topleft = self.posicion
        elif self.direccion == "abajo":
            self.posicion[1] += self.velocidad
            self.rect.topleft = self.posicion

    def mostrar(self, ventana):
        ventana.blit(self.imagen, self.posicion)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
