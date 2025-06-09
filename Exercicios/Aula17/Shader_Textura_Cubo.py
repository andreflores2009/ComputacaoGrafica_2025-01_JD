# -*- coding: utf-8 -*-
"""
Exemplo: cubo texturizado que pulsa de verde para vermelho no tempo
Usa OpenGL 4.0 core em Python (PyOpenGL + GLFW + Pyrr)
Padronizado: inicializa_opengl(), inicializa_shaders(), inicializa_resources(), render_loop(), main()
Inclui movimentação de câmera com WSAD.
"""
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
from PIL import Image
import time
import pyrr
import ctypes

# --- Parâmetros da janela e variáveis globais ---
WIDTH, HEIGHT = 800, 600           # resolução da janela
window = None                      # handle da janela GLFW
program = None                     # ID do programa de shaders
vao = None                         # ID do VAO do cubo
texture_id = None                  # ID da textura carregada
start_time = None                  # hora de início para animação
# vetores de câmera
cam_pos = pyrr.Vector3([0.0,0.0,3.0])
cam_front = pyrr.Vector3([0.0,0.0,-1.0])
cam_up = pyrr.Vector3([0.0,1.0,0.0])

# ---------- Inicialização do contexto OpenGL ----------
def inicializa_opengl():
    """Inicia GLFW, cria janela e contexto OpenGL."""
    global window
    if not glfw.init():
        raise RuntimeError("Falha ao inicializar GLFW")
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(WIDTH, HEIGHT, "Cubo Colorido", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Falha ao criar janela GLFW")
    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)             # ativa teste de profundidade

# ---------- Compilação e linkagem de shaders ----------
def inicializa_shaders():
    """Compila fontes GLSL e configura o programa de shaders."""
    global program
    # vertex shader
    vertex_src = """
        #version 400 core
        layout(location=0) in vec3 in_pos;
        layout(location=1) in vec2 in_uv;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        out vec2 frag_uv;
        void main() {
            frag_uv = in_uv;
            gl_Position = projection * view * model * vec4(in_pos,1.0);
        }
        """
   
    # fragment shader
        # - Recebe as coordenadas UV interpoladas (frag_uv)
        # - Amostra a cor da textura através de texture(texture1, frag_uv)
        # - Calcula um pulso senoidal absoluto para variar entre 0 e 1
        # - Interpola entre verde e vermelho com mix()
        # - Aplica essa cor pulsante sobre a textura (multiplicação)
    fragment_src = """
        #version 400 core
        in vec2 frag_uv;
        uniform sampler2D texture1;
        uniform float u_time;
        out vec4 FragColor;
        void main() {
            vec4 tex = texture(texture1, frag_uv);
            float pulse = abs(sin(u_time));
            vec3 color = mix(vec3(0.0,1.0,0.0), vec3(1.0,0.0,0.0), pulse);
            FragColor = vec4(tex.rgb * color, tex.a);
        }
        """
    vs = OpenGL.GL.shaders.compileShader(vertex_src, GL_VERTEX_SHADER)
    fs = OpenGL.GL.shaders.compileShader(fragment_src, GL_FRAGMENT_SHADER)
    program = OpenGL.GL.shaders.compileProgram(vs, fs)

# ---------- Carregamento do VAO e textura ----------
def inicializa_resources():
    """Cria VAO do cubo e carrega textura."""
    global vao, texture_id
    # configura VAO do cubo
    stride = 5 * ctypes.sizeof(ctypes.c_float)
    vertices = np.array([
        # front
       -0.5,-0.5,0.5, 0.0,0.0,  
        0.5,-0.5,0.5, 1.0,0.0,  
        0.5,0.5,0.5,  1.0,1.0,
       -0.5,-0.5,0.5, 0.0,0.0,  
        0.5,0.5,0.5,  1.0,1.0, 
       -0.5,0.5,0.5,  0.0,1.0,
        # back
       -0.5,-0.5,-0.5, 1.0,0.0, 
       -0.5,0.5,-0.5,  1.0,1.0,  
        0.5,0.5,-0.5,  0.0,1.0,
       -0.5,-0.5,-0.5, 1.0,0.0,  
        0.5,0.5,-0.5,  0.0,1.0,  
        0.5,-0.5,-0.5, 0.0,0.0,
        # left
       -0.5,-0.5,-0.5, 0.0,0.0, 
       -0.5,-0.5,0.5,  1.0,0.0, 
       -0.5,0.5,0.5,   1.0,1.0,
       -0.5,-0.5,-0.5, 0.0,0.0, 
       -0.5,0.5,0.5,   1.0,1.0, 
       -0.5,0.5,-0.5,  0.0,1.0,
        # right
         0.5,-0.5,-0.5, 1.0,0.0,  
         0.5,0.5,-0.5,  1.0,1.0,  
         0.5,0.5,0.5,   0.0,1.0,
         0.5,-0.5,-0.5, 1.0,0.0,  
         0.5,0.5,0.5,   0.0,1.0,  
         0.5,-0.5,0.5,  0.0,0.0,
        # top
        -0.5,0.5,-0.5, 0.0,1.0, 
        -0.5,0.5,0.5,  0.0,0.0,  
        0.5,0.5,0.5,   1.0,0.0,
        -0.5,0.5,-0.5, 0.0,1.0,  
        0.5,0.5,0.5,   1.0,0.0,  
        0.5,0.5,-0.5,  1.0,1.0,
        # bottom
        -0.5,-0.5,-0.5, 0.0,0.0, 
        0.5,-0.5,-0.5,  1.0,0.0, 
        0.5,-0.5,0.5,   1.0,1.0,
        -0.5,-0.5,-0.5, 0.0,0.0, 
        0.5,-0.5,0.5,   1.0,1.0, 
        -0.5,-0.5,0.5,  0.0,1.0,
    ], dtype=np.float32)

    # 1) Gera e registra um VAO (vertex array object)
    vao = glGenVertexArrays(1)
    # 2) Gera e registra um VBO (vertex buffer object)
    vbo = glGenBuffers(1)
    # 3) Vincula o VAO para configurar os atributos
    glBindVertexArray(vao)
    # 4) Vincula o VBO e envia os dados de vértice (posição + UV)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # 5) Habilita e define o atributo 0 para as coordenadas de posição (x,y,z)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    
    # 6) Habilita e define o atributo 1 para as coordenadas de textura (u,v)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))  
    # pula os 3 primeiros floats (x,y,z) para ler os componentes de textura (u,v)

    # 7) Desvincula o VAO para evitar configurações acidentais posteriores
    glBindVertexArray(0)
    
    
    
    # carrega a imagem "textura.jpg" do disco e prepara os dados
    img = Image.open("textura.jpg").transpose(Image.FLIP_TOP_BOTTOM)  # inverte verticalmente para coordenadas UV
    data = img.convert("RGBA").tobytes()                             # converte para bytes RGBA
    w, h = img.size                                                  # obtém largura e altura

    # gera um ID de textura no OpenGL e vincula como GL_TEXTURE_2D
    texture_id = glGenTextures(1)
    glActiveTexture(GL_TEXTURE0)            # seleciona a texture unit 0
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Define como a textura será filtrada quando ampliada/reduzida
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # filtragem linear para minification
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # filtragem linear para magnification

    # Envia os dados da imagem para a GPU (nível 0, formato RGBA)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

    # Desvincula a textura da unidade para evitar efeitos colaterais
    glBindTexture(GL_TEXTURE_2D, 0)

    # Vincula o sampler 'texture1' do fragment shader à texture unit 0
    glUseProgram(program)
    loc = glGetUniformLocation(program, "texture1")  # obtém localização do uniform sampler2D
    glUniform1i(loc, 0)                               # configura para usar GL_TEXTURE0


