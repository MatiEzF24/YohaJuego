from yoha_const import *
from yoha_classes import *
import sqlite3
posision_enemigo = ENEMIGO_POS_INICIAL.copy()
posision_enemigo_nv_2 = ENEMIGO_POS_NV_2.copy()
posision_enemigo_nv_3 = ENEMIGO_POS_NV_3.copy()
def crear_enemigo(color_enemigo, pos_a_usar = posision_enemigo):
    if color_enemigo == "naranja": #Este if hace que vaya intercalando entre amarillo y naranja
            mandarina = Enemigo("mandarina_1.png", pos_a_usar)
            color_enemigo = "amarillo"
    else:
        mandarina = Enemigo("mandarina_2.png", pos_a_usar)
        color_enemigo = "naranja"

    return mandarina, color_enemigo

def crear_celda(color_enemigo, enemigos, pos_a_usar = posision_enemigo, posicion_x = 100):
    mandarina, color_enemigo = crear_enemigo(color_enemigo, pos_a_usar)
    pos_a_usar[0] += posicion_x
    enemigos.append(mandarina)
    
    return enemigos, color_enemigo

def escribir_texto(pantalla, texto=str,fuente=font,color=tuple,posision=tuple):
    imagen =fuente.render(texto, True, color)
    pantalla.blit(imagen, posision)

def mapear_enemigos(enemigos, pos_a_usar = posision_enemigo):
    color_enemigo = "naranja"
    flag_mapeo = True
    
    while len(enemigos) < 14: #Mapea a los enemigos, cada fila está marcada por los if principales
        if len(enemigos) < 5:
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, pos_a_usar)
        elif len(enemigos) < 9:
            if flag_mapeo:
                pos_a_usar[0] -=150
                pos_a_usar[1] +=80
                flag_mapeo = False
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos,pos_a_usar, -100)
        else:
            if not flag_mapeo:
                pos_a_usar[0] +=50
                pos_a_usar[1] +=80
                flag_mapeo = True
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, pos_a_usar)

def mapear_enemigos_nv_2(enemigos, pos_a_usar = posision_enemigo_nv_2):
    color_enemigo = "naranja"
    flag_mapeo = True
    
    while len(enemigos) < 17: #Mapea a los enemigos, cada fila está marcada por los if principales
        if len(enemigos) < 6:
            # print("linea53")
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, pos_a_usar)
        elif len(enemigos) < 11:
            # print("linea56")
            if flag_mapeo:
                pos_a_usar[0] -=150
                pos_a_usar[1] +=80
                flag_mapeo = False
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos,pos_a_usar, -100)
        else:
            # print("linea63")
            if not flag_mapeo:
                pos_a_usar[0] +=50
                pos_a_usar[1] +=80
                flag_mapeo = True
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, pos_a_usar)

def reiniciar_nivel(yohane = JugadorYoha, puntaje=int, enemigos = list, proyectiles = list, proyectiles_enemigos = list, nivel = int):
    tecla = key.get_pressed()
    if tecla[K_SPACE]:
        for i in range(6):
            yohane.recibir_salud()
        puntaje = 0
        if nivel != "nivel_3": 
            yohane.mover_forzado(YOHANE_POS_INICIAL)
        else:
            yohane.mover_forzado(YOHANE_POS_NV_3)
        enemigos = []
        proyectiles = []
        proyectiles_enemigos = []
        if nivel == "nivel_1":#Mapea distinto según el nivel
            mapear_enemigos(enemigos, ENEMIGO_POS_INICIAL.copy()) 
        elif nivel == "nivel_2":
            mapear_enemigos_nv_2(enemigos, ENEMIGO_POS_NV_2.copy())
            # print(ENEMIGO_POS_NV_2)
        elif nivel == "nivel_3":
            mapear_enemigos_nv_3(enemigos, ENEMIGO_POS_NV_3.copy())
        # print(enemigos)
    else:
        puntaje = puntaje
        enemigos = enemigos
        proyectiles = proyectiles
        proyectiles_enemigos = proyectiles_enemigos

    return puntaje, enemigos, proyectiles, proyectiles_enemigos

