# -*- coding: utf-8 -*-
import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()
ventana = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Hola Mundo")

# miFuente = pygame.font.Font(None, 30)
# miTexto = miFuente.render("ARIAL", 0, (45, 75, 96), (255, 255, 255))

Fuente = pygame.font.SysFont("Arial", 30)
# miTexto2 = Fuente.render("MARIO MMG :3", 3, (45, 75, 96), (255, 255, 255))

"""Dibujo de figurasgeometricas"""
# pygame.draw.rect(ventana, (90, 90, 90), (300, 74, 69, 7))
# # pygame.draw.circle( ventana, (90, 90, 90), (75, 100), 45)
# pygame.draw.polygon( ventana, (90, 90, 90), ( (90, 20), (45, 50), (80, 90), (100, 60) ) )

"""Creación de rectangulos"""
# rectangulo_dos = pygame.Rect(200,200, 100, 50)
# posX, posY = 200, 100
# velocidad = 0.1
# derecha = True
# rectangulo = pygame.Rect(0,0, 100, 50)
blanco = (0, 0, 0)
aux = 1
while True:
    """Dibujos de rectangulos"""
    ventana.fill(blanco)
    tiempo = pygame.time.get_ticks()/1000
    if aux == tiempo:
        aux += 1
        print( tiempo )
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()


    # pygame.draw.rect(ventana, (0, 0, 0), rectangulo_dos)
    # pygame.draw.rect(ventana, (0, 0, 0), rectangulo)
    # rectangulo.left, rectangulo.top = pygame.mouse.get_pos()
    """Colisión de rectangulos"""
    # if rectangulo.colliderect(rectangulo_dos):
    #     velocidad = 0
    #     print ("Colisionó")

    """Movimiento de rectangulos"""
    # if ( derecha == True ):
    #     if posX < 550:
    #         posX += velocidad
    #         rectangulo_dos.left = posX
    #     else:
    #         derecha = False
    # else:
    #     if (posX > 1):
    #         posX -= velocidad
    #         rectangulo_dos.left = posX
    #     else:
    #         derecha = True

        # if event.type == pygame.KEYDOWN:
        #     if event.key == K_LEFT:
        #         posX -= velocidad
        #
        #     if event.key == K_RIGHT:
        #         posX += velocidad
        #
        #     if event.key == K_UP:
        #         posY -= velocidad
        #
        #     if event.key == K_DOWN:
        #         posY += velocidad

    contador = Fuente.render("Tiempo: " + str(tiempo), 0, (120, 70, 0))
    ventana.blit(contador, (100, 100))
    # ventana.blit(miTexto2, (100, 100))
    # ventana.blit(miTexto, (200, 200))
    pygame.display.update()
