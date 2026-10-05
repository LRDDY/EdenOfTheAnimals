import os
import math
import random
import pygame

# =============================================================================
# CORES AUXILIARES PARA CRIAÇÃO DE SPRITES PROCEDURAIS
# =============================================================================
CORES_ANIMAIS = {
    "Macaco": (139, 90, 43),
    "Arara": (30, 144, 255),
    "Crocodilo": (46, 125, 50),
    "Cobra": (198, 40, 40),
    "Tartaruga": (56, 142, 60),
    "Peixe-Palhaço": (255, 112, 67),
    "Pirarucu": (120, 144, 156),
    "Sapo-Cururu": (104, 159, 56),
    "Salamandra": (255, 179, 0),
    "Javali": (109, 76, 65),
    "Raposa": (230, 81, 0),
    "Cervo": (161, 136, 127),
    "Lebre": (189, 189, 189),
    "Tetraz-Negro": (38, 50, 56)
}


def gerar_sprite_procedural(nome, tamanho=(64, 64)):
    """Gera um sprite 2D estilizado em pixel art quando uma imagem não existir."""
    surf = pygame.Surface(tamanho, pygame.SRCALPHA)
    w, h = tamanho
    cor = CORES_ANIMAIS.get(nome, (100, 100, 100))
    cor_escura = (max(0, cor[0] - 40), max(0, cor[1] - 40), max(0, cor[2] - 40))
    cor_clara = (min(255, cor[0] + 40), min(255, cor[1] + 40), min(255, cor[2] + 40))

    if nome == "Macaco":
        # Corpo e cabeça
        pygame.draw.circle(surf, cor, (w // 2, h // 2 + 6), 18)
        pygame.draw.circle(surf, cor, (w // 2, h // 2 - 12), 14)
        # Orelhas
        pygame.draw.circle(surf, cor_escura, (w // 2 - 14, h // 2 - 12), 6)
        pygame.draw.circle(surf, cor_escura, (w // 2 + 14, h // 2 - 12), 6)
        # Rosto
        pygame.draw.circle(surf, (245, 222, 179), (w // 2, h // 2 - 10), 9)
        # Olhos
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 - 4, h // 2 - 12), 2)
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 + 4, h // 2 - 12), 2)
        # Cauda longa curvada
        pygame.draw.arc(surf, cor, (w // 2 - 28, h // 2 - 4, 24, 28), 1.5, 4.8, 4)

    elif nome == "Arara":
        # Corpo azul/amarelo
        pygame.draw.ellipse(surf, cor, (w // 2 - 12, h // 2 - 16, 24, 34))
        # Peito amarelo
        pygame.draw.ellipse(surf, (255, 215, 0), (w // 2 - 8, h // 2 - 6, 16, 22))
        # Asa
        pygame.draw.polygon(surf, (0, 100, 200), [(w // 2 + 4, h // 2 - 10), (w // 2 + 20, h // 2 + 4), (w // 2 + 4, h // 2 + 12)])
        # Bico curvo
        pygame.draw.polygon(surf, (50, 50, 50), [(w // 2 - 12, h // 2 - 12), (w // 2 - 22, h // 2 - 8), (w // 2 - 12, h // 2 - 4)])
        # Olho
        pygame.draw.circle(surf, (255, 255, 255), (w // 2 - 6, h // 2 - 12), 3)
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 - 6, h // 2 - 12), 1)
        # Cauda colorida
        pygame.draw.polygon(surf, (220, 20, 60), [(w // 2 - 4, h // 2 + 16), (w // 2 + 6, h // 2 + 16), (w // 2 + 10, h - 4), (w // 2 - 6, h - 4)])

    elif nome == "Crocodilo":
        # Corpo alongado horizontal
        pygame.draw.ellipse(surf, cor, (6, h // 2 - 8, w - 12, 18))
        # Cabeça / Focinho com dentes
        pygame.draw.polygon(surf, cor_escura, [(w - 22, h // 2 - 10), (w - 2, h // 2 - 2), (w - 22, h // 2 + 6)])
        # Escamas no dorso
        for ox in range(16, w - 24, 7):
            pygame.draw.polygon(surf, cor_clara, [(ox, h // 2 - 8), (ox + 3, h // 2 - 14), (ox + 6, h // 2 - 8)])
        # Patas
        pygame.draw.rect(surf, cor_escura, (14, h // 2 + 6, 6, 8), border_radius=2)
        pygame.draw.rect(surf, cor_escura, (w - 30, h // 2 + 6, 6, 8), border_radius=2)
        # Olho saliente
        pygame.draw.circle(surf, (255, 215, 0), (w - 20, h // 2 - 9), 3)
        pygame.draw.circle(surf, (0, 0, 0), (w - 20, h // 2 - 9), 1)

    elif nome == "Cobra":
        # Corpo sinuoso em espiral
        pontos = [
            (12, h // 2 + 10), (22, h // 2 - 10), (34, h // 2 + 12),
            (46, h // 2 - 8), (54, h // 2 - 2)
        ]
        pygame.draw.lines(surf, cor, False, pontos, 8)
        # Listras / anéis
        for px, py in [(18, h // 2 - 2), (28, h // 2 + 4), (40, h // 2)]:
            pygame.draw.circle(surf, (255, 255, 255), (px, py), 4)
            pygame.draw.circle(surf, (0, 0, 0), (px, py), 2)
        # Cabeça
        pygame.draw.circle(surf, cor_escura, (54, h // 2 - 2), 7)
        # Olhos
        pygame.draw.circle(surf, (255, 215, 0), (55, h // 2 - 5), 2)
        # Língua bifurcada
        pygame.draw.line(surf, (255, 0, 0), (60, h // 2 - 2), (64, h // 2 - 4), 2)
        pygame.draw.line(surf, (255, 0, 0), (60, h // 2 - 2), (64, h // 2), 2)

    elif nome == "Tartaruga":
        # Casco oval
        pygame.draw.ellipse(surf, cor_escura, (w // 2 - 18, h // 2 - 14, 36, 28))
        pygame.draw.ellipse(surf, cor, (w // 2 - 15, h // 2 - 12, 30, 24))
        # Placas do casco
        pygame.draw.circle(surf, cor_clara, (w // 2, h // 2), 6, 2)
        # Cabeça
        pygame.draw.circle(surf, (100, 180, 100), (w // 2 + 20, h // 2), 7)
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 + 22, h // 2 - 2), 2)
        # Nadadeiras / patas
        pygame.draw.ellipse(surf, (80, 160, 80), (w // 2 + 4, h // 2 - 20, 14, 8))
        pygame.draw.ellipse(surf, (80, 160, 80), (w // 2 + 4, h // 2 + 12, 14, 8))
        pygame.draw.ellipse(surf, (80, 160, 80), (w // 2 - 22, h // 2 - 16, 10, 6))
        pygame.draw.ellipse(surf, (80, 160, 80), (w // 2 - 22, h // 2 + 10, 10, 6))

    elif nome == "Peixe-Palhaço":
        # Corpo laranja
        pygame.draw.ellipse(surf, cor, (8, h // 2 - 14, 44, 28))
        # Cauda
        pygame.draw.polygon(surf, cor, [(12, h // 2), (2, h // 2 - 12), (2, h // 2 + 12)])
        # Três faixas brancas características com bordas pretas
        faixas_x = [18, 28, 40]
        for fx in faixas_x:
            pygame.draw.rect(surf, (255, 255, 255), (fx, h // 2 - 13, 5, 26), border_radius=2)
            pygame.draw.rect(surf, (0, 0, 0), (fx, h // 2 - 13, 5, 26), 1, border_radius=2)
        # Olho
        pygame.draw.circle(surf, (0, 0, 0), (44, h // 2 - 4), 3)
        pygame.draw.circle(surf, (255, 255, 255), (45, h // 2 - 5), 1)

    elif nome == "Pirarucu":
        # Corpo longo prateado avermelhado
        pygame.draw.ellipse(surf, cor, (4, h // 2 - 10, 52, 20))
        # Cauda larga com detalhes vermelhos
        pygame.draw.polygon(surf, (211, 47, 47), [(10, h // 2), (2, h // 2 - 14), (2, h // 2 + 14)])
        # Escamas avermelhadas no terço posterior
        for sx in range(12, 34, 5):
            pygame.draw.line(surf, (211, 47, 47), (sx, h // 2 - 6), (sx, h // 2 + 6), 2)
        # Cabeça achatada
        pygame.draw.ellipse(surf, cor_escura, (44, h // 2 - 8, 14, 16))
        # Olho
        pygame.draw.circle(surf, (0, 0, 0), (52, h // 2 - 3), 2)

    elif nome == "Sapo-Cururu":
        # Corpo arredondado robusto
        pygame.draw.ellipse(surf, cor, (w // 2 - 18, h // 2 - 10, 36, 26))
        # Verrugas / manchas
        for vx, vy in [(w // 2 - 6, h // 2), (w // 2 + 4, h // 2 - 4), (w // 2 - 10, h // 2 + 6), (w // 2 + 8, h // 2 + 4)]:
            pygame.draw.circle(surf, cor_escura, (vx, vy), 3)
        # Patas traseiras dobradas
        pygame.draw.ellipse(surf, cor_escura, (w // 2 - 24, h // 2 + 2, 14, 12))
        pygame.draw.ellipse(surf, cor_escura, (w // 2 + 10, h // 2 + 2, 14, 12))
        # Olhos bulbosos no topo
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 - 8, h // 2 - 12), 6)
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 - 8, h // 2 - 12), 3)
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 + 8, h // 2 - 12), 6)
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 + 8, h // 2 - 12), 3)

    elif nome == "Salamandra":
        # Corpo preto com manchas amarelas vibrantes
        pygame.draw.ellipse(surf, (30, 30, 30), (w // 2 - 8, h // 2 - 20, 16, 40))
        # Manchas amarelas
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 - 2, h // 2 - 12), 5)
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 + 3, h // 2 + 4), 4)
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 - 3, h // 2 + 14), 4)
        # Patas abertas
        pygame.draw.line(surf, (30, 30, 30), (w // 2 - 6, h // 2 - 10), (w // 2 - 20, h // 2 - 16), 3)
        pygame.draw.line(surf, (30, 30, 30), (w // 2 + 6, h // 2 - 10), (w // 2 + 20, h // 2 - 16), 3)
        pygame.draw.line(surf, (30, 30, 30), (w // 2 - 6, h // 2 + 10), (w // 2 - 20, h // 2 + 16), 3)
        pygame.draw.line(surf, (30, 30, 30), (w // 2 + 6, h // 2 + 10), (w // 2 + 20, h // 2 + 16), 3)
        # Cabeça
        pygame.draw.circle(surf, (30, 30, 30), (w // 2, h // 2 - 20), 8)
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 - 4, h // 2 - 22), 2)
        pygame.draw.circle(surf, (255, 215, 0), (w // 2 + 4, h // 2 - 22), 2)

    else:
        # Fallback genérico bonito com silhueta e olhos
        pygame.draw.circle(surf, cor, (w // 2, h // 2), 22)
        pygame.draw.circle(surf, cor_escura, (w // 2, h // 2), 22, 3)
        pygame.draw.circle(surf, (255, 255, 255), (w // 2 + 8, h // 2 - 6), 4)
        pygame.draw.circle(surf, (0, 0, 0), (w // 2 + 9, h // 2 - 6), 2)

    return surf


# =============================================================================
# HIERARQUIA DE CLASSES DE ANIMAIS (POO - SEÇÃO 8 DO GDD)
# =============================================================================
class Animal(pygame.sprite.Sprite):
    """
    Classe base para todos os animais do jogo.
    Implementa comportamento de física 2D, animação, interatividade e ficha educativa.
    """
    def __init__(self, nome, especie, classe_bio, habitat, alimentacao, curiosidade,
                 x, y, image_filename=None, som_texto="..."):
        super().__init__()
        self.nome = nome
        self.especie = especie
        self.classe_bio = classe_bio
        self.habitat = habitat
        self.alimentacao = alimentacao
        self.curiosidade = curiosidade
        self.image_filename = image_filename
        self.som_texto = som_texto

        # Estado no jogo
        self.descoberto = False
        self.no_zoologico = False
        self.recinto_atual = None

        # Posicionamento e movimentação autônoma (idle / wandering)
        self.origem_x = x
        self.origem_y = y
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.move_timer = random.randint(1000, 3000)
        self.limite_raio = 140

        # Animação
        self.frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 200
        self.olhando_direita = True

        self._carregar_graficos()
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(int(self.pos_x), int(self.pos_y)))

        # Cache de imagem para a Ficha Educativa (tamanho maior para visualização limpa)
        self.imagem_grande = self._criar_imagem_ampliada()
        self.imagem_silhueta = self._criar_silhueta()

    def _carregar_graficos(self):
        """Carrega do disco se existir ou gera sprite pixel-art procedural."""
        carregado = False
        if self.image_filename:
            caminho = os.path.join("assets", self.image_filename)
            if os.path.exists(caminho):
                try:
                    img = pygame.image.load(caminho).convert_alpha()
                    w, h = img.get_size()
                    # Redimensiona mantendo proporção para caber em 64x64
                    escala = min(64 / w, 64 / h)
                    novo_w = max(16, int(w * escala))
                    novo_h = max(16, int(h * escala))
                    img_scaled = pygame.transform.smoothscale(img, (novo_w, novo_h))

                    # Cria superfície 64x64 centralizada
                    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
                    surf.blit(img_scaled, ((64 - novo_w) // 2, (64 - novo_h) // 2))

                    self.frames.append(surf)
                    # Cria segundo frame com leve respiração para dar vida ao animal
                    surf2 = pygame.Surface((64, 64), pygame.SRCALPHA)
                    img_squash = pygame.transform.smoothscale(img, (novo_w + 2, max(14, novo_h - 2)))
                    surf2.blit(img_squash, ((64 - (novo_w + 2)) // 2, (64 - (novo_h - 2)) // 2 + 1))
                    self.frames.append(surf2)

                    carregado = True
                except Exception as e:
                    print(f"Aviso ao carregar {caminho}: {e}")

        if not carregado:
            base_surf = gerar_sprite_procedural(self.nome, (64, 64))
            self.frames.append(base_surf)
            # Frame 2 levemente pulsando
            base_surf2 = pygame.transform.smoothscale(base_surf, (64, 62))
            surf_final = pygame.Surface((64, 64), pygame.SRCALPHA)
            surf_final.blit(base_surf2, (0, 2))
            self.frames.append(surf_final)

    def _criar_imagem_ampliada(self):
        """Gera imagem nítida de 140x140 para a ficha educativa."""
        if self.frames:
            return pygame.transform.smoothscale(self.frames[0], (140, 140))
        return pygame.Surface((140, 140), pygame.SRCALPHA)

    def _criar_silhueta(self):
        """Gera uma silhueta preta misteriosa para animais ainda não descobertos."""
        if not self.frames:
            return pygame.Surface((64, 64), pygame.SRCALPHA)
        sil = self.frames[0].copy()
        sil.fill((30, 30, 40, 255), special_flags=pygame.BLEND_RGBA_MULT)
        return sil

    def update(self, dt, limites_area=None):
        """Atualiza animação e movimentação orgânica do animal."""
        # Animação
        if len(self.frames) > 1:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                img_atual = self.frames[self.current_frame]
                if not self.olhando_direita:
                    self.image = pygame.transform.flip(img_atual, True, False)
                else:
                    self.image = img_atual

        # Comportamento de vaguear (wandering)
        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_timer = random.randint(1500, 4500)
            if random.random() < 0.6:  # 60% chance de mover
                ang = random.uniform(0, 2 * math.pi)
                vel = random.uniform(0.3, 0.9)
                self.vel_x = math.cos(ang) * vel
                self.vel_y = math.sin(ang) * vel
                if self.vel_x < -0.1:
                    self.olhando_direita = False
                elif self.vel_x > 0.1:
                    self.olhando_direita = True
            else:
                self.vel_x = 0.0
                self.vel_y = 0.0

        # Aplica movimento
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        # Se tiver limites de recinto ou área, mantém o animal contido
        if limites_area:
            pad = 28
            self.pos_x = max(limites_area.left + pad, min(limites_area.right - pad, self.pos_x))
            self.pos_y = max(limites_area.top + pad, min(limites_area.bottom - pad, self.pos_y))
        else:
            # Mantém próximo da origem no mapa selvagem
            dist = math.hypot(self.pos_x - self.origem_x, self.pos_y - self.origem_y)
            if dist > self.limite_raio:
                dx = self.origem_x - self.pos_x
                dy = self.origem_y - self.pos_y
                self.vel_x = (dx / dist) * 0.5
                self.vel_y = (dy / dist) * 0.5

        self.rect.center = (int(self.pos_x), int(self.pos_y))

    def emitir_som(self):
        """Retorna representação sonora do animal para interface e balão."""
        return self.som_texto

    def obter_ficha_educativa(self):
        """Retorna dicionário completo com dados científicos do animal."""
        return {
            "nome": self.nome,
            "especie": self.especie,
            "classe": self.classe_bio,
            "habitat": self.habitat,
            "alimentacao": self.alimentacao,
            "curiosidade": self.curiosidade,
            "termoregulacao": self.obter_termoregulacao(),
            "respiracao": self.obter_respiracao(),
            "som": self.emitir_som()
        }

    # Métodos polimórficos sobrescritos pelas subclasses
    def obter_termoregulacao(self):
        return "Indefinida"

    def obter_respiracao(self):
        return "Pulmonar"


# =============================================================================
# SUBCLASSES ZOOLOGICAS (POLIMORFISMO E HERANÇA)
# =============================================================================
class Mamifero(Animal):
    """Animais vertebrados endotérmicos, com glândulas mamárias e pelos."""
    def __init__(self, nome, especie, habitat, alimentacao, curiosidade, x, y, image_filename=None, som_texto="Grrr!"):
        super().__init__(nome, especie, "Mamífero", habitat, alimentacao, curiosidade, x, y, image_filename, som_texto)

    def obter_termoregulacao(self):
        return "Endotérmico (sangue quente)"

    def obter_respiracao(self):
        return "Pulmonar completa (diafragma)"


class Ave(Animal):
    """Animais vertebrados endotérmicos com penas, bicos e asas."""
    def __init__(self, nome, especie, habitat, alimentacao, curiosidade, x, y, image_filename=None, som_texto="Piu-Piu!"):
        super().__init__(nome, especie, "Ave", habitat, alimentacao, curiosidade, x, y, image_filename, som_texto)

    def obter_termoregulacao(self):
        return "Endotérmico (alta taxa metabólica)"

    def obter_respiracao(self):
        return "Pulmonar com sacos aéreos"


class Reptil(Animal):
    """Animais vertebrados ectotérmicos com escamas ou carapaça córnea."""
    def __init__(self, nome, especie, habitat, alimentacao, curiosidade, x, y, image_filename=None, som_texto="Ssshh!"):
        super().__init__(nome, especie, "Réptil", habitat, alimentacao, curiosidade, x, y, image_filename, som_texto)

    def obter_termoregulacao(self):
        return "Ectotérmico (regulado pelo sol)"

    def obter_respiracao(self):
        return "Pulmonar eficiente"


class Peixe(Animal):
    """Animais vertebrados aquáticos com brânquias e nadadeiras."""
    def __init__(self, nome, especie, habitat, alimentacao, curiosidade, x, y, image_filename=None, som_texto="Glub-Glub!"):
        super().__init__(nome, especie, "Peixe", habitat, alimentacao, curiosidade, x, y, image_filename, som_texto)

    def obter_termoregulacao(self):
        return "Ectotérmico (aquático)"

    def obter_respiracao(self):
        return "Branquial (filtra oxigênio da água)"


class Anfibio(Animal):
    """Animais vertebrados que passam por metamorfose, com pele úmida permeável."""
    def __init__(self, nome, especie, habitat, alimentacao, curiosidade, x, y, image_filename=None, som_texto="Croac-Croac!"):
        super().__init__(nome, especie, "Anfíbio", habitat, alimentacao, curiosidade, x, y, image_filename, som_texto)

    def obter_termoregulacao(self):
        return "Ectotérmico (depende do ambiente)"

    def obter_respiracao(self):
        return "Cutânea (pela pele) e Pulmonar"


# =============================================================================
# BANCO DE DADOS DE ANIMAIS DO JOGO (20 ESPÉCIES ABRANGENDO 5 CLASSES)
# =============================================================================
def criar_banco_animais_completo():
    """Instancia a coleção de animais com todos os dados científicos exigidos pelo GDD."""
    animais = [
        # --- MAMÍFEROS (Savana) ---
        Mamifero(
            nome="Leão",
            especie="Panthera leo",
            habitat="Savana",
            alimentacao="Carnívoro",
            curiosidade="Vive em grupos familiares chamados alcateias/coalizões, liderados pelas leoas nas caçadas.",
            x=240, y=260,
            image_filename="leao.png",
            som_texto="ROAAAR!"
        ),
        Mamifero(
            nome="Elefante",
            especie="Loxodonta africana",
            habitat="Savana",
            alimentacao="Herbívoro",
            curiosidade="Possui mais de 40 mil músculos na tromba e excelente memória a longo prazo.",
            x=450, y=210,
            image_filename="elefante.png",
            som_texto="FUUUUN!"
        ),
        Mamifero(
            nome="Girafa",
            especie="Giraffa camelopardalis",
            habitat="Savana",
            alimentacao="Herbívoro",
            curiosidade="É o animal mais alto do mundo; sua língua de até 45 cm alcança folhas entre espinhos de acácia.",
            x=680, y=280,
            image_filename="girafa.png",
            som_texto="Hummm..."
        ),
        Mamifero(
            nome="Zebra",
            especie="Equus quagga",
            habitat="Savana",
            alimentacao="Herbívoro",
            curiosidade="Suas listras únicas funcionam como camuflagem contra moscas tsé-tsé e predadores.",
            x=850, y=230,
            image_filename="zebra.png",
            som_texto="Iii-haaa!"
        ),
        Mamifero(
            nome="Guepardo",
            especie="Acinonyx jubatus",
            habitat="Savana",
            alimentacao="Carnívoro",
            curiosidade="Acelera de 0 a 100 km/h em menos de 3 segundos, sendo o mamífero terrestre mais veloz.",
            x=180, y=420,
            image_filename="guepardo.png",
            som_texto="Churrr!"
        ),

        # --- MAMÍFEROS (Tropical / Floresta) ---
        Mamifero(
            nome="Macaco",
            especie="Sapajus apella",
            habitat="Tropical",
            alimentacao="Onívoro",
            curiosidade="Usa pedras como ferramentas para quebrar sementes duras e nozes na floresta tropical.",
            x=1150, y=260,
            image_filename=None,
            som_texto="Uhh-Ah-Ah!"
        ),
        Mamifero(
            nome="Raposa",
            especie="Vulpes vulpes",
            habitat="Tropical",
            alimentacao="Onívoro",
            curiosidade="Possui audição tão aguçada que consegue ouvir pequenos roedores se movendo sob o solo.",
            x=1380, y=220,
            image_filename=None,
            som_texto="Yap-yap!"
        ),
        Mamifero(
            nome="Cervo",
            especie="Cervus elaphus",
            habitat="Tropical",
            alimentacao="Herbívoro",
            curiosidade="Os machos trocam de galhada anualmente; os novos chifres crescem cobertos por pele aveludada.",
            x=1520, y=360,
            image_filename=None,
            som_texto="Bramido!"
        ),

        # --- AVES (Aquático / Tropical / Floresta) ---
        Ave(
            nome="Pinguim",
            especie="Aptenodytes forsteri",
            habitat="Aquático",
            alimentacao="Piscívoro",
            curiosidade="Suas asas funcionam como barbatanas eficientes, permitindo mergulhos a até 500 metros.",
            x=320, y=1050,
            image_filename="pinguim.png",
            som_texto="Quaac!"
        ),
        Ave(
            nome="Arara",
            especie="Ara ararauna",
            habitat="Tropical",
            alimentacao="Herbívoro (Sementes e Frutos)",
            curiosidade="Forma casais monogâmicos para a vida inteira e ajuda a reflorestar dispersando sementes.",
            x=1260, y=420,
            image_filename=None,
            som_texto="Craaah!"
        ),
        Ave(
            nome="Tetraz-Negro",
            especie="Tetrao tetrix",
            habitat="Tropical",
            alimentacao="Herbívoro",
            curiosidade="Durante o cortejo nupcial na primavera, exibe suas penas da cauda em formato de lira.",
            x=1440, y=500,
            image_filename=None,
            som_texto="Glu-glu-tchur!"
        ),

        # --- RÉPTEIS (Répteis & Aquático) ---
        Reptil(
            nome="Crocodilo",
            especie="Crocodylus niloticus",
            habitat="Répteis",
            alimentacao="Carnívoro",
            curiosidade="Possui uma das mordidas mais fortes do planeta e existe há mais de 80 milhões de anos.",
            x=1200, y=980,
            image_filename=None,
            som_texto="Grrr-snap!"
        ),
        Reptil(
            nome="Cobra",
            especie="Micrurus corallinus",
            habitat="Répteis",
            alimentacao="Carnívoro",
            curiosidade="Capta partículas químicas no ar com sua língua bifurcada para rastrear presas no ambiente.",
            x=1420, y=1080,
            image_filename=None,
            som_texto="Tss-ssss!"
        ),
        Reptil(
            nome="Tartaruga",
            especie="Chelonia mydas",
            habitat="Aquático",
            alimentacao="Herbívoro",
            curiosidade="Pode migrar milhares de quilômetros navegando pelo campo magnético da Terra.",
            x=540, y=1120,
            image_filename=None,
            som_texto="Hiss..."
        ),

        # --- PEIXES (Aquático) ---
        Peixe(
            nome="Peixe-Palhaço",
            especie="Amphiprion ocellaris",
            habitat="Aquático",
            alimentacao="Onívoro",
            curiosidade="Vive protegido entre os tentáculos venenosos de anêmonas graças a um muco especial na pele.",
            x=720, y=1060,
            image_filename=None,
            som_texto="Glub-glub!"
        ),
        Peixe(
            nome="Pirarucu",
            especie="Arapaima gigas",
            habitat="Aquático",
            alimentacao="Carnívoro",
            curiosidade="Conhecido como o gigante das águas doces, precisa subir à superfície para respirar ar atmosférico.",
            x=880, y=1180,
            image_filename=None,
            som_texto="Chomp-glub!"
        ),

        # --- ANFÍBIOS (Répteis & Pântano) ---
        Anfibio(
            nome="Sapo-Cururu",
            especie="Rhinella marina",
            habitat="Répteis",
            alimentacao="Insetívoro",
            curiosidade="Possui glândulas paratoides que liberam substâncias de defesa contra predadores.",
            x=1080, y=1160,
            image_filename=None,
            som_texto="Croac-coac!"
        ),
        Anfibio(
            nome="Salamandra",
            especie="Salamandra salamandra",
            habitat="Répteis",
            alimentacao="Insetívoro",
            curiosidade="Suas cores vivas (amarelo e preto) sinalizam a predadores que ela é impalatável e tóxica.",
            x=1320, y=1200,
            image_filename=None,
            som_texto="Pfft!"
        ),

        # --- MAMÍFEROS ADICIONAIS DE EXPLORAÇÃO ---
        Mamifero(
            nome="Javali",
            especie="Sus scrofa",
            habitat="Tropical",
            alimentacao="Onívoro",
            curiosidade="Possui presas afiadas de crescimento contínuo e faro apurado para encontrar raízes e fungos.",
            x=1560, y=460,
            image_filename=None,
            som_texto="Oinc-oinc!"
        ),
        Mamifero(
            nome="Lebre",
            especie="Lepus europaeus",
            habitat="Savana",
            alimentacao="Herbívoro",
            curiosidade="Pode atingir até 70 km/h em ziguezague com suas longas pernas para despistar predadores.",
            x=340, y=470,
            image_filename=None,
            som_texto="Focinho!"
        )
    ]
    return animais