def mostrar_pantalla_muerte(pantalla, fuente_juego, puntaje, nivel):
    if not nivel == "nivel_3":
        escribir_texto(pantalla, "¡PERDISTE!", fuente_juego, ROJO, POS_MENSAJE_PERDER_GANAR)
        escribir_texto(pantalla, f"Puntaje: {puntaje}", fuente_juego, ROJO, POS_PUNTAJE_PERDER_GANAR)
        escribir_texto(pantalla, "Preciona 'Espacio' para jugar de nuevo.", fuente_juego, ROJO, (15, 485))
    else:
        escribir_texto(pantalla, "¡PERDISTE!", fuente_juego, ROJO, (550, 275))
        escribir_texto(pantalla, f"Puntaje: {puntaje}", fuente_juego, ROJO, (540, 300))
        escribir_texto(pantalla, "Preciona 'Espacio' para jugar de nuevo.", fuente_juego, ROJO, (350, 525))

def mostrar_pantalla_victoria(pantalla, fuente_juego, puntaje):
    escribir_texto(pantalla, "¡GANASTE!", fuente_juego, VERDE, POS_MENSAJE_PERDER_GANAR)
    escribir_texto(pantalla, f"Puntaje: {puntaje}", fuente_juego, AZUL, POS_PUNTAJE_PERDER_GANAR)
    escribir_texto(pantalla, "Preciona 'Espacio' para continuar al", fuente_juego, AZUL, (30, 485))
    escribir_texto(pantalla, "siguiente nivel.", fuente_juego, AZUL, (200, 509))

def mapear_enemigos_nv_3(enemigos, pos_a_usar = posision_enemigo_nv_3):
    color_enemigo = "amarillo"
    flag_mapeo = True
    
    while len(enemigos) < 24: #Mapea a los enemigos, cada fila está marcada por los if principales
        if len(enemigos) < 7:
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, pos_a_usar)
        elif len(enemigos) < 15:
            if flag_mapeo:
                pos_a_usar[0] -=50
                pos_a_usar[1] +=80
                color_enemigo = "amarillo"
                flag_mapeo = False
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos,pos_a_usar, -100)
        else:
            if not flag_mapeo:
                pos_a_usar[0] +=50
                pos_a_usar[1] +=80
                color_enemigo = "naranja"
                flag_mapeo = True
            enemigos, color_enemigo = crear_celda(color_enemigo, enemigos, pos_a_usar)

def mostrar_pantalla_final(pantalla, fuente_juego, puntaje):
    escribir_texto(pantalla, "¡GANASTE!", fuente_juego, VERDE, (560, 275))
    escribir_texto(pantalla, f"Puntaje final: {puntaje}", fuente_juego, AZUL, (500, 300))
    escribir_texto(pantalla, "Preciona 'Espacio' para salr del juego", fuente_juego, AZUL, (350, 525))


def crear_tablas():
    with sqlite3.connect("database.db") as conexion:
        try:
        
            crear_tabla = ''' create table Puntajes
            (
            id integer primary key autoincrement,
            nombre text,
            score integer
            )
            '''
            conexion.execute(crear_tabla) #Ejecuta las instrucciones dadas en el string de arriba
            # print("se creo la tabla de scores")
        except sqlite3.OperationalError:
            print("La tabla ya existe")

def insertar(nombre, score):
    score = int(score)
    with sqlite3.connect("database.db") as conexion:
        try:
            conexion.execute("insert into Puntajes(nombre,score) values (?,?)", (nombre, score))

            conexion.commit() #Confirma los cambios para que estos sean permanentes
            # print("Se ejecuto correctamente")
        except:
            print("Error")

def limpiar_tabla():
    with sqlite3.connect("database.db") as conexion:
            try:
                conexion.execute("DELETE FROM Puntajes")

                conexion.commit()
                # print("Se ejecuto correctamente")
            except:
                print("Error")

def seleccionar()-> list:
    '''Devuelve una lista de 5 tuplas ya ordenadas de mayor score a menor'''
    with sqlite3.connect("database.db") as conexion:
            seleccion = []
            try:
                cursor = conexion.execute("SELECT * FROM Puntajes ORDER BY score DESC LIMIT 5")
                for fila in cursor:
                    seleccion.append(fila)

                conexion.commit()
            except:
                print("Error")
                seleccion = None
            
            return seleccion

def eliminar_dato(id):
    with sqlite3.connect("database.db") as conexion:
        try:
            conexion.execute("DELETE FROM Puntajes WHERE id=?", (id))

            conexion.commit()
            # print("Se ejecuto correctamente")
        except:
            print("Error")
