import math
import os
import pygame

# =============================================================================
# CORES DOS BIOMAS DO MAPA DE EXPLORAÇÃO
# =============================================================================
BIOMA_SAVANA_CHAO = (212, 175, 115)       # Solo dourado de savana
BIOMA_TROPICAL_CHAO = (46, 125, 50)       # Verde vivo tropical
BIOMA_AQUATICO_CHAO = (41, 128, 185)      # Água azul do oceano / costa
BIOMA_AQUATICO_PRAIA = (244, 208, 111)    # Areia da praia
BIOMA_REPTEIS_CHAO = (58, 77, 44)         # Verde pântano musgoso

COR_CAMINHO_ZOO = (210, 205, 195)
COR_BORDA_CAMINHO = (160, 155, 145)


class Camera:
    """Câmera de rolagem suave para o mapa de exploração."""
    def __init__(self, largura_tela, altura_tela, largura_mundo, altura_mundo):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.largura_mundo = largura_mundo
        self.altura_mundo = altura_mundo
        self.offset_x = 0
        self.offset_y = 0

    def seguir(self, alvo_x, alvo_y):
        self.offset_x = max(0, min(self.largura_mundo - self.largura_tela, int(alvo_x - self.largura_tela // 2)))
        self.offset_y = max(0, min(self.altura_mundo - self.altura_tela, int(alvo_y - self.altura_tela // 2)))

    def aplicar_rect(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

    def aplicar_pos(self, pos):
        return (pos[0] - self.offset_x, pos[1] - self.offset_y)


class CenaExploracao:
    """
    Cena de Exploração dos Biomas Selvagens (GDD 1, 5).
    O jogador viaja por 4 biomas:
    - Savana (Noroeste)
    - Floresta Tropical (Nordeste)
    - Região Aquática e Costeira (Sudoeste)
    - Santuário de Répteis & Anfíbios (Sudeste)
    """
    def __init__(self, largura_tela, altura_tela, lista_animais, jogador):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.largura_mundo = 1800
        self.altura_mundo = 1400

        self.jogador = jogador
        self.animais = lista_animais
        self.camera = Camera(largura_tela, altura_tela, self.largura_mundo, self.altura_mundo)
        self.rect_mundo = pygame.Rect(0, 0, self.largura_mundo, self.altura_mundo)

        # Superfície do mapa pré-renderizada para alta performance
        self.surf_mapa = pygame.Surface((self.largura_mundo, self.altura_mundo))
        self._construir_mapa_biomas()

    def _construir_mapa_biomas(self):
        """Renderiza o terreno dos 4 biomas com detalhes naturais."""
        meio_x = self.largura_mundo // 2
        meio_y = self.altura_mundo // 2

        # 1. Savana (Noroeste)
        pygame.draw.rect(self.surf_mapa, BIOMA_SAVANA_CHAO, (0, 0, meio_x, meio_y))
        # Acácias e tufos secos
        for ox, oy in [(150, 150), (450, 120), (700, 200), (300, 400), (600, 480)]:
            pygame.draw.circle(self.surf_mapa, (160, 130, 70), (ox, oy), 26)
            pygame.draw.circle(self.surf_mapa, (140, 110, 50), (ox, oy), 20)

        # 2. Floresta Tropical (Nordeste)
        pygame.draw.rect(self.surf_mapa, BIOMA_TROPICAL_CHAO, (meio_x, 0, meio_x, meio_y))
        # Copa de árvores densas
        for ox, oy in [(meio_x + 180, 140), (meio_x + 400, 220), (meio_x + 650, 160),
                       (meio_x + 220, 420), (meio_x + 500, 460), (meio_x + 720, 380)]:
            pygame.draw.circle(self.surf_mapa, (27, 94, 32), (ox, oy), 38)
            pygame.draw.circle(self.surf_mapa, (56, 142, 60), (ox + 5, oy - 5), 30)

        # 3. Região Aquática (Sudoeste)
        pygame.draw.rect(self.surf_mapa, BIOMA_AQUATICO_CHAO, (0, meio_y, meio_x, meio_y))
        # Faixa de areia de praia no topo e margem
        pygame.draw.rect(self.surf_mapa, BIOMA_AQUATICO_PRAIA, (0, meio_y - 20, meio_x, 40))
        # Recifes e ondas suaves
        for oy in range(meio_y + 60, self.altura_mundo - 50, 60):
            pygame.draw.line(self.surf_mapa, (129, 212, 250), (40, oy), (meio_x - 40, oy), 3)

        # 4. Santuário de Répteis & Pântano (Sudeste)
        pygame.draw.rect(self.surf_mapa, BIOMA_REPTEIS_CHAO, (meio_x, meio_y, meio_x, meio_y))
        # Poças de lodo e vitórias-régias
        for ox, oy in [(meio_x + 200, meio_y + 160), (meio_x + 520, meio_y + 220),
                       (meio_x + 320, meio_y + 440), (meio_x + 680, meio_y + 480)]:
            pygame.draw.ellipse(self.surf_mapa, (38, 50, 32), (ox - 40, oy - 25, 80, 50))
            pygame.draw.circle(self.surf_mapa, (76, 175, 80), (ox, oy), 14)

        # Divisórias naturais suaves entre os biomas
        pygame.draw.line(self.surf_mapa, (90, 80, 70), (meio_x, 0), (meio_x, self.altura_mundo), 4)
        pygame.draw.line(self.surf_mapa, (90, 80, 70), (0, meio_y), (self.largura_mundo, meio_y), 4)

        # Placas indicativas nos biomas
        fonte_placa = pygame.font.SysFont("Arial", 16, bold=True)
        placas = [
            ("BIOMA SAVANA", (meio_x // 2, 35)),
            ("BIOMA TROPICAL", (meio_x + meio_x // 2, 35)),
            ("REGIÃO AQUÁTICA", (meio_x // 2, meio_y + 35)),
            ("SANTUÁRIO DE RÉPTEIS & ANFÍBIOS", (meio_x + meio_x // 2, meio_y + 35))
        ]
        for texto, pos in placas:
            surf_t = fonte_placa.render(f"📍 {texto}", True, (240, 240, 240))
            px, py = pos
            r_placa = pygame.Rect(px - surf_t.get_width() // 2 - 12, py - 4, surf_t.get_width() + 24, 26)
            pygame.draw.rect(self.surf_mapa, (20, 25, 30, 220), r_placa, border_radius=6)
            self.surf_mapa.blit(surf_t, (px - surf_t.get_width() // 2, py))

    def update(self, dt):
        self.jogador.update(dt, limites_mundo=self.rect_mundo)
        self.camera.seguir(self.jogador.pos_x, self.jogador.pos_y)

        # Atualiza animais livres na natureza
        for animal in self.animais:
            if not animal.no_zoologico:
                animal.update(dt)

    def draw(self, screen, fontes, exibir_dicas=True):
        # Blit da janela visível do mapa
        sub_mapa = self.surf_mapa.subsurface((self.camera.offset_x, self.camera.offset_y, self.largura_tela, self.altura_tela))
        screen.blit(sub_mapa, (0, 0))

        # Desenha animais livres visíveis na tela
        animal_mais_proximo = None
        dist_min = 75.0

        for animal in self.animais:
            if not animal.no_zoologico:
                rect_visivel = self.camera.aplicar_rect(animal.rect)
                if rect_visivel.colliderect(pygame.Rect(0, 0, self.largura_tela, self.altura_tela)):
                    screen.blit(animal.image, rect_visivel)

                    # Calcula proximidade com o jogador
                    dist = math.hypot(self.jogador.pos_x - animal.pos_x, self.jogador.pos_y - animal.pos_y)
                    if dist <= dist_min:
                        animal_mais_proximo = (animal, rect_visivel)

        # Desenha o Jogador
        rect_jogador = self.camera.aplicar_rect(self.jogador.rect)
        screen.blit(self.jogador.image, rect_jogador)

        # Dica visual interativa sobre o animal próximo (GDD 1, 5)
        if animal_mais_proximo and exibir_dicas:
            animal, r_vis = animal_mais_proximo
            # Contorno de destaque pulsante
            pygame.draw.rect(screen, (255, 215, 0), r_vis.inflate(10, 10), 2, border_radius=6)

            txt_dica = f"[E] Examinar {animal.nome}" if not animal.descoberto else f"[E] Consultar {animal.nome}"
            surf_dica = fontes["pequena"].render(txt_dica, True, (255, 255, 255))
            dica_rect = surf_dica.get_rect(center=(r_vis.centerx, r_vis.top - 16))

            fundo_dica = dica_rect.inflate(14, 6)
            pygame.draw.rect(screen, (15, 20, 25, 220), fundo_dica, border_radius=4)
            pygame.draw.rect(screen, (241, 196, 15), fundo_dica, 1, border_radius=4)
            screen.blit(surf_dica, dica_rect)

        return animal_mais_proximo[0] if animal_mais_proximo else None


class CenaZoologico:
    """
    Cena do Zoológico Educativo Completo (GDD 1, 3, 5.5, 8).
    Exibe os recintos temáticos com os animais alocados, passeios de pedestres
    e praça central de visitação.
    """
    def __init__(self, largura_tela, altura_tela, zoologico, jogador):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.zoologico = zoologico
        self.jogador = jogador
        self.rect_tela = pygame.Rect(0, 0, largura_tela, altura_tela)

        # Tenta carregar fundo1.png se existir
        self.fundo_img = None
        caminho_fundo = os.path.join("assets", "fundo1.png")
        if os.path.exists(caminho_fundo):
            try:
                raw_bg = pygame.image.load(caminho_fundo).convert()
                self.fundo_img = pygame.transform.smoothscale(raw_bg, (largura_tela, altura_tela))
            except Exception as e:
                print(f"Aviso ao carregar fundo1: {e}")

    def update(self, dt):
        self.jogador.update(dt, limites_mundo=self.rect_tela)
        self.zoologico.update(dt)

    def draw(self, screen, fontes, exibir_dicas=True):
        fonte_m = fontes["media"]
        fonte_p = fontes["pequena"]

        # 1. Fundo do Zoológico
        if self.fundo_img:
            screen.blit(self.fundo_img, (0, 0))
            # Camada translúcida suave para destacar os recintos
            velo = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
            velo.fill((10, 25, 10, 60))
            screen.blit(velo, (0, 0))
        else:
            screen.fill((50, 115, 50))  # Grama bem cuidada do zoo

        # 2. Corredores de Passeio para Visitantes
        # Corredor Vertical Central
        pygame.draw.rect(screen, COR_CAMINHO_ZOO, (485, 56, 50, self.altura_tela - 86))
        pygame.draw.rect(screen, COR_BORDA_CAMINHO, (485, 56, 50, self.altura_tela - 86), 2)

        # Corredor Horizontal Central
        pygame.draw.rect(screen, COR_CAMINHO_ZOO, (0, 365, self.largura_tela, 50))
        pygame.draw.rect(screen, COR_BORDA_CAMINHO, (0, 365, self.largura_tela, 50), 2)

        # Praça Central / Chafariz do Zoológico
        centro_x = self.largura_tela // 2
        centro_y = 390
        pygame.draw.circle(screen, COR_CAMINHO_ZOO, (centro_x, centro_y), 50)
        pygame.draw.circle(screen, (41, 128, 185), (centro_x, centro_y), 32)
        pygame.draw.circle(screen, (129, 212, 250), (centro_x, centro_y), 20)
        pygame.draw.circle(screen, (255, 255, 255), (centro_x, centro_y), 8)

        # 3. Desenha os 4 Recintos Temáticos
        self.zoologico.draw(screen, fonte_m, fonte_p)

        # 4. Desenha o Jogador
        screen.blit(self.jogador.image, self.jogador.rect)

        # 5. Verifica interação com animais dentro dos recintos
        animal_focado = None
        for recinto in self.zoologico.recintos.values():
            for animal in recinto.animais:
                dist = math.hypot(self.jogador.pos_x - animal.pos_x, self.jogador.pos_y - animal.pos_y)
                if dist <= 75:
                    animal_focado = animal
                    if exibir_dicas:
                        pygame.draw.rect(screen, (255, 215, 0), animal.rect.inflate(10, 10), 2, border_radius=6)
                        txt = fontes["pequena"].render(f"[E] Consultar {animal.nome}", True, (255, 255, 255))
                        r_txt = txt.get_rect(center=(animal.rect.centerx, animal.rect.top - 16))
                        bg_txt = r_txt.inflate(12, 6)
                        pygame.draw.rect(screen, (15, 20, 25, 220), bg_txt, border_radius=4)
                        screen.blit(txt, r_txt)

        return animal_focado
