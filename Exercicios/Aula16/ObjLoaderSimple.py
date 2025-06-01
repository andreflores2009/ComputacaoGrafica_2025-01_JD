# ObjLoaderSimple.py
# Carrega apenas vértices e coordenadas de textura (UV) de um arquivo .obj
# Gera um buffer intercalado [x, y, z, u, v] para uso com glDrawArrays
#
# Cada linha de face no OBJ usa o formato:
#   f i/j/k i/j/k i/j/k
#   • i = índice de VÉRTICE (posição) — 1-based no arquivo, subtraímos 1 para 0-based em Python
#   • j = índice de COORDENADA DE TEXTURA (UV) — 1-based, subtrai 1 para 0-based
#   • k = índice de NORMAL — 1-based, subtrai 1 para 0-based (não usado neste loader simples)
# O loader extrai (i, j) para cada vértice do triângulo, convertendo para índices Python,
# e depois monta o buffer [x, y, z, u, v] na ordem correta para glDrawArrays.

import numpy as np

class ObjLoaderSimple:
    """
    Classe utilitária para ler modelos OBJ simplificados, contendo apenas
    vértices (v) e coordenadas de textura (vt), e montar um buffer de dados
    intercalados para renderização sem normais.
    """

    @staticmethod
    def load_obj(path):
        """
        Lê um arquivo .obj procurando linhas de vértices ('v') e UVs ('vt'),
        e faces ('f'), e monta um buffer de floats intercalados [x, y, z, u, v].

        Parâmetros:
            path (str): caminho para o arquivo .obj a ser lido.

        Retorna:
            vertex_buffer (np.ndarray): array float32 com dados [x,y,z,u,v,...].
            num_vertices  (int): número de vértices (contagem de triplas x,y,z).
        """
        vertices = []     # lista de [x, y, z]
        uvs      = []     # lista de [u, v]
        faces    = []     # lista de tuplas (índice vértice, índice UV)




        # Para cada linha do arquivo OBJ, o loader:
        # 1. Usa line.strip().split() para:
        #    - strip(): remover espaços em branco e quebras de linha no início/fim.
        #    - split(): separar a linha em tokens (parts) usando espaços como delimitador.
        # 2. Checa if not parts: continue — pula linhas em branco ou só com espaços.
        # 3. Examina parts[0] (o primeiro token) para decidir o que aquela linha representa:
        #    - 'v'  → linha de vértice: parts[1:4] são as coordenadas x, y, z; converte para float e adiciona a vertices.
        #    - 'vt' → linha de coordenada de textura: parts[1:3] são u, v; converte para float e adiciona a uvs.
        #    - 'f'  → linha de face: cada token parts[1], parts[2], parts[3] é algo como "i/j/k"; a gente separa em vals = vert.split('/')
        #             e extrai os índices de vértice (i) e de UV (j), convertendo de 1-based para 0-based e armazenando em faces.
        # Assim, cada linha é processada apenas uma vez, roteando o fluxo conforme o prefixo parts[0].
        
        # Abra e leia cada linha do arquivo
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts:  #se é linha em branco pula p proxima
                    continue

                # Interpreta coordenadas de vértice
                if parts[0] == 'v':
                    # 'v x y z'
                    x, y, z = map(float, parts[1:4])
                    vertices.append([x, y, z])

                # Interpreta coordenadas de textura
                elif parts[0] == 'vt':
                    # 'vt u v'
                    u, v = map(float, parts[1:3])
                    uvs.append([u, v])

                
                # --- Leitura e ajuste de índices de face ---
                # Este trecho processa cada linha de face ('f') do arquivo OBJ,
                # que vem no formato "i/j/k" para cada vértice do triângulo:
                #   i = índice de vértice (posição)
                #   j = índice de coordenada de textura (UV)
                #   k = índice de normal (não usado aqui)
                # Para cada "i/j", convertemos de 1-based (OBJ) para 0-based (Python):
                #   vi = int(i) - 1  → posição correta em vertices[vi]
                #   ti = int(j) - 1  → posição correta em uvs[ti] (ou None se não existir)
                # O par (vi, ti) é então armazenado em `faces` para montar o buffer de vértices.
                # Interpreta faces (somente os índices de vértice e UV)
                elif parts[0] == 'f':
                    # Cada face no OBJ é definida por três vértices no formato "i/j/k"
                    # onde i = índice de vértice, j = índice de UV, k = índice de normal.
                    # Aqui percorremos apenas os três primeiros (triângulo).
                    for vert in parts[1:4]:
                        # Exemplo de vert: "12/34/56" ou "12/34" se não houver normal.
                        vals = vert.split('/')  

                        # ----------------------------
                        # Índice de vértice (vi):
                        # vals[0] é a parte antes da primeira "/", ex: "12".
                        # Convertemos para inteiro e subtraímos 1 porque o OBJ é 1-based (indice começa em 1) e em python os indices começam em zero.
                        # Assim, vi aponta para vertices[vi].
                        #ex: v  a   b   c       ← vértice 12, fica: vi = int("12") - 1  # vi = 11
                        vi = int(vals[0]) - 1  

                        # ----------------------------
                        # Índice de UV (ti) texturas:
                        # Se houver uma segunda parte (vals[1]) e ela não estiver vazia,
                        # convertemos para inteiro e subtraímos 1 (também 1-based → 0-based).
                        # Caso contrário, marcamos ti como None (sem textura).
                        if len(vals) > 1 and vals[1]:
                            ti = int(vals[1]) - 1
                        else:
                            ti = None

                        # Adiciona ao array de faces o par (índice de vértice, índice de UV)
                        faces.append((vi, ti))  #[x, y, z, u, v]

        #------- Monta o buffer intercalado [x, y, z, u, v] para cada face-----
        buffer = []
        for vi, ti in faces:
            # Adiciona posição do vértice
            x, y, z = vertices[vi]
            buffer.extend([x, y, z])
            # Adiciona UV se existir, senão (0.0, 0.0)
            if ti is not None and ti < len(uvs):
                u, v = uvs[ti]
                buffer.extend([u, v])
            else:
                buffer.extend([0.0, 0.0])

        # Converte para numpy float32 e calcula número de vértices
        vertex_buffer = np.array(buffer, dtype=np.float32)
        num_vertices  = vertex_buffer.size // 5  # 5 componentes por vértice O operador // faz divisão inteira, ou seja, sempre retorna um número inteiro (no exemplo 500 // 5 dá 100, sem casas decimais).

        return vertex_buffer, num_vertices
