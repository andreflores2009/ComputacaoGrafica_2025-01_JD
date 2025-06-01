from OpenGL.GL import (
    glBindTexture, glTexParameteri, glTexImage2D,
    GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T,
    GL_REPEAT, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER,
    GL_LINEAR, GL_RGBA, GL_UNSIGNED_BYTE
)
from PIL import Image

# Função para carregar uma textura PNG e configurá-la no OpenGL
def load_texture(path, texture):
    # Vincula o ID da textura ao alvo GL_TEXTURE_2D
    glBindTexture(GL_TEXTURE_2D, texture)
    
    # Configura o modo de repetição da textura no eixo S (horizontal)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    # Configura o modo de repetição da textura no eixo T (vertical)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    
    # Define o filtro de minificação (quando a textura fica menor na tela)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    # Define o filtro de magnificação (quando a textura fica maior na tela)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    # Abre a imagem do caminho especificado
    image = Image.open(path)
    # Inverte a imagem verticalmente para corresponder ao sistema de coordenadas do OpenGL - 
    #Por padrão, as imagens em Pillow (Image.open) têm origem no canto superior-esquerdo, enquanto o OpenGL espera a textura com origem no canto inferior-esquerdo.
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    # Converte a imagem para RGBA e obtém os dados brutos em bytes
    img_data = image.convert("RGBA").tobytes()
    
    # Envia os dados da imagem para a GPU, criando a textura 2D
    # Parâmetros:
    #   GL_TEXTURE_2D: alvo
    #   0             : nível de mipmap
    #   GL_RGBA       : formato interno da textura
    #   width, height : dimensões da imagem
    #   0             : borda (sempre 0)
    #   GL_RGBA       : formato dos dados enviados
    #   GL_UNSIGNED_BYTE : tipo dos dados enviados
    #   img_data      : ponteiro para os bytes da imagem
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 image.width, image.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE,
                 img_data)
    
    # Retorna o ID da textura para uso em glBindTexture() posteriormente
    return texture
