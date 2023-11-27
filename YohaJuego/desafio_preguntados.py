# A. Analizar detenidamente el set de datos.
# B. Recorrer la lista guardando en sub-listas: la pregunta, cada opción y la respuesta
# correcta.
# C. Crear 2 botones (rectángulos) uno con la etiqueta “Pregunta”, otro con la etiqueta
# “Reiniciar”
# D. Imprimir el Score: 999 donde se va a ir acumulando el puntaje de las respuestas
# correctas. Cada respuesta correcta suma 10 puntos.
# E. Al hacer clic en el botón (rectángulo) “Pregunta” debe mostrar las preguntas
# comenzando por la primera y las tres opciones, cada clic en este botón pasa a la
# siguiente pregunta.
# F. Al hacer clic en una de las tres palabras que representa una de las tres opciones, si es
# correcta, debe sumar el score y dejar de mostrar las opciones.
# G. Solo tiene 2 opciones para acertar la respuesta correcta y sumar puntos, si agotó ambas
# opciones, deja de mostrar las opciones y no suma score
# H. Al hacer clic en el botón (rectángulo) “Reiniciar” debe mostrar las preguntas
# comenzando por la primera y las tres opciones, cada clic pasa a la siguiente pregunta.
# También debe reiniciar el Score.
import pygame
from datos import lista
from constantes import *

#Inicializo variables
posicion=0
preguntas = [" "]
opciones_a = [" "]
opciones_b = [" "]
opciones_c = [" "]
opciones_correctas = [" "]

for dic in lista:
    preguntas.append(dic["pregunta"])
    opciones_a.append(dic["a"])
    opciones_b.append(dic["b"])
    opciones_c.append(dic["c"])
    opciones_correctas.append(dic["correcta"])

pygame.init()
screen = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA]) #La ventana
preguntados_pic = pygame.image.load("Trivia-Crack-F.png")
preguntados_pic = pygame.transform.scale(preguntados_pic,(250, 250))
font = pygame.font.SysFont("Minecraftia Normal", 50)
font_preguntas = pygame.font.SysFont("Minecraftia Normal", 25)
text_boton_pregunta = font.render("Pregunta", False, COLOR_GRIS)
text_reiniciar = font.render("Reiniciar", False, COLOR_GRIS)
pygame.display.set_caption("Preguntados") #Título de la ventana
#Inicializo variables
pregunta = preguntas[posicion]
respuesta_a = opciones_a[posicion]
respuesta_b = opciones_b[posicion]
respuesta_c = opciones_c[posicion]
respuesta_correcta = opciones_correctas[posicion]
respuesta_usuario = ""
text_pregunta = font_preguntas.render(pregunta, True, COLOR_AMARILLO)
text_opcion_a = font_preguntas.render(respuesta_a, True, COLOR_AMARILLO)
text_opcion_b = font_preguntas.render(respuesta_b, True, COLOR_AMARILLO)
text_opcion_c = font_preguntas.render(respuesta_c, True, COLOR_AMARILLO)
score = 000
intentos = 0
flag_score = True
maximo_preguntas = False
text_score = font.render(f"Score: {score}", True, COLOR_ROJO)
running = True

while running:

    listado_eventos = pygame.event.get()

    for evento in listado_eventos:
        if evento.type == pygame.QUIT:
            running = False
    
        if evento.type == pygame.MOUSEBUTTONDOWN:
            posicion_click = evento.pos
            print(posicion_click)

            #Botón pregunta
            if (posicion_click[0] > 300 and posicion_click[0] < 500) and (posicion_click[1] > 20 and posicion_click[1] < 120):
                posicion +=1
                usuario_correcta = False
                flag_score = True
                intentos = 0
                respuesta_usuario = ""
                pregunta = preguntas[posicion]
                respuesta_a = opciones_a[posicion]
                respuesta_b = opciones_b[posicion]
                respuesta_c = opciones_c[posicion]
                respuesta_correcta = opciones_correctas[posicion]
                print(respuesta_correcta)
                text_pregunta = font_preguntas.render(pregunta, True, COLOR_AMARILLO)
                text_opcion_a = font_preguntas.render(respuesta_a, True, COLOR_AMARILLO)
                text_opcion_b = font_preguntas.render(respuesta_b, True, COLOR_AMARILLO)
                text_opcion_c = font_preguntas.render(respuesta_c, True, COLOR_AMARILLO)

            #Botón reiniciar       min pos left           max pos left                  min pos top          max pos top
            if (posicion_click[0] > 550 and posicion_click[0] < 800) and (posicion_click[1] > 20 and posicion_click[1] < 120):
                posicion = 1
                score = 0
                text_score = font.render(f"Score: {score}", True, COLOR_ROJO)
                usuario_correcta = False
                flag_score = True
                intentos = 0
                respuesta_usuario = ""
                pregunta = preguntas[posicion]
                respuesta_a = opciones_a[posicion]
                respuesta_b = opciones_b[posicion]
                respuesta_c = opciones_c[posicion]
                respuesta_correcta = opciones_correctas[posicion]
                text_pregunta = font_preguntas.render(pregunta, True, COLOR_AMARILLO)
                text_opcion_a = font_preguntas.render(respuesta_a, True, COLOR_AMARILLO)
                text_opcion_b = font_preguntas.render(respuesta_b, True, COLOR_AMARILLO)
                text_opcion_c = font_preguntas.render(respuesta_c, True, COLOR_AMARILLO)

            if posicion > 0:
                if (posicion_click[0] > 100 and posicion_click[0] < 250) and (posicion_click[1] > 385 and posicion_click[1] < 435):
                    print("a")
                    respuesta_usuario = "a"
                    if respuesta_usuario != respuesta_correcta:
                        intentos +=1
                elif (posicion_click[0] > 350 and posicion_click[0] < 500) and (posicion_click[1] > 385 and posicion_click[1] < 435):
                    print("b")
                    respuesta_usuario = "b"
                    if respuesta_usuario != respuesta_correcta:
                        intentos +=1
                elif (posicion_click[0] > 600 and posicion_click[0] < 750) and (posicion_click[1] > 385 and posicion_click[1] < 435):
                    print("c")
                    respuesta_usuario = "c"
                    if respuesta_usuario != respuesta_correcta:
                        intentos +=1

    if respuesta_usuario == respuesta_correcta:
        if flag_score == True:
            score +=10
            flag_score = False
        text_score = font.render(f"Score: {score}", True, COLOR_ROJO)
        usuario_correcta = True

    screen.fill(COLOR_AZUL)
    pygame.draw.rect(screen, COLOR_ROJO, (300, 20, 200, 100)) #Pos left, pos top, size left, size top
    pygame.draw.rect(screen, COLOR_ROJO, (550, 20, 200, 100))
    screen.blit(preguntados_pic, (0, 0))
    screen.blit(text_boton_pregunta, (300, 20))
    screen.blit(text_reiniciar, (550, 20))
    if posicion > 0 and usuario_correcta == False and intentos < 2:
        pygame.draw.rect(screen, COLOR_ROJO, (100, 385, 150, 50))
        pygame.draw.rect(screen, COLOR_ROJO, (350, 385, 150, 50))
        pygame.draw.rect(screen, COLOR_ROJO, (600, 385, 150, 50))
        screen.blit(text_opcion_a, (100, 400))
        screen.blit(text_opcion_b, (350, 400))
        screen.blit(text_opcion_c, (600, 400))
    screen.blit(text_pregunta, (250, 200))
    screen.blit(text_score, (50, 250))
    pygame.display.flip()

pygame.quit()