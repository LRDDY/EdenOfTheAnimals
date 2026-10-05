import pygame

# =============================================================================
# CORES TEMÁTICAS DOS RECINTOS
# =============================================================================
CORES_RECINTOS = {
    "Savana": {
        "chao": (222, 184, 135),     # Tom arenoso / savana dourada
        "borda": (160, 82, 45),      # Madeira escura
        "detalhe": (205, 133, 63)
    },
    "Tropical": {
        "chao": (46, 125, 50),       # Verde floresta tropical
        "borda": (27, 94, 32),
        "detalhe": (76, 175, 80)
    },
    "Aquático": {
        "chao": (33, 150, 243),      # Lago azul cristalino
        "borda": (2, 119, 189),
        "detalhe": (129, 212, 250)
    },
    "Répteis": {
        "chao": (85, 107, 47),       # Pântano verde musgo
        "borda": (62, 39, 35),
        "detalhe": (107, 142, 35)
    }
}


class Recinto:
    """
    Representa um recinto temático do zoológico (GDD 5.5).
    Cada recinto acomoda animais adequados ao seu habitat biológico.
    """
    def __init__(self, nome, tipo_habitat, rect, capacidade=6):
        self.nome = nome
        self.tipo_habitat = tipo_habitat  # "Savana", "Tropical", "Aquático", "Répteis"
        self.rect = pygame.Rect(rect)
        self.capacidade = capacidade
        self.animais = []

    def compatibilidade(self, animal):
        """
        Verifica se o animal é biologicamente compatível com o recinto (GDD 5.5).
        Retorna (compativel: bool, motivo: str).
        """
        if animal.habitat == self.tipo_habitat:
            return True, "Habitat perfeito para a espécie!"

        # Casos biológicos especiais
        if self.tipo_habitat == "Aquático" and (animal.classe_bio == "Peixe" or animal.nome in ["Pinguim", "Tartaruga"]):
            return True, "Ambiente aquático adequado para a espécie!"
        if self.tipo_habitat == "Répteis" and animal.classe_bio in ["Réptil", "Anfíbio"]:
            return True, "Temperatura e umidade ideais para répteis/anfíbios!"
        if self.tipo_habitat == "Tropical" and (animal.habitat in ["Tropical", "Floresta"] or animal.classe_bio == "Ave"):
            return True, "Vegetação rica apropriada!"

        return False, f"Este animal necessita de um recinto do tipo '{animal.habitat}', e não '{self.tipo_habitat}'."

    def adicionar_animal(self, animal):
        """Adiciona o animal ao recinto se houver vaga e for compatível."""
        compativel, msg = self.compatibilidade(animal)
        if not compativel:
            return False, msg

        if len(self.animais) >= self.capacidade:
            return False, f"O {self.nome} atingiu sua capacidade máxima ({self.capacidade} animais)."

        if animal not in self.animais:
            self.animais.append(animal)
            animal.no_zoologico = True
            animal.recinto_atual = self
            # Reposiciona o animal dentro da área do recinto
            animal.pos_x = float(self.rect.centerx + (len(self.animais) * 18 - 40))
            animal.pos_y = float(self.rect.centery + (len(self.animais) % 2 * 20 - 10))
            animal.rect.center = (int(animal.pos_x), int(animal.pos_y))
            return True, f"{animal.nome} acomodado com sucesso no {self.nome}!"

        return False, f"{animal.nome} já reside neste recinto."

    def remover_animal(self, animal):
        """Remove o animal do recinto."""
        if animal in self.animais:
            self.animais.remove(animal)
            animal.no_zoologico = False
            animal.recinto_atual = None
            return True
        return False

    def update(self, dt):
        """Atualiza a movimentação suave dos animais dentro do recinto cercado."""
        for animal in self.animais:
            animal.update(dt, limites_area=self.rect)

    def draw(self, screen, fonte_titulo, fonte_sub):
        """Desenha o recinto com cerca decorativa, chão temático e placa."""
        cores = CORES_RECINTOS.get(self.tipo_habitat, CORES_RECINTOS["Savana"])

        # Chão do recinto
        pygame.draw.rect(screen, cores["chao"], self.rect, border_radius=12)

        # Detalhes decorativos internos (lago ou textura de grama)
        if self.tipo_habitat == "Aquático":
            # Ondas no lago
            for oy in range(self.rect.top + 25, self.rect.bottom - 20, 30):
                pygame.draw.line(screen, cores["detalhe"], (self.rect.left + 20, oy), (self.rect.right - 20, oy), 2)
        elif self.tipo_habitat == "Savana":
            # Pequenos arbustos / tufos de vegetação seca
            pygame.draw.circle(screen, cores["detalhe"], (self.rect.left + 45, self.rect.top + 45), 12)
            pygame.draw.circle(screen, cores["detalhe"], (self.rect.right - 45, self.rect.bottom - 45), 14)
        elif self.tipo_habitat == "Tropical":
            # Folhagens decorativas
            pygame.draw.circle(screen, cores["detalhe"], (self.rect.centerx, self.rect.top + 30), 16)
            pygame.draw.circle(screen, cores["detalhe"], (self.rect.left + 35, self.rect.bottom - 35), 12)
        elif self.tipo_habitat == "Répteis":
            # Rochas de aquecimento solar
            pygame.draw.ellipse(screen, (100, 100, 95), (self.rect.centerx - 25, self.rect.centery - 15, 50, 30))

        # Cerca de contenção ao redor do recinto
        pygame.draw.rect(screen, cores["borda"], self.rect, width=4, border_radius=12)

        # Postes da cerca nos cantos
        canto_offset = [(self.rect.left, self.rect.top), (self.rect.right - 8, self.rect.top),
                        (self.rect.left, self.rect.bottom - 8), (self.rect.right - 8, self.rect.bottom - 8)]
        for cx, cy in canto_offset:
            pygame.draw.rect(screen, (50, 30, 20), (cx, cy, 8, 8), border_radius=2)

        # Placa de identificação no topo do recinto
        placa_w, placa_h = 210, 26
        placa_rect = pygame.Rect(self.rect.centerx - placa_w // 2, self.rect.top - 13, placa_w, placa_h)
        pygame.draw.rect(screen, (245, 235, 215), placa_rect, border_radius=6)
        pygame.draw.rect(screen, cores["borda"], placa_rect, 2, border_radius=6)

        texto_placa = f"{self.nome} ({len(self.animais)}/{self.capacidade})"
        surf_texto = fonte_sub.render(texto_placa, True, (40, 30, 20))
        screen.blit(surf_texto, surf_texto.get_rect(center=placa_rect.center))

        # Desenha os animais que habitam o recinto
        for animal in self.animais:
            screen.blit(animal.image, animal.rect)


class Zoologico:
    """
    Gerenciador principal do Zoológico Educativo (GDD 5.5 e 8).
    Organiza os recintos e a população de animais residentes.
    """
    def __init__(self):
        # 4 Grandes Recintos distribuídos harmonicamente na tela (1024x768)
        self.recintos = {
            "Savana": Recinto("Recinto da Savana", "Savana", (50, 70, 430, 290), capacidade=6),
            "Tropical": Recinto("Recinto Tropical", "Tropical", (540, 70, 430, 290), capacidade=6),
            "Aquático": Recinto("Recinto Aquático", "Aquático", (50, 420, 430, 290), capacidade=6),
            "Répteis": Recinto("Recinto dos Répteis", "Répteis", (540, 420, 430, 290), capacidade=6)
        }

    def total_animais_abrigados(self):
        return sum(len(r.animais) for r in self.recintos.values())

    def alocar_automaticamente(self, animal):
        """Encontra o recinto ideal compatível para o animal e o acomoda."""
        for recinto in self.recintos.values():
            compativel, _ = recinto.compatibilidade(animal)
            if compativel:
                sucesso, msg = recinto.adicionar_animal(animal)
                if sucesso:
                    return True, msg
        return False, "Nenhum recinto com vaga compatível encontrado."

    def update(self, dt):
        for recinto in self.recintos.values():
            recinto.update(dt)

    def draw(self, screen, fonte_titulo, fonte_sub):
        for recinto in self.recintos.values():
            recinto.draw(screen, fonte_titulo, fonte_sub)
