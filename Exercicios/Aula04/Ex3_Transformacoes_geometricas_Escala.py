import matplotlib.pyplot as plt

# Função para calcular a escala dos pontos
def escala(pontos, Sx, Sy):
    pontos_escala = []
    for ponto in pontos:
        x_u = ponto[0] * Sx
        y_u = ponto[1] * Sy
        pontos_escala.append((x_u, y_u))
    return pontos_escala

# Pontos originais
p1 = (-1, -1)
p2 = (1, 1)

# Fatores de escala
Sx = 2
Sy = 2

# Calcular a escala dos pontos
pontos_escala = escala([p1, p2], Sx, Sy)

# Plotar os pontos originais e os pontos escalados
plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo-', label='Pontos originais')
plt.plot([ponto[0] for ponto in pontos_escala], [ponto[1] for ponto in pontos_escala], 'ro-', label='Pontos escalados')

# Definir os limites dos eixos
plt.xlim(-3, 5)  # Define o limite do eixo X de 0 a 15
plt.ylim(-3, 5)  # Define o limite do eixo Y de 0 a 15

# Configurações do gráfico
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Escala de pontos no plano cartesiano')
plt.grid(True)
plt.legend()

# Mostrar o gráfico
plt.show()
