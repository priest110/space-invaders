import math
import time

import pygame
from time import perf_counter, sleep

img_bala = pygame.image.load('bullet.png')
img_explosao = pygame.image.load('explosion.png')


# Jogador dispara bala
def dispara_bala(x, y, screen):
    screen.blit(img_bala, (x + 16, y - 20))  # Desenhar a imagem da bala
    return 1

# Verifica se bala e alien colidem
def colisao(alienX, alienY, balaX, balaY):
    distancia = math.sqrt(math.pow(alienX - balaX, 2) + math.pow(alienY - balaY, 2))
    if distancia < 27:  # 27 px
        return True
    else:
        return False
