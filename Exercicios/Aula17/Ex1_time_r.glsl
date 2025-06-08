/*Adicionamos o bloco #ifdef GL_ES … precision mediump float; 
para definir a precisão de floats em ambientes WebGL/GL ES.*/

#ifdef GL_ES
precision mediump float;
#endif

// Uniform injetado pelo glsl-canvas
uniform float u_time;

void main() {
    // calcula um pulso vermelho baseado no tempo
    float pulso = abs(sin(u_time));
    gl_FragColor = vec4(pulso, 0.0, 0.0, 1.0);
}
