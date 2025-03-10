# Importa a biblioteca NumPy para facilitar a manipulação de matrizes
import numpy as np

# Define a matriz A
A = np.array([[1, 3, 2],
              [4, 7, 6]])

# Define a matriz B
B = np.array([[2, 8],
              [3, 1],
              [5, 9]])

# Exibe as matrizes iniciais
print("Matriz A:")
print(A)
print("\nMatriz B:")
print(B)

# Obtém as dimensões das matrizes
linhas_A, colunas_A = A.shape
linhas_B, colunas_B = B.shape

# Exibe as dimensões das matrizes
print(f"\nDimensões de A: {linhas_A}x{colunas_A}")
print(f"Dimensões de B: {linhas_B}x{colunas_B}")

# Verifica se as matrizes podem ser multiplicadas
if colunas_A != linhas_B:
    print("\nErro: O número de colunas de A deve ser igual ao número de linhas de B para multiplicação.")
else:
    # Inicializa a matriz resultado com zeros (como inteiros para evitar pontos decimais) numpy por padrão inicializa variáveis como float
    resultado = np.zeros((linhas_A, colunas_B), dtype=int)
    #print(resultado)

    # Multiplica as matrizes A e B manualmente com loops aninhados
    for i in range(linhas_A):  # Percorre as linhas de A
        for j in range(colunas_B):  # Percorre as colunas de B
            soma = 0  # Variável para armazenar a soma dos produtos
            for k in range(colunas_A):  # Percorre os elementos da linha de A e coluna de B
                soma += A[i][k] * B[k][j]  # Multiplica e acumula o resultado
            resultado[i][j] = soma  # Atribui o resultado final para a posição correta

    # Exibe o resultado da multiplicacao das matrizes
    print("\nResultado da multiplicacao de A e B:")
    print(resultado)
