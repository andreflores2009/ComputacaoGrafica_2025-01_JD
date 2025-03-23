#Algoritmo DDA

#Biliotecas
import matplotlib.pyplot as plt

P1x = 2
P1y = 1
#P2x = 9
#P2y = 3
P2x = 5
P2y = 7

# Lista para armazenar os pontos da reta
points_x = []
points_y = []

#reta vertical
if P1x == P2x:
    print("Reta vertical")
    y = P1y
    while y<=P2y:
        print(P1x,",",y)
        #adiciona os pontos na lista para gerar o gráfico
        points_x.append(P1x)
        points_y.append(y)
        y+=1

else:
    m = (P2y - P1y)/(P2x - P1x)
    x = P1x
    y = P1y
    #reta mais deitada
    if m <= 1: #angulo <= 45º
        print("Reta mais deitada")
        while x <= P2x:
            print(x,",",round(y)) #round() usada para arredondamento
            #adiciona os pontos na lista para gerar o gráfico
            points_x.append(x)
            points_y.append(round(y))
            y+=m
            x+=1

    #reta mais de pé
    elif m > 1: #angulo > 45º
        print("Reta mais de pé")
        while y <= P2y:
            print(round(x),",",y)
            #adiciona os pontos na lista para gerar o gráfico
            points_x.append(round(x))
            points_y.append(y)
            x+=1/m
            y+=1

# Mostrar o gráfico
plt.plot(points_x, points_y, marker='o', linestyle='-', color='b')
plt.title('Rasterização de Linha')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid(True)
plt.show()
