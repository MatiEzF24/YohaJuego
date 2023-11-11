from pygame import *
from yoha_const import *



class Fondo:
    def __init__(self, imagen) -> None:
        self.imagen = image.load(imagen)

    def mostrar(self, pantalla):
        pantalla.blit(self.imagen, (0, 0))

class JugadorYoha:
    def __init__(self, imagen, posicion_inicial) -> None:
        self.imagen = image.load(imagen)
        self.posicion = list(posicion_inicial)
        self.rect = self.imagen.get_rect()
        self.rect.topleft = posicion_inicial
        self.salud = 6
        self.salud_maxima = 6
        self.corazon = image.load("corazon.png")
    
    def mover_derecha(self):
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

    def recibir_daño(self):
        if self.salud > 0:
            self.salud -= 1

    def recibir_salud(self):
        if self.salud < self.salud_maxima:
            self.salud += 1

    def vida(self, pantalla):
        for corazon in range(self.salud):
            pantalla.blit(self.corazon,(corazon * 40, 10))

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
