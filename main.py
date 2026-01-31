import pygame

# 1. Inicialização
pygame.init()
pygame.font.init()

# 2. Configurações da Janela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Meu Primeiro Jogo")

# 3. Variáveis de Controle
rodando = True
relogio = pygame.time.Clock() # Controla a velocidade do jogo (FPS)
fonte = pygame.font.SysFont("arial", 30)
ataque_selecionado = 1
vida_personagem = 100
vida_vilão = 100
ganhou = False

# 4. Definição de cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
PRETO = (0, 0, 0)

# 5. FORMAS
x_retangulo, y_retangulo = 90, 550
retangulo_select = pygame.Rect(x_retangulo, y_retangulo, 100, 40)

# --- LOOP PRINCIPAL ---
while rodando:


    # A. Tratar Eventos (Entradas do usuário)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Clicou no 'X' da janela
            rodando = False

        if evento.type == pygame.KEYDOWN:

            if evento.key == pygame.K_RIGHT:

                ataque_selecionado = 2
                
            if evento.key == pygame.K_LEFT:

                ataque_selecionado = 1

            if evento.key == pygame.K_RETURN:

                if ganhou:

                    ganhou = False

                if (ataque_selecionado == 1):

                    vida_vilão -= 30

                elif (ataque_selecionado == 2):

                    vida_vilão -= 10
                
                # verificação da vida do vilão
                if (vida_vilão <= 0):

                    ganhou = True

    # B. Lógica do Jogo (Movimentação, colisões, etc.)

    # pegando a posição do meu mouse para ajudar no posicionamento das coisas na tela
    x_mouse, y_mouse = pygame.mouse.get_pos()
    
    # selecionar golpes na batalha
    if (ataque_selecionado == 1):

        retangulo_select.left -= 110

        if (retangulo_select.left < 90):

            retangulo_select.left = 90 # limite

    elif (ataque_selecionado == 2):

        retangulo_select.left += 110

        if (retangulo_select.left > 200):

            retangulo_select.left = 200 # limite

    # C. Desenhar na Tela
    tela.fill(BRANCO) # Pinta o fundo de cinza escuro (RGB)

    if not ganhou:
        # desenhando um círculo na posição do meu mouse para ajudar no posicionamento das coisas
        pygame.draw.circle(tela, VERDE, (x_mouse, y_mouse), 10, 2)
        
        # Desenha um círculo (Onde?, Cor, Posição, Raio)
        pygame.draw.circle(tela, VERDE, (largura//4, ((altura//3) * 2)), 50) # inimigo
        pygame.draw.circle(tela, VERMELHO, (((largura// 4) * 3), (altura // 3)), 50) ## inimigo

        # Desenha retângulo
        pygame.draw.rect(tela, VERMELHO, retangulo_select, 3)
        
        # desenhando texto na tela
        texto_ataque1 = fonte.render("chute", True, PRETO)
        tela.blit(texto_ataque1, (100, 552))

        texto_ataque2 = fonte.render("soco", True, PRETO)
        tela.blit(texto_ataque2, (210, 552))

        # desenhando a vida
        texto_vida_personagem = fonte.render(f"Vida: {vida_personagem}", True, PRETO)
        tela.blit(texto_vida_personagem, (40, 300))

        texto_vida_personagem = fonte.render(f"Vida: {vida_vilão}", True, PRETO)
        tela.blit(texto_vida_personagem, (560, 75))

        # desenhando a posição do mouse
        texto_pos = fonte.render(f"Posição: X: {x_mouse}  Y: {y_mouse}", True, PRETO)
        tela.blit(texto_pos, (10, 10))

    else:

        texto_vitoria = fonte.render("Parabéns, você ganhou!", True, VERDE)
        tela.blit(texto_vitoria, (largura // 2, altura // 2))

    # D. Atualizar a tela
    pygame.display.flip()

    # E. Limitar FPS (60 quadros por segundo)
    relogio.tick(60)

# 4. Finalização
pygame.quit()