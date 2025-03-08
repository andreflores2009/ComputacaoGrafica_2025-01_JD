import pygame  # Importa a biblioteca Pygame para gerenciar gráficos e entrada do usuário
from pygame.locals import *  # Importa constantes do Pygame para eventos de teclado e mouse
from OpenGL.GL import *  # Importa funções do OpenGL para renderização gráfica
from OpenGL.GLUT import *  # Importa GLUT para utilitários gráficos do OpenGL
from OpenGL.GLU import *  # Importa GLU para operações gráficas auxiliares

# Variáveis de posição do triângulo
x = -1.5  # Posição inicial no eixo X
y = 0  # Posição inicial no eixo Y
r = 0  # Ângulo de rotação do triângulo

# Variáveis de escala (tamanho do triângulo)
ex = 1  # Escala no eixo X
ey = 1  # Escala no eixo Y
ez = 1  # Escala no eixo Z (não afeta 2D)

# Função de inicialização do OpenGL
def init():
    glClearColor(0, 0, 1, 1)  # Define a cor de fundo azul (R=0, G=0, B=1, A=1)
    glClearDepth(1.0)  # Define a profundidade máxima para renderização
    glEnable(GL_DEPTH_TEST)  # Habilita o teste de profundidade para ocultação de objetos
    glDepthFunc(GL_LEQUAL)  # Define o tipo de teste de profundidade
    glShadeModel(GL_SMOOTH)  # Habilita sombreamento suave
    glMatrixMode(GL_PROJECTION)  # Define a matriz de projeção (perspectiva)
    glLoadIdentity()  # Reinicializa a matriz de projeção
    gluPerspective(45, 640/480, 0.1, 100)  
    # gluPerspective(fov, aspectRatio, near, far)
    # 45 → Campo de visão (FOV) em graus
    # 640/480 → Razão de aspecto (largura/altura da tela)
    # 0.1 → Distância mínima de renderização (near plane)
    # 100 → Distância máxima de renderização (far plane)
    
    glMatrixMode(GL_MODELVIEW)  # Define a matriz de visualização

# Função para desenhar o triângulo
def draw():
    glLoadIdentity()  # Reinicia a matriz de visualização para evitar acúmulo de transformações

    # Aplica transformações (movimentação, rotação e escala)
    glTranslatef(x, y, -6)  
    # glTranslatef(transX, transY, transZ)
    # x → deslocamento no eixo X (horizontal: esquerda/direita)
    # y → deslocamento no eixo Y (vertical: cima/baixo)
    # -6 → deslocamento no eixo Z (afasta ou aproxima da tela)

    glRotatef(r, 0, 1, 0)  
    # glRotatef(angle, axisX, axisY, axisZ)
    # r → ângulo de rotação em graus
    # 0 → não rotaciona no eixo X
    # 1 → rotaciona no eixo Y (gira horizontalmente)
    # 0 → não rotaciona no eixo Z

    glScalef(ex, ey, ez)  
    # glScalef(scaleX, scaleY, scaleZ)
    # ex → escala no eixo X (alarga ou reduz horizontalmente)
    # ey → escala no eixo Y (estica ou reduz verticalmente)
    # ez → escala no eixo Z (não afeta em 2D, pois Z é fixo)

    # Inicia a definição do triângulo
    glBegin(GL_TRIANGLES)
    glColor3f(1, 1, 0)  # Define a cor do triângulo como amarelo (R=1, G=1, B=0)
    glVertex3f(0, 1, 0)  # Define o vértice superior
    glVertex3f(-1, -1, 0)  # Define o vértice inferior esquerdo
    glVertex3f(1, -1, 0)  # Define o vértice inferior direito
    glEnd()  # Finaliza a definição do triângulo

# Função principal do programa
def main():
    pygame.init()  # Inicializa o Pygame
    pygame.display.set_mode((640, 480), DOUBLEBUF | OPENGL)  
    # Cria a janela com buffer duplo (DOUBLEBUF) e suporte OpenGL (OPENGL)
    init()  # Chama a função de inicialização do OpenGL

    global x, y, r, ex, ey, ez  # Declara as variáveis globais para uso dentro da função

    running = True  # Variável de controle do loop principal
    while running:
        for event in pygame.event.get():  # Captura eventos do sistema (teclado, mouse, etc.)
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                running = False  # Sai do loop e encerra o programa
            if event.type == KEYDOWN:  # Se uma tecla for pressionada
                if event.key == K_ESCAPE:  # Se a tecla ESC for pressionada
                    running = False  # Sai do loop e fecha o programa
                if event.key == K_a:  # Se a tecla A for pressionada
                    x += -0.2  # Move o triângulo para a esquerda
                if event.key == K_d:  # Se a tecla D for pressionada
                    x += 0.2  # Move o triângulo para a direita
                if event.key == K_w:  # Se a tecla W for pressionada
                    y += 0.2  # Move o triângulo para cima
                if event.key == K_s:  # Se a tecla S for pressionada
                    y += -0.2  # Move o triângulo para baixo
            if event.type == MOUSEBUTTONDOWN:  # Se o usuário rolar o mouse
                if event.button == 4:  # Scroll para cima
                    ex += 0.2  # Aumenta a escala do triângulo no eixo X
                    ey += 0.2  # Aumenta a escala do triângulo no eixo Y
                    ez += 0.2  # Aumenta a escala do triângulo no eixo Z (não afeta 2D)
                if event.button == 5:  # Scroll para baixo
                    ex -= 0.2  # Diminui a escala do triângulo no eixo X
                    ey -= 0.2  # Diminui a escala do triângulo no eixo Y
                    ez -= 0.2  # Diminui a escala do triângulo no eixo Z (não afeta 2D)
                    
        # Limpa a tela e o buffer de profundidade antes de desenhar
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Chama a função que desenha o triângulo
        draw()

        # Atualiza a tela com a nova renderização
        pygame.display.flip()

        # Aguarda um pequeno tempo para suavizar a execução
        pygame.time.wait(10)

        # Atualiza o ângulo de rotação para dar efeito de giro contínuo
        r += 3  

    pygame.quit()  # Finaliza o Pygame quando o loop termina

# Executa o programa se ele for chamado diretamente
if __name__ == "__main__":
    main()