# ---------- Loop principal ----------
def render_loop():
    """Loop de eventos e renderização com WSAD."""
    global start_time, cam_pos
    start_time = time.time()
    
    model = pyrr.matrix44.create_identity(dtype=np.float32)
    while not glfw.window_should_close(window):
        current_time = time.time() - start_time
        glfw.poll_events()
        # WSAD controla cam_pos
        speed = 0.1 * (1/60)
        if glfw.get_key(window, glfw.KEY_W)==glfw.PRESS: 
          cam_pos += cam_front*speed
        if glfw.get_key(window, glfw.KEY_S)==glfw.PRESS: 
          cam_pos -= cam_front*speed
        right = pyrr.vector.normalize(pyrr.vector3.cross(cam_front, cam_up))
        if glfw.get_key(window, glfw.KEY_D)==glfw.PRESS: 
          cam_pos += right*speed
        if glfw.get_key(window, glfw.KEY_A)==glfw.PRESS: 
          cam_pos -= right*speed
        
        # limpar tela
        glClearColor(0.1,0.1,0.1,1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #Usa o programa de shaders
        glUseProgram(program)
        
        # view/proj
        # Cria a matriz 'view' (câmera):
        # - Origem: cam_pos
        # - Alvo:   cam_pos + cam_front (ponto à frente da câmera)
        # - Vetor up: cam_up
        # - Tipo de dado: np.float32 (compatível com OpenGL)
        view = pyrr.matrix44.create_look_at(cam_pos,cam_pos+cam_front,cam_up,dtype=np.float32)
        
        # Cria a matriz de projeção em perspectiva:
        # - FOV (campo de visão) de 45 graus
        # - Aspect ratio igual a WIDTH/HEIGHT
        # - Plano próximo (near) em 0.1
        # - Plano distante (far) em 100.0
        # - Tipo de dado: np.float32 (compatível com OpenGL)
        proj = pyrr.matrix44.create_perspective_projection_matrix(45.0,WIDTH/HEIGHT,0.1,100.0,dtype=np.float32)
        
        # envia uniforms
        loc = glGetUniformLocation
        glUniformMatrix4fv(loc(program,"model"),1,GL_FALSE,model)
        glUniformMatrix4fv(loc(program,"view"),1,GL_FALSE,view)
        glUniformMatrix4fv(loc(program,"projection"),1,GL_FALSE,proj)
        glUniform1f(loc(program,"u_time"),current_time)
        
        # desenha cubo
        # 1) Seleciona a texture unit 0 (corresponde ao sampler2D 'texture1')
        glActiveTexture(GL_TEXTURE0)
        # 2) Vincula a textura carregada a essa unidade
        glBindTexture(GL_TEXTURE_2D, texture_id)
        # 3) Vincula o VAO contendo posição e UV do cubo
        glBindVertexArray(vao)
        # 4) Emite o draw call para 36 vértices 
        glDrawArrays(GL_TRIANGLES, 0, 36)
        # 5) Troca os buffers para exibir o frame renderizado
        
        # swap_buffers(windows) serve para exibir o frame renderizado
        glfw.swap_buffers(window)
    glfw.terminate()

# ---------- main ----------
def main():
    inicializa_opengl()
    inicializa_shaders()
    inicializa_resources()
    render_loop()

if __name__ == "__main__":
    main()
