from yoha_const import *
from yoha_classes import *
def crear_enemigo(color_enemigo):
    if color_enemigo == "naranja": #Este if hace que vaya intercalando entre amarillo y naranja
            mandarina = Enemigo("mandarina_1.png", ENEMIGO_POS_INICIAL)
            color_enemigo = "amarillo"
    else:
        mandarina = Enemigo("mandarina_2.png", ENEMIGO_POS_INICIAL)
        color_enemigo = "naranja"

    return mandarina, color_enemigo

def crear_celda(color_enemigo, enemigos, posicion_x = 100):
    mandarina, color_enemigo = crear_enemigo(color_enemigo)
    ENEMIGO_POS_INICIAL[0] += posicion_x
    enemigos.append(mandarina)
    
    return enemigos, color_enemigo