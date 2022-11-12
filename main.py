import random

import pygame
from pygame.locals import *
import time

from src import jogadores, estados

img_explosao = pygame.image.load('./data/explosion.png')

# Inicializa o pygame
pygame.init()

# ATRIBUIÇÕES INICIAIS

# Janela, background, título e ícone
back = pygame.image.load('./data/background.jpg')
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('./data/game.png')
pygame.display.set_icon(icone)
screen = pygame.display.set_mode(size=(800, 600))

# Jogadores
jogadorX = 470
jogadorY = 500
jogadorX_change = 0
alienX = []
alienY = []
alienX_change = []
alienY_change = []

# Bala
balaX = 0
balaY = 700
balaX_change = 0
balaY_change = 1
bala_estado = 0  # 0 caso ainda não tenha sido disparada, 1 caso tenha sido

# Explosão
explosaoX = 0
explosaoY = 0
explosao_estado = 0  # 0 caso ainda não tenha acontecido, 1 caso tenha acontecido

# Níveis do jogo
niveis = [30, 40, 50, 51]  # 4 níveis com os aliens respetivos
nivel_atual = 0
aliens_vivos = niveis[nivel_atual]
for n in niveis:
    auxX = []
    auxY = []
    coordX = 200      # coordenada X onde surge o primeiro alien
    coordY = 100 - 40 * nivel_atual     # coordenada Y onde surge o primeiro alien da coordenada x
    auxX_change = []
    auxY_change = []
    for i in range(n):
        if i < 30:
            auxX.append(coordX)
            auxY.append(coordY)
            auxX_change.append(0.1)
            auxY_change.append(40)
        elif i < 40:
            auxX.append(coordX)
            auxY.append(coordY)
            auxX_change.append(0.1)
            auxY_change.append(40)
        elif i < 50:
            auxX.append(coordX)
            auxY.append(coordY)
            auxX_change.append(0.1)
            auxY_change.append(40)
        else:
            auxX.append(coordX)
            auxY.append(coordY)
            auxX_change.append(0.1)
            auxY_change.append(40)

        if coordX < 740:
            coordX += 60
        else:
            coordX = 200
            coordY += 40

    alienX.append(auxX)
    alienY.append(auxY)
    alienX_change.append(auxX_change)
    alienY_change.append(auxY_change)

# COMEÇO DO JOGO

score = 0
running = True
colisao = False
explosao = False
tempo_explosao = time.time()

while running:
    screen.fill((0, 0, 0))  # Cor do background (R, G, B)
    screen.blit(back, (0, 0))  # Img do background
    for evento in pygame.event.get():
        if evento.type == QUIT:
            running = False
        if evento.type == KEYDOWN:  # Pressionar uma tecla
            if evento.key == pygame.K_LEFT:  # Pressionar a seta esquerda
                jogadorX_change = -1
            if evento.key == pygame.K_RIGHT:  # Pressionar a seta direita
                jogadorX_change = 1
            if evento.key == pygame.K_SPACE:  # Pressionar espaço
                if bala_estado == 0:
                    balaX = jogadorX  # Pega na coordenadaX da nave
                    balaY = 500
                    bala_estado = estados.bala_em_movimento(balaX, balaY, screen)
        if evento.type == KEYUP:  # Deixar de pressionar uma tecla
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jogadorX_change = 0  # Para imobilizar a nave

    # Verifica se o jogador pode sair das bordas
    jogadorX += jogadorX_change
    if jogadorX <= 0:
        jogadorX = 0
    elif jogadorX >= 736:
        jogadorX = 736

    # Verifica o movimento de cada alien
    #   - Saída das bordas
    #   - Colisão com bala
    #   - Game over
    i = 0
    while i < aliens_vivos:
        alienX[nivel_atual][i] += alienX_change[nivel_atual][i]
        if alienX[nivel_atual][i] <= 0:
            for j in range(niveis[nivel_atual]):
                alienX_change[nivel_atual][j] = 0.1
                alienY[nivel_atual][j] += alienY_change[nivel_atual][i]
        elif alienX[nivel_atual][i] >= 760:
            for j in range(niveis[nivel_atual]):
                alienX_change[nivel_atual][j] = -0.1
                alienY[nivel_atual][j] += alienY_change[nivel_atual][i]

        colisao = estados.colisao(alienX[nivel_atual][i], alienY[nivel_atual][i], balaX, balaY)
        if colisao:
            bala_estado = 0
            balaY = 700
            score += 1
            explosaoX = alienX[nivel_atual][i]
            explosaoY = alienY[nivel_atual][i]
            alienX[nivel_atual].pop(i)
            alienY[nivel_atual].pop(i)
            alienX_change[nivel_atual].pop(i)
            alienY_change[nivel_atual].pop(i)
            aliens_vivos -= 1
            tempo_explosao = time.time()
            print("\nQue fixe, mataste um gajo.\nScore = ", score)
            explosao = True

        if alienY[nivel_atual][i] > 480:
            running = False

        jogadores.desenha_alien(alienX[nivel_atual][i], alienY[nivel_atual][i], screen)
        i += 1

    # Verifica se a bala pode sair das bordas
    if balaY <= 0:
        bala_estado = 0
        balaY = 500

    # Movimento da bala, após disparada
    if bala_estado == 1:
        bala_estado = estados.bala_em_movimento(balaX, balaY, screen)
        balaY -= balaY_change

    # Verifica se houve colisão
    if explosao:
        if time.time() - tempo_explosao < 0.1:
            screen.blit(img_explosao, (explosaoX, explosaoY))  # Desenhar a explosão
        else:
            explosao = False  # Cancelar a explosão

    jogadores.desenha_jogador(jogadorX, jogadorY, screen)
    pygame.display.update()

# FIM DO JOGO

running = True
while running:
    print("Game over")
    screen.fill((0, 0, 0))  # Cor do background (R, G, B)
    screen.blit(icone, (0, 0))  # Img do background
    pygame.display.update()
