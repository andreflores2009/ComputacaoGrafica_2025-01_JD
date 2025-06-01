# Camera.py
# Gerencia a câmera 3D usando yaw (rotação horizontal) e pitch (rotação vertical)
#
# Atributos principais:
#   camera_pos         : Vector3 – posição da câmera no mundo
#   camera_front       : Vector3 – direção que a câmera está apontando
#   camera_up          : Vector3 – vetor “para cima” da câmera
#   camera_right       : Vector3 – vetor “para a direita” da câmera
#   yaw                : float   – ângulo de rotação horizontal em graus (em torno do eixo Y)
#   pitch              : float   – ângulo de rotação vertical em graus (em torno do eixo X)
#   mouse_sensitivity  : float   – quanto o movimento do mouse afeta yaw/pitch
#
# Métodos:
#   get_view_matrix()
#       → Retorna a matriz look-at com base em camera_pos, camera_front e camera_up.
#
#   process_mouse_movement(xoffset, yoffset, constrain_pitch=True)
#       xoffset, yoffset : deslocamento do mouse em pixels.
#       constrain_pitch   : limita pitch a [-45°, +45°] para evitar inversão de câmera.
#       Atualiza yaw e pitch e recalcula os vetores da câmera.
#
#   process_keyboard(direction, velocity)
#       direction : "FORWARD" | "BACKWARD" | "LEFT" | "RIGHT"
#       velocity  : valor de deslocamento ao longo de camera_front ou camera_right.
#
#   update_camera_vectors()
#       Interno: converte yaw/pitch em vetores normais de direção da câmera.

from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Camera:
    def __init__(self):
        # posição inicial da câmera (x, y, z)
        self.camera_pos    = Vector3([0.0, 4.0, 30.0])
        # direção inicial (front) apontando para -Z
        self.camera_front  = Vector3([0.0, 0.0, -1.0])
        # vetor "para cima" global
        self.camera_up     = Vector3([0.0, 1.0, 0.0])
        # vetor "para a direita" inicial (usado no movimento lateral)
        self.camera_right  = Vector3([1.0, 0.0, 0.0])

        # sensibilidade do mouse (quanto xoffset e yoffset afetam yaw/pitch)
        self.mouse_sensitivity = 0.01
        # ângulo yaw (horizontal), começa em -90° para olhar para -Z
        self.yaw   = -90.0
        # ângulo pitch (vertical), 0° inicialmente (nível)
        self.pitch = 0.0

    def get_view_matrix(self):
        """
        Gera a matriz de visualização (LookAt).
        → camera_pos é o olho da câmera.
        → camera_pos + camera_front é o ponto para onde a câmera olha.
        → camera_up define a orientação "para cima".
        """
        return matrix44.create_look_at(
            self.camera_pos,
            self.camera_pos + self.camera_front,
            self.camera_up
        )

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        """
        Atualiza yaw e pitch conforme movimento do mouse.
        - xoffset: deslocamento horizontal do mouse (pixels).
        - yoffset: deslocamento vertical do mouse (pixels).
        - constrain_pitch: True limita pitch para evitar virar a câmera de ponta-cabeça.
        """
        # aplica sensibilidade
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        # atualiza ângulos
        self.yaw   += xoffset
        self.pitch += yoffset

        # limita pitch se necessário
        if constrain_pitch:
            max_angle = 45.0
            if self.pitch > max_angle:
                self.pitch = max_angle
            if self.pitch < -max_angle:
                self.pitch = -max_angle

        # recalcula vetores front, right e up
        self.update_camera_vectors()

    def process_keyboard(self, direction, velocity):
        """
        Move a câmera em uma das direções com base em camera_front e camera_right.
        - direction: "FORWARD", "BACKWARD", "LEFT" ou "RIGHT"
        - velocity : distância a ser movida.
        """
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        elif direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        elif direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        elif direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity

    def update_camera_vectors(self):
        """
        Converte yaw/pitch em um vetor direção (front), depois recalcula
        os vetores right e up para manter a câmera ortonormal.
        """
        # calcula vetor "front" com trigonometria
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.yaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.yaw)) * cos(radians(self.pitch))

        # normaliza
        self.camera_front = vector.normalise(front)
        # vetor right = cross(camera_front, world_up)
        world_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, world_up))
        # vetor up = cross(camera_right, camera_front)
        self.camera_up    = vector.normalise(vector3.cross(self.camera_right, self.camera_front))
