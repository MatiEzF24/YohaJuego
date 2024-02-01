from pygame import *
from yoha_const import *
from yoha_classes import *
from yoha_funciones import *
from random import *
from tkinter.simpledialog import askstring as prompt
init()

pantalla = display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
display.set_caption("YohaJuego")

fondo = Fondo("fondo.png")
fondo_nv_3 = Fondo("fondo_nv3.png")
yohane = JugadorYoha("yohane.png", "yohane2.png", "yohane3.png", YOHANE_POS_INICIAL)
titulo = Titulo("titulo.png")
fuente_juego = font.SysFont("Monocraft", 24)
fuente_menu_principal = font.SysFont("Monocraft", 42)

proyectiles_enemigos = []
proyectiles = []
enemigos = []
tiempo_ultimo_disparo = 0
tiempo_ultimo_disparo_enemigo= 0
puntaje = 0
puntaje_final = 0
tiempo_ultima_actulizacion = 0
pantalla_actual = "menu_principal"
pantalla_victoria = True
pantalla_final = False
flag_correr = True
posicion_click = (0, 0)
flag_guardar_puntaje = True
crear_tablas()

def detectar_inputs_jugador(nivel_3 = False):
    global tiempo_ultimo_disparo
    if True in lista_teclas:
        if lista_teclas[K_RIGHT]:
            if nivel_3:
                yohane.mover_derecha(nivel_3= True)
            else:
                yohane.mover_derecha()
        if lista_teclas[K_LEFT]:
            yohane.mover_izquierda()
        if lista_teclas[K_UP] and tiempo_actual - tiempo_ultimo_disparo > DELAY_ENTRE_DISPAROS:
            yohane.disparar(proyectiles)
            tiempo_ultimo_disparo = tiempo_actual

def mostrar_y_calcular_proyectiles():
    global puntaje
    for proyectil in proyectiles: #Logica de los proyectiles
        proyectil.mover()
        proyectil.mostrar(pantalla)
        for enemigo in enemigos:
            if proyectil.rect.colliderect(enemigo.rect):
                proyectiles.remove(proyectil)  # Eliminar el proyectil
                enemigos.remove(enemigo)
                puntaje +=10
                # print(puntaje)

def mostrar_y_calcular_proyectiles_enemigos():
    global puntaje
    for proyectil_enemigo in proyectiles_enemigos: #Logica de los proyectiles enemigos
        proyectil_enemigo.mover()
        proyectil_enemigo.mostrar(pantalla)
        if proyectil_enemigo.rect.colliderect(yohane.rect): #Le baja la vida al tocar al jugador
            proyectiles_enemigos.remove(proyectil_enemigo)
            yohane.recibir_daño()
            if puntaje >= PENALIZACION_PUNTAJE:
                puntaje -= PENALIZACION_PUNTAJE
            else:
                puntaje -= puntaje

def mostrar_enemigos_y_atacar_al_jugador(delay):
    global enemigos
    global tiempo_ultimo_disparo_enemigo
    for enemigo in enemigos:
        enemigo.mostrar(pantalla)
        if len(enemigos) > 0 and tiempo_actual - tiempo_ultimo_disparo_enemigo > delay:
            enemigo_aleatoreo = choice(enemigos)
            enemigo_aleatoreo.disparar(proyectiles_enemigos)
            tiempo_ultimo_disparo_enemigo = tiempo_actual

def animar_sprite():
    global tiempo_ultima_actulizacion
    if tiempo_actual - tiempo_ultima_actulizacion > DELAY_FRAMES:
        yohane.actualizar_sprite()
        tiempo_ultima_actulizacion = tiempo_actual

