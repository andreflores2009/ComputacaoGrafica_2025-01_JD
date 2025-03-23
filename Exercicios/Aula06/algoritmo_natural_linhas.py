# O coeficiente angular e o coeficiente linear são conceitos importantes ao descrever uma reta em um sistema de coordenadas.
# Vamos explorar cada um deles:

# Coeficiente Angular (m):
# O coeficiente angular, denotado por 'm', representa a inclinação ou a taxa de variação de uma reta.
# Ele é definido como a mudança na coordenada 'y' dividida pela mudança correspondente na coordenada 'x' entre dois pontos em uma reta.
# Matematicamente, o coeficiente angular é calculado pela fórmula:
# m = Δy / Δx
# onde Δy é a variação em 'y' e Δx é a variação em 'x' entre dois pontos.
# Se m > 0, a reta inclina para cima; se m < 0, a reta inclina para baixo; se m = 0, a reta é horizontal.

# Coeficiente Linear (b):
# O coeficiente linear, denotado por 'b', é o ponto onde a reta intercepta o eixo 'y' quando x = 0.
# Ele representa a constante aditiva que ajusta a posição vertical da reta.
# Matematicamente, é o valor de 'y' quando x = 0.
# A equação geral de uma reta em coordenadas cartesianas é expressa como:
# y = mx + b
# onde 'y' é a coordenada 'y', 'x' é a coordenada 'x', 'm' é o coeficiente angular e 'b' é o coeficiente linear.

# Em resumo, o coeficiente angular controla a inclinação da reta, enquanto o coeficiente linear determina a posição vertical da reta
# no plano cartesiano.
# Juntos, esses coeficientes formam a equação da reta e descrevem completamente sua posição e inclinação.
#Biliotecas

#algoritmo natural


#Biliotecas
import matplotlib.pyplot as plt

# Coordenadas dos pontos P1 e P2
P1x = 2
P1y = 1

#P2x = 5
#P2y = 7
P2x = 7
P2y = 3

# Inicialização das listas para armazenar os pontos da reta
points_x = []
points_y = []


#reta vertical
if P1x == P2x:
    print("Reta vertical")
    y = P1y
    while y<=P2y:
        #imprime os pontos na tela
        #print(P1x,",",y)

        #adiciona os pontos na lista para gerar o gráfico
        points_x.append(P1x)
        points_y.append(y)
        y+=1

else:
    # Cálculo do coeficiente angular (m) e coeficiente linear (b)
    m = (P2y - P1y)/(P2x - P1x)
    b = P1y - m*P1x

    #reta mais deitada
    if m <= 1: #angulo <= 45º
        print("Reta mais deitada")
        x = P1x
        while x <= P2x:
            #equacao reduzida da reta
            y = round(m*x + b)
            #imprime os pontos na tela
            #print(x,",",y)

            #adiciona os pontos na lista para gerar o gráfico
            points_x.append(x)
            points_y.append(y)
            x+=1

    #reta mais de pé
    elif m > 1: #angulo > 45º
        print("Reta mais de pé")
        y = P1y
        while y <= P2y:
            x = round((y-b)/m)
            #imprime os pontos na tela
            #print(x,",",y)

            #adiciona os pontos na lista para gerar o gráfico
            points_x.append(x)
            points_y.append(y)
            y+=1


# Imprimir os pontos da reta
print("\n Pontos da reta:")
for i in range(len(points_x)):
    print(points_x[i], ",", points_y[i])


# Gerar o gráfico
plt.plot(points_x, points_y, marker='o', linestyle='-', color='b')
plt.title('Rasterização de Linha')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid(True)
plt.show()
