import math
import pygame

img_bala = pygame.image.load('./data/bullet.png')


# Estado em que a bala se encontra em movimento
def bala_em_movimento(x, y, screen):
    screen.blit(img_bala, (x + 16, y - 20))  # Desenhar a imagem da bala
    return 1


# Estado em que ocorre uma verificação se bala e alien colidem
def colisao(alienX, alienY, balaX, balaY):
    if alienY <= balaY <= alienY + 32 and alienX + 4 >= balaX >= alienX - 40:
        return True
    else:
        return False