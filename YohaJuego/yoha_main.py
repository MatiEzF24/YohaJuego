from pygame import *
from yoha_const import *
from yoha_classes import *
from yoha_funciones import *
from random import *
init()

pantalla = display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
display.set_caption("YohaJuego")

flag = True
color_enemigo = "naranja"
fondo = Fondo("fondo.png")
yohane = JugadorYoha("yohane.png", YOHANE_POS_INICIAL)
proyectiles_enemigos = []
proyectiles = []
enemigos = []
tiempo_ultimo_disparo = 0
delay_entre_disparos = 300
tiempo_ultimo_disparo_enemigo= 0
delay_entre_disparos_enemigo = 1500
flag_correr = True
puntaje = 0

while len(enemigos) < 14: #Mapea a los enemigos, cada fila está marcada por los if principales
    if len(enemigos) < 5:
        enemigos, color_enemigo = crear_celda(color_enemigo, enemigos)
    elif len(enemigos) < 9:
        if flag:
            ENEMIGO_POS_INICIAL[0] -=150
            ENEMIGO_POS_INICIAL[1] +=80
            flag = False
        enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, -100)
    else:
        if not flag:
            ENEMIGO_POS_INICIAL[0] +=50
            ENEMIGO_POS_INICIAL[1] +=80
            flag = True
        enemigos, color_enemigo = crear_celda(color_enemigo, enemigos)

while flag_correr:
    tiempo_actual = time.get_ticks()
    lista_eventos = event.get()
    for evento in lista_eventos:#Este for sólo sirve para debug, ver la posición del click en la consola
        if evento.type == MOUSEBUTTONDOWN:
            posicion_click = evento.pos
            yohane.recibir_salud()
            print(posicion_click)
        if evento.type == QUIT:
            flag_correr = False

    lista_teclas = key.get_pressed()#Eventos para tomar los botones y hacer que el jugador dispare y se mueva
    if True in lista_teclas:
        if lista_teclas[K_RIGHT]:
            yohane.mover_derecha()
        if lista_teclas[K_LEFT]:
            yohane.mover_izquierda()
        if lista_teclas[K_UP] and tiempo_actual - tiempo_ultimo_disparo > delay_entre_disparos:
            yohane.disparar(proyectiles)
            tiempo_ultimo_disparo = tiempo_actual

    fondo.mostrar(pantalla)
    # if len(enemigos) > 0 and tiempo_actual - tiempo_ultimo_disparo_enemigo > delay_entre_disparos_enemigo:
    #         enemigo.disparar(proyectiles_enemigos)
    #         tiempo_ultimo_disparo_enemigo = tiempo_actual

    for proyectil in proyectiles: #Logica de los proyectiles
        proyectil.mover()
        proyectil.mostrar(pantalla)
        for enemigo in enemigos:
            if proyectil.rect.colliderect(enemigo.rect):
                proyectiles.remove(proyectil)  # Eliminar el proyectil
                enemigos.remove(enemigo)
                puntaje +=10
                print(puntaje)
    for proyectil_enemigo in proyectiles_enemigos: #Logica de los proyectiles enemigos
        proyectil_enemigo.mover()
        proyectil_enemigo.mostrar(pantalla)
        if proyectil_enemigo.rect.colliderect(yohane.rect): #Le baja la vida al tocar al jugador
            proyectiles_enemigos.remove(proyectil_enemigo)
            yohane.recibir_daño()

    yohane.mostrar(pantalla)
    yohane.vida(pantalla)

    if len(enemigos) != 0:#Deja de blitear a los enemigos si se mueren
        for enemigo in enemigos:
            enemigo.mostrar(pantalla)
            if len(enemigos) > 0 and tiempo_actual - tiempo_ultimo_disparo_enemigo > delay_entre_disparos_enemigo:
                enemigo_aleareo = choice(enemigos)
                enemigo_aleareo.disparar(proyectiles_enemigos)
                tiempo_ultimo_disparo_enemigo = tiempo_actual
    # # draw.rect(pantalla, ROJO, proyectil.rect, 2) #Quitar comentario para poder ver la colision
    #draw.rect(pantalla, ROJO, mandarina.rect, 2)

    display.flip()

quit()