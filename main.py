import pygame

pygame.init()
pygame.mixer.init()

largura, altura = 540, 960
tela = pygame.display.set_mode((largura, altura))

preto = (0, 0, 0)
roxo = (104, 15, 131)
cinza_claro = (165, 80, 191)

raio_bola = 5
x, y = largura // 2, altura // 2
velocidade_x, velocidade_y = 5, 5

rastros = []

som_colisao = pygame.mixer.Sound('som.wav')

def att_bola(raio_bola, velocidade_x, velocidade_y):
    raio_bola += 3
    velocidade_x *= 1.05
    velocidade_y *= 1.05

    # limita a velocidade
    if velocidade_y >= 40:
        velocidade_y = 40
    elif velocidade_x >= 40:
        velocidade_x = 40
    # limita o raio
    elif raio_bola >= 1100:
        pygame.quit()

    return raio_bola, velocidade_x, velocidade_y

def tocar_som_rapido(velocidade_x, velocidade_y, som):
    frequencia = int((abs(velocidade_x) + abs(velocidade_y)) / 100)
    if frequencia < 1:
        frequencia = 1

    for _ in range(frequencia):
        som.play()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    rastros.append((x, y, raio_bola))

    # Move a bola
    x += velocidade_x
    y += velocidade_y

    colisao = False # Verifica colisões com as bordas da tela

    if x - raio_bola < 0:
        velocidade_x = -velocidade_x
        raio_bola, velocidade_x, velocidade_y = att_bola(raio_bola, velocidade_x, velocidade_y)
        x = raio_bola  # Reposiciona a bola dentro da tela
        colisao = True

    elif x + raio_bola > largura:
        velocidade_x = -velocidade_x
        raio_bola, velocidade_x, velocidade_y = att_bola(raio_bola, velocidade_x, velocidade_y)
        x = largura - raio_bola  # Reposiciona a bola dentro da tela
        colisao = True

    if y - raio_bola < 0:
        velocidade_y = -velocidade_y
        raio_bola, velocidade_x, velocidade_y = att_bola(raio_bola, velocidade_x, velocidade_y)
        y = raio_bola  # Reposiciona a bola dentro da tela
        colisao = True

    elif y + raio_bola > altura:
        velocidade_y = -velocidade_y
        raio_bola, velocidade_x, velocidade_y = att_bola(raio_bola, velocidade_x, velocidade_y)
        y = altura - raio_bola  # Reposiciona a bola dentro da tela
        colisao = True

    if colisao:
        tocar_som_rapido(velocidade_x, velocidade_y, som_colisao)

    tela.fill(preto)

    for i, (rx, ry, rraio) in enumerate(rastros):
        pygame.draw.circle(tela, cinza_claro, (int(rx), int(ry)), int(rraio), 1)

    pygame.draw.circle(tela, roxo, (int(x), int(y)), int(raio_bola))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

    if len(rastros) > 50:
        rastros.pop(0)