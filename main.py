# coding=utf-8

import pygame
from pygame.locals import *
import time

from src import interface

# Constrói a GUI
pygame.init()

# ATRIBUIÇÕES INICIAIS

# Janela, background, título e ícone
screen = pygame.display.set_mode(size=(800, 600))
back = pygame.image.load('./data/background.jpg')
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('./data/game.png')
pygame.display.set_icon(icone)

# Jogadores
jogador = {
    "coordX": 470,
    "coordY": 500,
    "changeX": 20
}
aliens = []

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
niveis = [20, 30, 40, 41]  # 4 níveis com os aliens respetivos
nivel_atual = 0  # inicialmente é o 0
aliens_vivos = niveis[nivel_atual]  # inicialmente é 30, correspondente ao nível inicial


# Verificação de colisão entre bala e alien
def existe_colisao(alienX, alienY, balaX, balaY):
    if alienY <= balaY <= alienY + 32 and alienX + 4 >= balaX >= alienX - 40:
        return True
    else:
        return False


# Atribuição das coordenadas a todos os aliens dos respetivos níveis
def coordenadas_aliens():
    for n in niveis:
        coordX = 200  # coordenada X onde surge o primeiro alien
        coordY = 100 + 40 * niveis.index(n)  # coordenada Y onde surge o primeiro alien da coordenada x
        aliens_aux = []
        for i in range(n):
            alien = {
                "coordX": coordX,
                "coordY": coordY,
                "changeX": 0.1 if i < 30 else 0.3 if i < 40 else 0.5,
                # A partir dos 3º nível (30 aliens >) a velocidadeno eixo x dos mesmos altera
                "changeY": 40 if i < 30 else 0,
                "type": "red" if i < 20 else "yellow" if i < 30 else "green" if i < 40 else "extra"
                # O tipo de alien varia consoante o nível
            }
            aliens_aux.append(alien)
            if coordX < 740:
                coordX += 60
            else:
                coordX = 200
                coordY -= 40
        aliens.append(aliens_aux)


# COMEÇO DO JOGO

score = 0
font = pygame.font.Font('./data/space_invaders.ttf', 32)
running = True
game_over = False
colisao = False
explosao = False
tempo_explosao = time.time()

coordenadas_aliens()
while running:
    screen.fill((0, 0, 0))  # Cor do background (R, G, B)
    screen.blit(back, (0, 0))  # Img do background
    for evento in pygame.event.get():
        if evento.type == QUIT:
            running = False
        if evento.type == KEYDOWN:  # Pressionar uma tecla
            if evento.key == pygame.K_LEFT:  # Pressionar a seta esquerda
                jogador["changeX"] = -1
            if evento.key == pygame.K_RIGHT:  # Pressionar a seta direita
                jogador["changeX"] = 1
            if evento.key == pygame.K_SPACE:  # Pressionar espaço
                if bala_estado == 0:
                    balaX = jogador["coordX"]  # Pega na coordenadaX da nave
                    balaY = 500
                    bala_estado = interface.desenha_bala(balaX, balaY, screen)
        if evento.type == KEYUP:  # Deixar de pressionar uma tecla
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jogador["changeX"] = 0  # Para imobilizar a nave

    # Verifica se o jogador pode sair das bordas
    jogador["coordX"] += jogador["changeX"]
    if jogador["coordX"] <= 0:
        jogador["coordX"] = 0
    elif jogador["coordX"] >= 736:
        jogador["coordX"] = 736

    # Verifica o movimento de cada alien
    #   - Saída das bordas
    #   - Colisão com bala
    #   - Game over
    i = 0
    while i < aliens_vivos and not game_over:
        aliens[nivel_atual][i]["coordX"] += aliens[nivel_atual][i]["changeX"]

        if 760 <= aliens[nivel_atual][i]["coordX"] or aliens[nivel_atual][i]["coordX"] <= 0:
            for j in range(aliens_vivos):
                type_i = aliens[nivel_atual][i]["type"]
                type_j = aliens[nivel_atual][j]["type"]
                if (type_i in ["red", "yellow"] and type_j in ["red", "yellow"]) or (
                        type_i in ["green"] and type_j in ["green"]) or (type_i in ["extra"] and type_j in ["extra"]):
                    aliens[nivel_atual][j]["changeX"] = -aliens[nivel_atual][j]["changeX"]
                if type_i in ["red", "yellow"] and type_j in ["red", "yellow"]:
                    aliens[nivel_atual][j]["coordY"] += aliens[nivel_atual][j]["changeY"]

        colisao = existe_colisao(aliens[nivel_atual][i]["coordX"], aliens[nivel_atual][i]["coordY"], balaX, balaY)
        if colisao:
            bala_estado = 0
            balaY = 700
            score += 1
            explosaoX = aliens[nivel_atual][i]["coordX"]
            explosaoY = aliens[nivel_atual][i]["coordY"]
            aliens[nivel_atual].pop(i)
            aliens_vivos -= 1
            if aliens_vivos == 0:
                nivel_atual += 1
                if nivel_atual < len(niveis):
                    aliens_vivos = niveis[nivel_atual]
                else:
                    running = False
                    game_over = True
            tempo_explosao = time.time()
            print("\nQue fixe, mataste um gajo.\nScore = ", score)
            explosao = True
        elif aliens[nivel_atual][i]["coordY"] > 480:
            running = False
            game_over = True
        else:
            interface.desenha_alien(aliens[nivel_atual][i]["coordX"], aliens[nivel_atual][i]["coordY"],
                                    aliens[nivel_atual][i]["type"], screen)
            i += 1

    # Verifica se a bala pode sair das bordas
    if balaY <= 0:
        bala_estado = 0
        balaY = 500

    # Movimento da bala, após disparada
    if bala_estado == 1:
        bala_estado = interface.desenha_bala(balaX, balaY, screen)
        balaY -= balaY_change

    # Verifica se houve colisão
    if explosao:
        if time.time() - tempo_explosao < 0.1:
            interface.desenha_explosao(explosaoX, explosaoY, screen)
        else:
            explosao = False  # Cancelar a explosão

    interface.desenha_jogador(jogador["coordX"], jogador["coordY"], screen)
    interface.desenha_score(10, 10, score, screen, font)
    pygame.display.update()

# FIM DO JOGO

running = True
while running:
    print("Game over")
    screen.fill((0, 0, 0))  # Cor do background (R, G, B)
    screen.blit(icone, (0, 0))  # Img do background
    pygame.display.update()
