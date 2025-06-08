#ifdef GL_ES
// Em ambientes WebGL/GL ES, precisamos declarar a precisão de floats.
// Aqui usamos precisão média (“mediump”), o suficiente para a maioria dos efeitos.
precision mediump float;
#endif

// Uniform injetado pela aplicação (ou pelo glsl-canvas) contendo
// a resolução da viewport em pixels: (largura, altura)
uniform vec2 u_resolution;

void main() {
    // gl_FragCoord.xy contém as coordenadas do fragmento atual em pixels,
    // variando de (0.5,0.5) no canto inferior esquerdo ao (WIDTH-0.5,HEIGHT-0.5)
    // no canto superior direito.
    //
    // Ao dividir por u_resolution, obtemos um vetor “st” normalizado
    // no intervalo [0.0, 1.0] em ambas as direções.
    vec2 st = gl_FragCoord.xy / u_resolution;

    // Montamos a cor final do fragmento:
    // - canal R recebe st.x (varia de 0.0 na esquerda a 1.0 na direita)
    // - canal G recebe st.y (varia de 0.0 embaixo a 1.0 em cima)
    // - canal B fixo em 0.0
    // - alfa fixo em 1.0 (totalmente opaco)
    gl_FragColor = vec4(st.x, st.y, 0.0, 1.0);
}
