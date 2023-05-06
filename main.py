# coding=utf-8

import pygame
from pygame.locals import *
import time

from src import interface

# Constrói a GUI
pygame.init()

# ATRIBUIÇÕES INICIAIS

# Janela, background, título e ícone
screen_width = 800 
screen_height = 600
screen = pygame.display.set_mode(size=(screen_width, screen_height))
back = pygame.image.load('./data/background.jpg')
pygame.display.set_caption("Space Invaders")
icone = pygame.image.load('./data/game.png')
icone_width, icone_height = icone.get_size()
icone_pos_x = (screen_width-icone_width) / 2
icone_pos_y = (screen_height-icone_height) / 2
pygame.display.set_icon(icone)
game_state = "menu"

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

# Gerir os cliques do rato
def handle_mouse_click(position):
    global game_state

    if game_state == "menu":
        # Check if the click occurred on the "play" button
        if 150 <= position[0] <= 350 and 250 <= position[1] <= 300:
            game_state = "playing"
            start_game()

        # Check if the click occurred on the "quit" button
        elif 150 <= position[0] <= 350 and 350 <= position[1] <= 400:
            pygame.quit()
            sys.exit()

# COMEÇO DO JOGO

# Codigo do menu
def menu(screen):
    font = pygame.font.Font('./data/space_invaders.ttf', 64)
    title = font.render("Space Invaders", True, (255, 255, 255))
    play_text = font.render("Play", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))

    # Center the title and menu options
    title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
    play_rect = play_text.get_rect(center=(screen.get_width() // 2, 300))
    quit_rect = quit_text.get_rect(center=(screen.get_width() // 2, 400))

    while True:
    # Draw the title and menu options
        screen.fill((0, 0, 0))
        screen.blit(title, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                handle_mouse_click(pygame.mouse.get_pos())
                # Check which option was selected
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    return True
                elif quit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        

            # Highlight the selected option
            if play_rect.collidepoint(pygame.mouse.get_pos()):
                play_text = font.render("Play", True, (255, 0, 0))
            else:
                play_text = font.render("Play", True, (255, 255, 255))

            if quit_rect.collidepoint(pygame.mouse.get_pos()):
                quit_text = font.render("Quit", True, (255, 0, 0))
            else:
                quit_text = font.render("Quit", True, (255, 255, 255))

            pygame.display.update()



# Inicialização do menu
if not menu(screen):
    pygame.quit()
    sys.exit()

# Loop do jogo

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
    screen.blit(icone, (icone_pos_x, icone_pos_y))  # Img do background
    pygame.display.update()
    time.sleep(5)
    running = False
    

