import pygame

img_jogador = pygame.image.load('./data/nave.png')
img_alien = pygame.image.load('./data/red.png')
img_alien2 = pygame.image.load('./data/yellow.png')
img_alien3 = pygame.image.load('./data/green.png')
img_alien4 = pygame.image.load('./data/extra.png')
img_explosao = pygame.image.load('./data/explosion.png')
img_bala = pygame.image.load('./data/bullet.png')


# Função que desenha o jogador/a nave
def desenha_jogador(x, y, screen):
    screen.blit(img_jogador, (x, y))


# Função que desenha o inimigo/alien
def desenha_alien(x, y, type_alien, screen):
    if type_alien == "red":
        screen.blit(img_alien, (x, y))
    elif type_alien == "yellow":
        screen.blit(img_alien2, (x, y))
    elif type_alien == "green":
        screen.blit(img_alien3, (x, y))
    else:
        screen.blit(img_alien4, (x, y))


def desenha_score(x, y, score_val, screen, font):
    score = font.render("Score: " + str(score_val), True, (51, 255, 176))
    screen.blit(score, (x, y))


def desenha_explosao(x, y, screen):
    screen.blit(img_explosao, (x, y))


def desenha_bala(x, y, screen):
    screen.blit(img_bala, (x + 16, y - 20))
    return 1