while flag_correr:
    
    tiempo_actual = time.get_ticks()
    lista_eventos = event.get()
    for evento in lista_eventos:#Este for sólo sirve para debug, ver la posición del click en la consola
        if evento.type == MOUSEBUTTONDOWN:
            posicion_click = evento.pos
            # yohane.recibir_salud() #Herramientas de debug
            # print(posicion_click)
        if evento.type == QUIT:
            flag_correr = False

    match(pantalla_actual):

        case "menu_principal":
            fondo.mostrar(pantalla)
            titulo.mostrar(pantalla)
            escribir_texto(pantalla, "JUGAR", fuente_menu_principal, BLANCO, (250, 350))
            escribir_texto(pantalla, "TABLA DE PUNTAJES", fuente_menu_principal, BLANCO, (100, 450))
            escribir_texto(pantalla, "SALIR", fuente_menu_principal, BLANCO, (250, 550))
            if (posicion_click[0] > 250 and posicion_click[0] < 390) and (posicion_click[1] > 350 and posicion_click[1] < 380):
                pantalla_actual = "nivel_1"
                # print(pantalla_actual)
                mapear_enemigos(enemigos, ENEMIGO_POS_INICIAL.copy())
                posicion_click = (0, 0)
            elif (posicion_click[0] > 250 and posicion_click[0] < 390) and (posicion_click[1] > 450 and posicion_click[1] < 490):
                pantalla_actual = "tabla_puntajes"
                posicion_click = (0,0)
            elif (posicion_click[0] > 250 and posicion_click[0] < 390) and (posicion_click[1] > 550 and posicion_click[1] < 590):
                flag_correr = False


        case "nivel_1":
            
            lista_teclas = key.get_pressed()#Eventos para tomar los botones y hacer que el jugador dispare y se mueva

            detectar_inputs_jugador()
    
            if not yohane.morir():

                fondo.mostrar(pantalla)
                
                mostrar_y_calcular_proyectiles()

                mostrar_y_calcular_proyectiles_enemigos()

                yohane.mostrar(pantalla)
                animar_sprite()
                yohane.vida(pantalla)
                escribir_texto(pantalla, f"Puntaje: {puntaje}", fuente_juego, BLANCO, POSISION_PUNTAJE)
                #escribir_texto(pantalla, f"Tiempo : {int(tiempo_actual/1000)}", fuente_juego, BLANCO, POSISION_TIEMPO)

                if len(enemigos) != 0:#Deja de blitear a los enemigos si se mueren
                    mostrar_enemigos_y_atacar_al_jugador(DELAY_ENTRE_DISPAROS_ENEMIGO)
                elif len(enemigos) == 0:
                    puntaje_final += puntaje
                    pantalla_actual = "nivel_2"
                    pantalla_victoria = True
                    # print(pantalla_actual)
                # # draw.rect(pantalla, ROJO, proyectil.rect, 2) #Quitar comentario para poder ver la colision
                #draw.rect(pantalla, ROJO, mandarina.rect, 2)
            else:
                mostrar_pantalla_muerte(pantalla, fuente_juego, puntaje, pantalla_actual)
                puntaje, enemigos, proyectiles, proyectiles_enemigos = reiniciar_nivel(yohane, puntaje, enemigos, proyectiles, proyectiles_enemigos, pantalla_actual)

        case "nivel_2":
            if pantalla_victoria:
                mostrar_pantalla_victoria(pantalla, fuente_juego, puntaje)
                tecla = key.get_pressed()
                if tecla[K_SPACE]:
                    for i in range(6):
                        yohane.recibir_salud()
                    puntaje = 0
                    yohane.mover_forzado(YOHANE_POS_INICIAL)
                    enemigos = []
                    proyectiles = []
                    proyectiles_enemigos = []
                    mapear_enemigos_nv_2(enemigos, ENEMIGO_POS_NV_2.copy())
                    pantalla_victoria = False
            else:                
                lista_teclas = key.get_pressed()#Eventos para tomar los botones y hacer que el jugador dispare y se mueva

                detectar_inputs_jugador()
        
                if not yohane.morir():

                    fondo.mostrar(pantalla)
                    
                    mostrar_y_calcular_proyectiles()
                    
                    mostrar_y_calcular_proyectiles_enemigos()

                    yohane.mostrar(pantalla)
                    animar_sprite()
                    yohane.vida(pantalla)
                    escribir_texto(pantalla, f"Puntaje: {puntaje}", fuente_juego, BLANCO, POSISION_PUNTAJE)
                    # draw.rect(pantalla, ROJO, yohane.rect, 2)

                    if len(enemigos) != 0:#Deja de blitear a los enemigos si se mueren
                        mostrar_enemigos_y_atacar_al_jugador(DELAY_ENTRE_DISPAROS_ENEMIGO_NV_2)
                    elif len(enemigos) == 0:
                        puntaje_final += puntaje
                        pantalla_victoria = True
                        pantalla_actual = "nivel_3"
                    # # draw.rect(pantalla, ROJO, proyectil.rect, 2) #Quitar comentario para poder ver la colision
                    
                else:
                    mostrar_pantalla_muerte(pantalla, fuente_juego, puntaje, pantalla_actual)
                    puntaje, enemigos, proyectiles, proyectiles_enemigos = reiniciar_nivel(yohane, puntaje, enemigos, proyectiles, proyectiles_enemigos, pantalla_actual)
        case "nivel_3":
            # print(pantalla_victoria)
            if pantalla_victoria:
                mostrar_pantalla_victoria(pantalla, fuente_juego, puntaje)
                tecla = key.get_pressed()
                if tecla[K_SPACE]:
                    for i in range(6):
                        yohane.recibir_salud()
                    puntaje = 0
                    yohane.mover_forzado(YOHANE_POS_NV_3)
                    enemigos = []
                    proyectiles = []
                    proyectiles_enemigos = []
                    pantalla = display.set_mode((ANCHO_VENTANA_NV_3, ALTO_VENTANA_NV_3))
                    mapear_enemigos_nv_3(enemigos)
                    pantalla_victoria = False

            elif pantalla_final:
                mostrar_pantalla_final(pantalla, fuente_juego, puntaje_final)
                tecla = key.get_pressed()
                if flag_guardar_puntaje:
                    nombre_jugador = prompt("Nuevo score","Ingresa tu nombre!")
                    insertar(nombre_jugador, puntaje_final)
                    flag_guardar_puntaje = False
                if tecla[K_SPACE]:
                    flag_correr = False
                    #pantalla_actual = "menu_principal"
                    
                    
            else:               
                lista_teclas = key.get_pressed()#Eventos para tomar los botones y hacer que el jugador dispare y se mueva

                detectar_inputs_jugador(nivel_3= True)
        
                if not yohane.morir():

                    fondo_nv_3.mostrar(pantalla)
                    
                    mostrar_y_calcular_proyectiles()
                    
                    mostrar_y_calcular_proyectiles_enemigos()

                    yohane.mostrar(pantalla)
                    animar_sprite()
                    yohane.vida(pantalla)
                    escribir_texto(pantalla, f"Puntaje: {puntaje}", fuente_juego, BLANCO, (1100, 10))
                    # draw.rect(pantalla, ROJO, yohane.rect, 2)

                    if len(enemigos) != 0:#Deja de blitear a los enemigos si se mueren
                        mostrar_enemigos_y_atacar_al_jugador(DELAY_ENTRE_DISPAROS_ENEMIGO_NV_3)
                    elif len(enemigos) == 0:
                        puntaje_final += puntaje
                        # print(pantalla_actual)
                        pantalla_final = True
                else:
                    mostrar_pantalla_muerte(pantalla, fuente_juego, puntaje, pantalla_actual)
                    puntaje, enemigos, proyectiles, proyectiles_enemigos = reiniciar_nivel(yohane, puntaje, enemigos, proyectiles, proyectiles_enemigos, pantalla_actual)
        case "tabla_puntajes":
            fondo.mostrar(pantalla)
            puntuaciones = seleccionar()
            escribir_texto(pantalla, "VOLVER", fuente_menu_principal, BLANCO, (250, 550))
            #                                   enumera las puntuaciones empezando desde 1
            for indice, (id, nombre, score) in enumerate(puntuaciones, start=1):
                texto = fuente_menu_principal.render(f"{indice}. {nombre}: {score}", True, BLANCO)
                pantalla.blit(texto, (50, 50 + indice * 40)) #cada texto se pone 4 pixeles por debajo del anterior


            if (posicion_click[0] > 250 and posicion_click[0] < 390) and (posicion_click[1] > 550 and posicion_click[1] < 590):
                pantalla_actual = "menu_principal"
                posicion_click = (0,0)
                

    display.flip()


quit()