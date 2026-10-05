import pygame

# =============================================================================
# CORES DA INTERFACE
# =============================================================================
COR_BRANCO = (255, 255, 255)
COR_PRETO = (15, 15, 20)
COR_AMARELO = (241, 196, 15)
COR_OURO = (255, 215, 0)
COR_VERDE = (46, 204, 113)
COR_VERDE_ESCURO = (34, 112, 62)
COR_AZUL = (52, 152, 219)
COR_AZUL_ESCURO = (41, 128, 185)
COR_CINZA = (180, 185, 190)
COR_CINZA_ESCURO = (40, 44, 52)
COR_PAINEL = (25, 28, 36, 235)
COR_CARD = (38, 42, 54)
COR_CARD_HOVER = (50, 56, 72)


class Botao:
    """Botão interativo com estados normal, hover e clique."""
    def __init__(self, rect, texto, cor_fundo=COR_AZUL, cor_hover=COR_AZUL_ESCURO, cor_texto=COR_BRANCO):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.hover = False

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        return self.hover

    def draw(self, screen, fonte):
        cor = self.cor_hover if self.hover else self.cor_fundo
        pygame.draw.rect(screen, cor, self.rect, border_radius=6)
        pygame.draw.rect(screen, (255, 255, 255, 80), self.rect, width=1, border_radius=6)

        surf_txt = fonte.render(self.texto, True, self.cor_texto)
        rect_txt = surf_txt.get_rect(center=self.rect.center)
        screen.blit(surf_txt, rect_txt)

    def clicado(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hover


class HUD:
    """
    Interface superior e inferior (GDD 5.4, 8).
    Exibe barra de progresso com porcentagem, nível, botões de ação e atalhos.
    """
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        # Botões do HUD
        self.btn_modo = Botao((largura - 420, 10, 130, 36), "[Z] Zoológico", COR_VERDE_ESCURO, COR_VERDE)
        self.btn_livro = Botao((largura - 275, 10, 140, 36), "[B] Coleção", (142, 68, 173), (155, 89, 182))
        self.btn_som = Botao((largura - 120, 10, 100, 36), "[M] Áudio", (70, 80, 95), (90, 100, 115))

    def update(self, mouse_pos):
        self.btn_modo.update(mouse_pos)
        self.btn_livro.update(mouse_pos)
        self.btn_som.update(mouse_pos)

    def draw(self, screen, colecao, modo_atual, audio_mutado, fontes):
        fonte_p = fontes["pequena"]
        fonte_m = fontes["media"]
        fonte_b = fontes["grande"]

        # Barra Superior translúcida
        faixa_sup = pygame.Surface((self.largura, 56), pygame.SRCALPHA)
        faixa_sup.fill((20, 24, 32, 220))
        screen.blit(faixa_sup, (0, 0))
        pygame.draw.line(screen, (60, 68, 85), (0, 56), (self.largura, 56), 2)

        # Informações de Nível e Coleção
        nivel_num, nivel_titulo = colecao.obter_nivel()
        pct = colecao.porcentagem_progresso()
        qtd = colecao.quantidade_descobertos
        total = colecao.total

        # Nível Badge
        pygame.draw.rect(screen, COR_AMARELO, (12, 10, 75, 36), border_radius=6)
        txt_nv = fonte_m.render(f"Nível {nivel_num}", True, (20, 20, 20))
        screen.blit(txt_nv, txt_nv.get_rect(center=(12 + 37, 10 + 18)))

        # Título do Nível e Animais
        txt_tit = fonte_m.render(f"{nivel_titulo}", True, COR_BRANCO)
        screen.blit(txt_tit, (98, 10))

        txt_cont = fonte_p.render(f"Descobertos: {qtd}/{total} ({pct:.1f}%)", True, COR_CINZA)
        screen.blit(txt_cont, (98, 30))

        # Barra de Progresso estilizada (como no GDD 5.4: ████████░░░░░)
        bar_x = 350
        bar_y = 18
        bar_w = 230
        bar_h = 20
        pygame.draw.rect(screen, (35, 40, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
        prog_w = int((pct / 100.0) * bar_w)
        if prog_w > 0:
            cor_barra = COR_VERDE if pct >= 100 else (COR_AMARELO if pct >= 50 else COR_AZUL)
            pygame.draw.rect(screen, cor_barra, (bar_x, bar_y, prog_w, bar_h), border_radius=10)
        pygame.draw.rect(screen, (100, 110, 130), (bar_x, bar_y, bar_w, bar_h), width=2, border_radius=10)

        # Atualiza texto do botão de modo
        self.btn_modo.texto = "[Z] Explorar" if modo_atual == "zoologico" else "[Z] Zoológico"
        self.btn_som.texto = "[M] Mudo" if audio_mutado else "[M] Som: ON"

        # Desenha Botões
        self.btn_modo.draw(screen, fonte_p)
        self.btn_livro.draw(screen, fonte_p)
        self.btn_som.draw(screen, fonte_p)

        # Barra Inferior com Guia Rápido de Atalhos
        faixa_inf = pygame.Surface((self.largura, 30), pygame.SRCALPHA)
        faixa_inf.fill((20, 24, 32, 200))
        screen.blit(faixa_inf, (0, self.altura - 30))
        pygame.draw.line(screen, (50, 56, 70), (0, self.altura - 30), (self.largura, self.altura - 30), 1)

        txt_atalhos = fonte_p.render(
            "WASD / Setas: Mover  |  E / Clique: Examinar Animal  |  Z: Alternar Zoológico  |  B: Enciclopédia  |  ESC: Fechar Ficha",
            True, (200, 205, 215)
        )
        screen.blit(txt_atalhos, txt_atalhos.get_rect(center=(self.largura // 2, self.altura - 15)))


class FichaEducativa:
    """
    Ficha de informações zoológicas e biológicas do animal (GDD 2.2, 5.1).
    Apresenta nome científico, classe, habitat, alimentação, termorregulação e curiosidades.
    """
    def __init__(self, animal, zoologico, largura_tela, altura_tela):
        self.animal = animal
        self.zoologico = zoologico
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        # Dimensões da janela modal
        self.w = 580
        self.h = 490
        self.x = (largura_tela - self.w) // 2
        self.y = (altura_tela - self.h) // 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # Botões
        self.btn_fechar = Botao((self.x + self.w - 42, self.y + 12, 30, 30), "X", (192, 57, 43), (231, 76, 60))

        # Botão de acomodação no zoológico
        ja_no_zoo = animal.no_zoologico
        txt_zoo = "No Zoológico ✓" if ja_no_zoo else "Acomodar no Zoológico"
        cor_zoo = (39, 174, 96) if not ja_no_zoo else (60, 70, 80)
        self.btn_alocar = Botao((self.x + 30, self.y + self.h - 55, self.w - 60, 38), txt_zoo, cor_zoo, (46, 204, 113))

    def update(self, mouse_pos):
        self.btn_fechar.update(mouse_pos)
        self.btn_alocar.update(mouse_pos)

    def draw(self, screen, fontes):
        fonte_p = fontes["pequena"]
        fonte_m = fontes["media"]
        fonte_g = fontes["grande"]

        # Sombra de fundo escurecida (dim background)
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        # Fundo do painel
        painel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        painel.fill(COR_PAINEL)
        screen.blit(painel, self.rect.topleft)

        # Moldura com detalhes dourados
        pygame.draw.rect(screen, COR_AMARELO, self.rect, width=3, border_radius=14)
        pygame.draw.rect(screen, (80, 85, 100), self.rect.inflate(-4, -4), width=1, border_radius=12)

        # Cabeçalho da Ficha
        txt_nome = fonte_g.render(self.animal.nome.upper(), True, COR_AMARELO)
        screen.blit(txt_nome, (self.x + 30, self.y + 20))

        txt_especie = fonte_m.render(f"Espécie: {self.animal.especie}", True, (210, 215, 225))
        screen.blit(txt_especie, (self.x + 30, self.y + 54))

        # Botão fechar
        self.btn_fechar.draw(screen, fonte_m)

        # Linha divisória
        pygame.draw.line(screen, (70, 78, 95), (self.x + 30, self.y + 84), (self.x + self.w - 30, self.y + 84), 2)

        # Imagem ampliada do animal com moldura
        img_rect = pygame.Rect(self.x + 30, self.y + 100, 140, 140)
        pygame.draw.rect(screen, (30, 34, 44), img_rect, border_radius=10)
        pygame.draw.rect(screen, (90, 100, 120), img_rect, width=2, border_radius=10)
        screen.blit(self.animal.imagem_grande, img_rect.topleft)

        # Som emitido
        txt_som = fonte_p.render(f"Som: \"{self.animal.emitir_som()}\"", True, COR_OURO)
        screen.blit(txt_som, (self.x + 30, self.y + 248))

        # Dados biológicos à direita da imagem
        dx = self.x + 190
        dy = self.y + 98

        dados = [
            ("Classe:", self.animal.classe_bio, COR_VERDE),
            ("Habitat:", self.animal.habitat, COR_AZUL),
            ("Alimentação:", self.animal.alimentacao, (230, 126, 34)),
            ("Termorregulação:", self.animal.obter_termoregulacao(), (241, 196, 15)),
            ("Respiração:", self.animal.obter_respiracao(), (52, 152, 219)),
            ("Status:", f"Acomodado no {self.animal.recinto_atual.nome}" if self.animal.no_zoologico else "Livre na Natureza", (155, 89, 182))
        ]

        for rotulo, valor, cor_val in dados:
            txt_r = fonte_p.render(rotulo, True, COR_CINZA)
            screen.blit(txt_r, (dx, dy))
            txt_v = fonte_p.render(valor, True, cor_val)
            screen.blit(txt_v, (dx + 115, dy))
            dy += 25

        # Bloco de Curiosidade Educativa (GDD 2.2)
        curio_rect = pygame.Rect(self.x + 30, self.y + 276, self.w - 60, 140)
        pygame.draw.rect(screen, (32, 36, 48), curio_rect, border_radius=10)
        pygame.draw.rect(screen, (60, 68, 85), curio_rect, width=1, border_radius=10)

        tit_curio = fonte_m.render("💡 Curiosidade Zoológica & Ecológica:", True, COR_AMARELO)
        screen.blit(tit_curio, (curio_rect.x + 14, curio_rect.y + 12))

        # Quebra de texto automática das curiosidades
        texto_curio = self.animal.curiosidade
        palavras = texto_curio.split(' ')
        linhas = []
        linha_atual = ""
        max_largura = curio_rect.width - 28

        for p in palavras:
            teste = linha_atual + p + " "
            if fonte_p.size(teste)[0] < max_largura:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = p + " "
        if linha_atual:
            linhas.append(linha_atual)

        cy = curio_rect.y + 40
        for l in linhas:
            txt_l = fonte_p.render(l, True, (230, 235, 240))
            screen.blit(txt_l, (curio_rect.x + 14, cy))
            cy += 20

        # Botão de Ação (Acomodar no Zoológico)
        self.btn_alocar.draw(screen, fonte_m)


class LivroColecao:
    """
    Enciclopédia / Livro de Coleção interativo (GDD 5.4 e 8).
    Exibe todas as espécies em grid, filtros por classe, silhuetas para desconhecidos
    e porcentagem de progresso detalhada.
    """
    def __init__(self, colecao, largura_tela, altura_tela):
        self.colecao = colecao
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

        self.w = 900
        self.h = 620
        self.x = (largura_tela - self.w) // 2
        self.y = (altura_tela - self.h) // 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # Botão Fechar
        self.btn_fechar = Botao((self.x + self.w - 42, self.y + 14, 30, 30), "X", (192, 57, 43), (231, 76, 60))

        # Abas de Filtro por Classe Biológica
        self.filtro_ativo = "Todos"
        self.abas = ["Todos", "Mamífero", "Ave", "Réptil", "Peixe", "Anfíbio"]
        self.botoes_aba = []
        aba_x = self.x + 30
        for aba in self.abas:
            btn = Botao((aba_x, self.y + 68, 120, 32), aba, COR_CARD, COR_AZUL)
            self.botoes_aba.append((aba, btn))
            aba_x += 128

        # Cards de animais
        self.cards = []
        self._montar_cards()

    def _montar_cards(self):
        self.cards = []
        animais = self.colecao.animais_por_classe(self.filtro_ativo)
        cols = 5
        card_w = 156
        card_h = 105
        esp_x = 18
        esp_y = 15
        start_x = self.x + 28
        start_y = self.y + 115

        for i, a in enumerate(animais):
            col = i % cols
            lin = i // cols
            cx = start_x + col * (card_w + esp_x)
            cy = start_y + lin * (card_h + esp_y)
            r = pygame.Rect(cx, cy, card_w, card_h)
            self.cards.append((a, r))

    def update(self, mouse_pos):
        self.btn_fechar.update(mouse_pos)
        for _, btn in self.botoes_aba:
            btn.update(mouse_pos)

    def draw(self, screen, fontes):
        fonte_p = fontes["pequena"]
        fonte_m = fontes["media"]
        fonte_g = fontes["grande"]

        # Escurece o fundo
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Painel do Livro
        painel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        painel.fill(COR_PAINEL)
        screen.blit(painel, self.rect.topleft)

        pygame.draw.rect(screen, (70, 130, 180), self.rect, width=3, border_radius=14)

        # Título
        tit = fonte_g.render("ENCICLOPÉDIA DA FAUNA — EDEN OF THE ANIMALS", True, COR_AMARELO)
        screen.blit(tit, (self.x + 30, self.y + 20))

        # Progresso resumo
        pct = self.colecao.porcentagem_progresso()
        txt_prog = fonte_p.render(f"Progresso Geral: {self.colecao.quantidade_descobertos}/{self.colecao.total} ({pct:.1f}%)", True, COR_BRANCO)
        screen.blit(txt_prog, (self.x + 580, self.y + 24))

        self.btn_fechar.draw(screen, fonte_m)

        # Desenha Abas de Filtro
        for nome_aba, btn in self.botoes_aba:
            if nome_aba == self.filtro_ativo:
                btn.cor_fundo = COR_AZUL
            else:
                btn.cor_fundo = COR_CARD
            btn.draw(screen, fonte_p)

        # Desenha Cards de Animais
        mouse_pos = pygame.mouse.get_pos()
        for animal, r in self.cards:
            is_hover = r.collidepoint(mouse_pos)

            if animal.descoberto:
                cor_card = COR_CARD_HOVER if is_hover else COR_CARD
                pygame.draw.rect(screen, cor_card, r, border_radius=8)
                pygame.draw.rect(screen, COR_VERDE if not is_hover else COR_AMARELO, r, width=2, border_radius=8)

                # Miniatura do animal
                mini = pygame.transform.smoothscale(animal.frames[0], (44, 44))
                screen.blit(mini, (r.x + 10, r.y + 12))

                # Nome e Classe
                txt_n = fonte_p.render(animal.nome, True, COR_BRANCO)
                screen.blit(txt_n, (r.x + 60, r.y + 16))

                txt_c = fonte_p.render(animal.classe_bio, True, COR_VERDE)
                screen.blit(txt_c, (r.x + 60, r.y + 36))

                # Status de zoológico
                st_zoo = "No Zoológico" if animal.no_zoologico else "Selvagem"
                cor_st = COR_OURO if animal.no_zoologico else COR_CINZA
                txt_z = fonte_p.render(st_zoo, True, cor_st)
                screen.blit(txt_z, (r.x + 12, r.y + 72))

            else:
                # Animal Desconhecido (GDD 5.4: "apresentados como desconhecidos")
                pygame.draw.rect(screen, (25, 27, 34), r, border_radius=8)
                pygame.draw.rect(screen, (55, 60, 75), r, width=1, border_radius=8)

                # Silhueta escura com interrogação
                sil_mini = pygame.transform.smoothscale(animal.imagem_silhueta, (44, 44))
                screen.blit(sil_mini, (r.x + 10, r.y + 12))

                txt_desc = fonte_p.render("???", True, (130, 135, 145))
                screen.blit(txt_desc, (r.x + 62, r.y + 20))

                txt_desconhecido = fonte_p.render("Não descoberto", True, (90, 95, 105))
                screen.blit(txt_desconhecido, (r.x + 62, r.y + 42))

                txt_dica = fonte_p.render(f"Habitat: {animal.habitat}", True, (70, 75, 85))
                screen.blit(txt_dica, (r.x + 12, r.y + 72))

    def tratar_clique(self, pos):
        """Trata cliques nas abas, botão fechar ou em cards de animais."""
        if self.btn_fechar.rect.collidepoint(pos):
            return "fechar", None

        for nome_aba, btn in self.botoes_aba:
            if btn.rect.collidepoint(pos):
                self.filtro_ativo = nome_aba
                self._montar_cards()
                return "aba", nome_aba

        for animal, r in self.cards:
            if r.collidepoint(pos) and animal.descoberto:
                return "abrir_animal", animal

        return None, None


class NotificacaoManager:
    """Gerencia popups animados de descobertas e conquistas no topo da tela."""
    def __init__(self, largura_tela):
        self.largura_tela = largura_tela
        self.mensagem = ""
        self.submensagem = ""
        self.cor = COR_AMARELO
        self.tempo_restante = 0

    def exibir(self, mensagem, submensagem="", cor=COR_AMARELO, duracao_ms=3500):
        self.mensagem = mensagem
        self.submensagem = submensagem
        self.cor = cor
        self.tempo_restante = duracao_ms

    def update(self, dt):
        if self.tempo_restante > 0:
            self.tempo_restante -= dt

    def draw(self, screen, fontes):
        if self.tempo_restante <= 0:
            return

        fonte_m = fontes["media"]
        fonte_p = fontes["pequena"]

        w, h = 480, 58
        x = (self.largura_tela - w) // 2
        y = 66

        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((20, 24, 32, 235))
        screen.blit(surf, (x, y))

        pygame.draw.rect(screen, self.cor, (x, y, w, h), width=2, border_radius=8)

        txt_p = fonte_m.render(self.mensagem, True, self.cor)
        screen.blit(txt_p, txt_p.get_rect(center=(x + w // 2, y + 18)))

        if self.submensagem:
            txt_s = fonte_p.render(self.submensagem, True, COR_BRANCO)
            screen.blit(txt_s, txt_s.get_rect(center=(x + w // 2, y + 40)))
