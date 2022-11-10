import pygame

img_jogador = pygame.image.load('./data/nave.png')
img_alien = pygame.image.load('./data/alien.png')


# Função que desenha o jogador/a nave
def desenha_jogador(x, y, screen):
    screen.blit(img_jogador, (x, y))  # Desenhar a imagem do jogador


# Função que desenha o inimigo/alien
def desenha_alien(x, y, screen):
    screen.blit(img_alien, (x, y))  # Desenhar a imagem do jogador
