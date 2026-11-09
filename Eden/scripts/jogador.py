import os
import pygame

class Jogador(pygame.sprite.Sprite):
    """
    Representa o avatar do jogador (Guardião/Zoólogo).
    Permite movimentação em 8 direções pelo mapa com WASD ou setas,
    orientação visual e detecção de proximidade com animais.
    """
    def __init__(self, x, y):
        super().__init__()
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.velocidade = 4.5
        self.olhando_direita = True
        self.direcao_atual = (0, 1)

        self._carregar_graficos()
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))
        self.anim_timer = 0
        self.frame_idx = 0

    def _carregar_graficos(self):
        caminho = os.path.join("assets", "personagem.png")
        self.frames = []
        if os.path.exists(caminho):
            try:
                img_raw = pygame.image.load(caminho).convert_alpha()
                w, h = img_raw.get_size()
                # Escala proporcionalmente para ~56x56
                escala = min(56 / w, 56 / h)
                nw, nh = int(w * escala), int(h * escala)
                base = pygame.transform.smoothscale(img_raw, (nw, nh))

                # Cria superfície centralizada
                surf1 = pygame.Surface((56, 56), pygame.SRCALPHA)
                surf1.blit(base, ((56 - nw) // 2, (56 - nh) // 2))

                # Frame 2 levemente inclinado para simular passo
                surf2 = pygame.Surface((56, 56), pygame.SRCALPHA)
                base2 = pygame.transform.smoothscale(img_raw, (nw, nh - 2))
                surf2.blit(base2, ((56 - nw) // 2, (56 - nh) // 2 + 2))

                self.frames = [surf1, surf2]
            except Exception as e:
                print(f"Aviso ao carregar personagem: {e}")

        if not self.frames:
            # Fallback elegante estilizado com chapéu de safari / zoólogo
            surf1 = pygame.Surface((56, 56), pygame.SRCALPHA)
            # Chapéu de explorador (bege/safari)
            pygame.draw.ellipse(surf1, (189, 154, 107), (10, 8, 36, 16))
            pygame.draw.ellipse(surf1, (218, 189, 140), (16, 4, 24, 14))
            # Rosto
            pygame.draw.circle(surf1, (255, 224, 189), (28, 24), 11)
            pygame.draw.circle(surf1, (40, 40, 40), (25, 23), 2)
            pygame.draw.circle(surf1, (40, 40, 40), (32, 23), 2)
            # Uniforme verde de guardião / zoólogo
            pygame.draw.rect(surf1, (46, 125, 50), (18, 35, 20, 16), border_radius=4)
            # Cinto marrom
            pygame.draw.rect(surf1, (109, 76, 65), (18, 45, 20, 4))
            self.frames = [surf1, surf1]

        self.image = self.frames[0]

    def update(self, dt, limites_mundo=None):
        keys = pygame.key.get_pressed()
        dx, dy = 0.0, 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1.0

        em_movimento = (dx != 0 or dy != 0)

        if em_movimento:
            # Normalização diagonal
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071

            if dx < 0:
                self.olhando_direita = False
            elif dx > 0:
                self.olhando_direita = True

            self.direcao_atual = (dx, dy)
            self.pos_x += dx * self.velocidade
            self.pos_y += dy * self.velocidade

            # Animação de passos
            self.anim_timer += dt
            if self.anim_timer >= 180:
                self.anim_timer = 0
                self.frame_idx = (self.frame_idx + 1) % len(self.frames)

        else:
            self.frame_idx = 0

        # Aplica limites do mapa
        if limites_mundo:
            self.pos_x = max(limites_mundo.left + 24, min(limites_mundo.right - 24, self.pos_x))
            self.pos_y = max(limites_mundo.top + 24, min(limites_mundo.bottom - 24, self.pos_y))

        # Atualiza a orientação da imagem
        img_base = self.frames[self.frame_idx]
        if not self.olhando_direita:
            self.image = pygame.transform.flip(img_base, True, False)
        else:
            self.image = img_base

        self.rect.center = (int(self.pos_x), int(self.pos_y))
