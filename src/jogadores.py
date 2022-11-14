import pygame

img_jogador = pygame.image.load('./data/nave.png')
img_alien = pygame.image.load('./data/red.png')
img_alien2 = pygame.image.load('./data/yellow.png')
img_alien3 = pygame.image.load('./data/green.png')
img_alien4 = pygame.image.load('./data/extra.png')


# Função que desenha o jogador/a nave
def desenha_jogador(x, y, screen):
    screen.blit(img_jogador, (x, y))  # Desenhar a imagem do jogador


# Função que desenha o inimigo/alien
def desenha_alien(x, y, type_alien, screen):
    if type_alien == "red":
        screen.blit(img_alien, (x, y))  # Desenhar a imagem do jogador
    elif type_alien == "yellow":
        screen.blit(img_alien2, (x, y))  # Desenhar a imagem do jogador
    elif type_alien == "green":
        screen.blit(img_alien3, (x, y))  # Desenhar a imagem do jogador
    else:
        screen.blit(img_alien4, (x, y))  # Desenhar a imagem do jogador