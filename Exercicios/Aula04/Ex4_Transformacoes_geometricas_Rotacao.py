import numpy as np  # Importa a biblioteca NumPy para operações matemáticas
import matplotlib.pyplot as plt  # Importa a biblioteca Matplotlib para plotar gráficos

# Função para calcular a rotação dos pontos
def rotacao(pontos, angulo):
    pontos_rotacionados = []  # Lista para armazenar os pontos rotacionados
    angulo_rad = np.radians(angulo)  # Converter ângulo de graus para radianos

    for ponto in pontos:  # Percorre cada ponto na lista
        x0, y0 = ponto  # Obtém as coordenadas do ponto
        # Calcular as coordenadas após a rotação
        xu = round(x0 * np.cos(angulo_rad) - y0 * np.sin(angulo_rad), 2)
        yu = round(x0 * np.sin(angulo_rad) + y0 * np.cos(angulo_rad), 2)
        pontos_rotacionados.append((xu, yu))  # Adiciona o ponto rotacionado à lista

    return pontos_rotacionados  # Retorna a lista de pontos rotacionados

# Pontos originais
p1 = (2, 2)  # Primeiro ponto
p2 = (4, 4)  # Segundo ponto

# Ângulo de rotação (em graus)
angulo = 45  # Define o ângulo de rotação

# Calcular a rotação dos pontos
pontos_rotacionados = rotacao([p1, p2], angulo)

# Imprimir pontos originais e rotacionados para verificação
print("Pontos originais:")
print(f"P1: {p1}")
print(f"P2: {p2}")

print("\nPontos rotacionados:")
for i, p in enumerate(pontos_rotacionados, start=1):
    print(f"P{i}`: {p}")

# Plotar os pontos originais e os pontos rotacionados
plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo-', label='Pontos originais')  # Plota os pontos originais em azul
plt.plot([p[0] for p in pontos_rotacionados], [p[1] for p in pontos_rotacionados], 'ro-', label='Pontos rotacionados')  # Plota os pontos rotacionados em vermelho

# Adicionar rótulos aos pontos originais
plt.text(p1[0], p1[1], ' P1', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
plt.text(p2[0], p2[1], ' P2', fontsize=12, verticalalignment='bottom', horizontalalignment='right')

# Adicionar rótulos aos pontos rotacionados
for i, p in enumerate(pontos_rotacionados, start=1):
    plt.text(p[0], p[1], f' P{i}`', fontsize=12, verticalalignment='bottom', horizontalalignment='right')

# Configurações do gráfico
plt.xlabel('X')  # Define o rótulo do eixo X
plt.ylabel('Y')  # Define o rótulo do eixo Y
plt.title('Rotação de pontos no plano cartesiano')  # Define o título do gráfico
plt.grid(True)  # Exibe a grade no gráfico
plt.legend()  # Adiciona a legenda

# Mostrar o gráfico
plt.show()  # Exibe o gráfico
