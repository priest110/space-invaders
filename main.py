import random

import pygame
from pygame.locals import *
import time
from threading import Thread

import estados
import jogadores

img_explosao = pygame.image.load('explosion.png')

# Ícones: flaticon, Imagens: freepik

# Inicializa o pygame
pygame.init()

# Background
back = pygame.image.load('invaders.jpg')

# Mudar o title e ícone
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('game.png')
pygame.display.set_icon(icone)

# Desenhar a janela
screen = pygame.display.set_mode(size=(800, 600))

# Jogador
jogadorX = 370
jogadorY = 480
jogadorX_change = 0

# Aliens por nível
niveis = [6, 8, 10, 15]

# Aliens
alienX = [[]]
alienY = [[]]
alienY_change = [[]]
alienX_change = [[]]

for n in niveis:
    for i in range(n):
        print(i)
        print(n)
        alienX[i].append(random.randint(0, 736))
        alienY[i].append(random.randint(50, 200))
        alienX_change[i].append(1)
        alienY_change[i].append(40)

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
                jogadorX_change = -2
            if evento.key == pygame.K_RIGHT:  # Pressionar a seta direita
                jogadorX_change = 2
            if evento.key == pygame.K_SPACE:  # Pressionar espaço
                if bala_estado == 0:
                    balaX = jogadorX  # Pega na coordenadaX da nave
                    balaY = 480
                    bala_estado = estados.dispara_bala(balaX, balaY, screen)
        if evento.type == KEYUP:  # Deixar de pressionar uma tecla
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jogadorX_change = 0  # Para imobilizar a nave

    # Checkar as bordas, para não sair nenhum elemento da janela
    jogadorX += jogadorX_change
    if jogadorX <= 0:
        jogadorX = 0
    elif jogadorX >= 736:  # 800px da janela - 64px da figura
        jogadorX = 736

    alienX += alienX_change
    if alienX <= 0:
        alienX_change = 1
        alienY += alienY_change
    elif alienX >= 736:  # 800px da janela - 64px da figura
        alienX_change = -1
        alienY += alienY_change

    if balaY <= 0:
        bala_estado = 0
        balaY = 600

    # Movimento da bala, após disparada
    if bala_estado == 1:
        bala_estado = estados.dispara_bala(balaX, balaY, screen)
        balaY -= balaY_change

    colisao = estados.colisao(alienX, alienY, balaX, balaY)

    # Verifica se há colisão
    if colisao:
        bala_estado = 0
        balaY = 480
        score += 1
        explosaoX = alienX
        explosaoY = alienY
        alienX = random.randint(0, 736)
        alienY = random.randint(50, 200)
        tempo_explosao = time.time()
        print("\nQue fixe, mataste um gajo.\nScore = ", score)
        explosao = True

    # Verifica se há colisão
    if explosao:
        if time.time() - tempo_explosao < 0.1:
            screen.blit(img_explosao, (explosaoX, explosaoY))  # Desenhar a explosão
        else:
            explosao = False  # Cancelar a explosão

    # Verifica se é game over
    if alienY > 480:
        running = False

    jogadores.desenha_alien(alienX, alienY, screen)
    jogadores.desenha_jogador(jogadorX, jogadorY, screen)
    pygame.display.update()

running = True
while running:
    print("Game over")
    screen.fill((0, 0, 0))  # Cor do background (R, G, B)
    screen.blit(icone, (0, 0))  # Img do background
    pygame.display.update()
