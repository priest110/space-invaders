import random

import pygame
from pygame.locals import *
import time

from src import jogadores, estados

img_explosao = pygame.image.load('./data/explosion.png')

# Inicializa o pygame
pygame.init()

# Background
back = pygame.image.load('./data/invaders.jpg')

# Mudar o title e ícone
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('./data/game.png')
pygame.display.set_icon(icone)

# Desenhar a janela
screen = pygame.display.set_mode(size=(800, 600))

# Jogador
jogadorX = 370
jogadorY = 480
jogadorX_change = 0

# Aliens
alienX = []
alienY = []
alienX_change = []
alienY_change = []

# Níveis do jogo
niveis = [6, 8, 10, 15]  # aliens por nível
for n in niveis:
    auxX = []
    auxY = []
    auxX_change = []
    auxY_change = []
    for i in range(n):
        auxX.append(random.randint(0, 736))
        auxY.append(random.randint(50, 200))
        auxX_change.append(1)
        auxY_change.append(40)
    alienX.append(auxX)
    alienY.append(auxY)
    alienX_change.append(auxX_change)
    alienY_change.append(auxY_change)

# Bala
balaX = 0
balaY = 600
balaX_change = 0
balaY_change = 3
bala_estado = 0  # 0 caso ainda não tenha sido disparada, 1 caso tenha sido

# Explosão
explosaoX = 0
explosaoY = 0
explosao_estado = 0  # 0 caso ainda não tenha acontecido, 1 caso tenha acontecido

# Inicializa jogo
score = 0
nivel_atual = 0
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
                    balaY = 480
                    bala_estado = estados.dispara_bala(balaX, balaY, screen)
        if evento.type == KEYUP:  # Deixar de pressionar uma tecla
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jogadorX_change = 0  # Para imobilizar a nave

    # Verifica se o jogador pode sair das bordas
    jogadorX += jogadorX_change
    if jogadorX <= 0:
        jogadorX = 0
    elif jogadorX >= 736:  # 800px da janela - 64px da figura
        jogadorX = 736

    # Verifica o movimento de cada alien
    #   - Saída das bordas
    #   - Colisão com bala
    #   - Game over
    for i in range(niveis[nivel_atual]):
        alienX[nivel_atual][i] += alienX_change[nivel_atual][i]
        if alienX[nivel_atual][i] <= 0:
            alienX_change[nivel_atual][i] = 0.5
            alienY[nivel_atual][i] += alienY_change[nivel_atual][i]
        elif alienX[nivel_atual][i] >= 736:
            alienX_change[nivel_atual][i] = -0.5
            alienY[nivel_atual][i] += alienY_change[nivel_atual][i]

        colisao = estados.colisao(alienX[nivel_atual][i], alienY[nivel_atual][i], balaX, balaY)
        if colisao:
            bala_estado = 0
            balaY = 480
            score += 1
            explosaoX = alienX
            explosaoY = alienY
            alienX[nivel_atual][i] = random.randint(0, 736)
            alienY[nivel_atual][i] = random.randint(50, 200)
            tempo_explosao = time.time()
            print("\nQue fixe, mataste um gajo.\nScore = ", score)
            explosao = True

        if alienY[nivel_atual][i] > 480:
            running = False

        jogadores.desenha_alien(alienX[nivel_atual][i], alienY[nivel_atual][i], screen)

    # Verifica se a bala pode sair das bordas
    if balaY <= 0:
        bala_estado = 0
        balaY = 600

    # Movimento da bala, após disparada
    if bala_estado == 1:
        bala_estado = estados.dispara_bala(balaX, balaY, screen)
        balaY -= balaY_change

    # Verifica se houve colisão
    if explosao:
        if time.time() - tempo_explosao < 0.1:
            screen.blit(img_explosao, (explosaoX, explosaoY))  # Desenhar a explosão
        else:
            explosao = False  # Cancelar a explosão

    jogadores.desenha_jogador(jogadorX, jogadorY, screen)
    pygame.display.update()

running = True
while running:
    print("Game over")
    screen.fill((0, 0, 0))  # Cor do background (R, G, B)
    screen.blit(icone, (0, 0))  # Img do background
    pygame.display.update()
