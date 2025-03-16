# Desenhando um Círculo em OpenGL com Pygame

Este projeto demonstra como desenhar um círculo usando **OpenGL** e **Pygame**. Utilizamos a equação paramétrica do círculo para gerar pontos suaves ao longo da circunferência.

## Como Funciona?
O círculo é desenhado com a seguinte equação paramétrica:

```math
x = r \cdot \cos(\theta)
```

```math
y = r \cdot \sin(\theta)
```

onde:
- \( r \) é o **raio** do círculo.
- \( \theta \) varia de **0** a **2\pi** (360 graus) para cobrir toda a circunferência.
- \( \cos(\theta) \) e \( \sin(\theta) \) determinam a posição de cada ponto ao longo do círculo.

O OpenGL conecta esses pontos usando **GL_LINE_LOOP**, formando o círculo.

## Diferenças para Outros Algoritmos

| Algoritmo            | Como Funciona | Suavidade |
|----------------------|--------------|----------|
| **Bresenham**       | Aproxima pixels para rasterização | Baixa |
| **Ponto Médio**    | Decide pixels com base em um critério | Média |
| **Equação Paramétrica** | Usa funções trigonométricas | Alta |

A equação paramétrica é ideal para OpenGL, pois trabalha com coordenadas contínuas, sem restrições de pixels.

## Como Rodar o Código?

1. Instale as dependências necessárias:
   ```bash
   pip install pygame PyOpenGL PyOpenGL_accelerate
   ```

2. Execute o script:
   ```bash
   python circle_opengl.py
   ```

3. Uma janela será aberta exibindo um **círculo verde desenhado com OpenGL**.

## Personalização
- **Altere o raio**: Modifique `draw_circle(2)` para outro valor.
- **Mude a cor**: Edite `glColor3f(0.0, 1.0, 0.0)` para outras cores RGB.
- **Ajuste a suavidade**: Aumente `num_segments` para um círculo mais suave.

## Autor
Projeto desenvolvido para demonstrar o uso de OpenGL em Python com Pygame.

---
Este README serve como documentação básica do projeto. 🚀
