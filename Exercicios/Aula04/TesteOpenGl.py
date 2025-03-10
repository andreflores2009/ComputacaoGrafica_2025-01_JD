import pygame
from pygame.locals import *
from OpenGL.GL import glGetString, GL_VERSION

# Inicializa o Pygame e cria uma janela com suporte a OpenGL
pygame.init()
pygame.display.set_mode((640, 480), DOUBLEBUF | OPENGL)

# Agora é seguro chamar glGetString
opengl_version = glGetString(GL_VERSION)

# Exibe a versão do OpenGL
print("Versão do OpenGL:", opengl_version.decode())

# Encerra o Pygame
pygame.quit()
