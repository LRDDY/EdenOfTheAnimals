import os
import math
import random
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

        # Botões do HUD distribuídos ordenadamente no topo direito
        self.btn_modo = Botao((largura - 530, 10, 125, 36), "[Z] Zoológico", COR_VERDE_ESCURO, COR_VERDE)
        self.btn_livro = Botao((largura - 395, 10, 125, 36), "[B] Coleção", (142, 68, 173), (155, 89, 182))
        self.btn_menu = Botao((largura - 260, 10, 125, 36), "☰ Menu [ESC]", (52, 73, 94), (44, 62, 80))
        self.btn_som = Botao((largura - 125, 10, 115, 36), "[M] Áudio", (70, 80, 95), (90, 100, 115))

    def update(self, mouse_pos):
        self.btn_modo.update(mouse_pos)
        self.btn_livro.update(mouse_pos)
        self.btn_menu.update(mouse_pos)
        self.btn_som.update(mouse_pos)

    def draw(self, screen, colecao, modo_atual, audio_mutado, volume_audio, fontes):
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
        screen.blit(txt_tit, (96, 10))

        txt_cont = fonte_p.render(f"Descobertos: {qtd}/{total} ({pct:.1f}%)", True, COR_CINZA)
        screen.blit(txt_cont, (96, 30))

        # Barra de Progresso estilizada (como no GDD 5.4: ████████░░░░░)
        bar_x = 295
        bar_y = 18
        bar_w = 185
        bar_h = 20
        pygame.draw.rect(screen, (35, 40, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
        prog_w = int((pct / 100.0) * bar_w)
        if prog_w > 0:
            cor_barra = COR_VERDE if pct >= 100 else (COR_AMARELO if pct >= 50 else COR_AZUL)
            pygame.draw.rect(screen, cor_barra, (bar_x, bar_y, prog_w, bar_h), border_radius=10)
        pygame.draw.rect(screen, (100, 110, 130), (bar_x, bar_y, bar_w, bar_h), width=2, border_radius=10)

        # Atualiza texto dos botões
        self.btn_modo.texto = "[Z] Explorar" if modo_atual == "zoologico" else "[Z] Zoológico"
        vol_pct = int(volume_audio * 100) if not audio_mutado else 0
        self.btn_som.texto = f"[M] Som: {vol_pct}%" if not audio_mutado else "[M] Som: Mudo"

        # Desenha Botões
        self.btn_modo.draw(screen, fonte_p)
        self.btn_livro.draw(screen, fonte_p)
        self.btn_menu.draw(screen, fonte_p)
        self.btn_som.draw(screen, fonte_p)

        # Barra Inferior com Guia Rápido de Atalhos
        faixa_inf = pygame.Surface((self.largura, 30), pygame.SRCALPHA)
        faixa_inf.fill((20, 24, 32, 200))
        screen.blit(faixa_inf, (0, self.altura - 30))
        pygame.draw.line(screen, (50, 56, 70), (0, self.altura - 30), (self.largura, self.altura - 30), 1)

        txt_atalhos = fonte_p.render(
            "WASD / Setas: Mover  |  E / Clique: Examinar Animal  |  Z: Alternar Zoológico  |  B: Enciclopédia  |  ESC: Menu Principal",
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


# =============================================================================
# TELA DE INÍCIO / MENU PRINCIPAL (COMEÇAR, CONFIGURAÇÃO, SAIR)
# =============================================================================
class TelaInicio:
    """
    Tela de Início temática para Eden of the Animals.
    Possui os botões Começar, Configuração e Sair, vitrine animada de animais e créditos.
    """
    def __init__(self, largura_tela, altura_tela, lista_animais):
        self.largura = largura_tela
        self.altura = altura_tela
        self.lista_animais = lista_animais

        # Tenta carregar fundo1.png se disponível
        self.fundo_img = None
        caminho_fundo = os.path.join("assets", "fundo1.png")
        if os.path.exists(caminho_fundo):
            try:
                raw_bg = pygame.image.load(caminho_fundo).convert()
                self.fundo_img = pygame.transform.smoothscale(raw_bg, (largura_tela, altura_tela))
            except Exception as e:
                print(f"Aviso fundo menu: {e}")

        # Partículas flutuantes decorativas (simulam folhas e pólen na brisa)
        self.particulas = []
        for _ in range(30):
            self.particulas.append({
                "x": random.randint(0, largura_tela),
                "y": random.randint(0, altura_tela),
                "vel_y": random.uniform(0.4, 1.1),
                "vel_x": random.uniform(-0.3, 0.3),
                "raio": random.randint(2, 4),
                "cor": random.choice([(80, 220, 100, 150), (255, 230, 130, 170), (120, 210, 255, 140)])
            })

        # Três Botões Principais Centralizados (Começar, Configuração, Sair)
        btn_w = 340
        btn_h = 52
        centro_x = (largura_tela - btn_w) // 2
        y_inicial = 385
        espacamento = 68

        self.btn_comecar = Botao(
            (centro_x, y_inicial, btn_w, btn_h),
            "▶  COMEÇAR",
            cor_fundo=(39, 174, 96),
            cor_hover=(46, 204, 113),
            cor_texto=COR_BRANCO
        )

        self.btn_config = Botao(
            (centro_x, y_inicial + espacamento, btn_w, btn_h),
            "⚙  CONFIGURAÇÃO",
            cor_fundo=(41, 128, 185),
            cor_hover=(52, 152, 219),
            cor_texto=COR_BRANCO
        )

        self.btn_sair = Botao(
            (centro_x, y_inicial + espacamento * 2, btn_w, btn_h),
            "✖  SAIR",
            cor_fundo=(192, 57, 43),
            cor_hover=(231, 76, 60),
            cor_texto=COR_BRANCO
        )

        # Seleciona animais para a vitrine visual no menu
        self.animais_vitrine = []
        nomes_destaque = ["Leão", "Girafa", "Elefante", "Pinguim", "Zebra", "Arara"]
        for nome in nomes_destaque:
            encontrado = next((a for a in lista_animais if a.nome == nome), None)
            if encontrado:
                self.animais_vitrine.append(encontrado)

        self.tempo_anim = 0

    def update(self, dt, mouse_pos):
        self.tempo_anim += dt
        self.btn_comecar.update(mouse_pos)
        self.btn_config.update(mouse_pos)
        self.btn_sair.update(mouse_pos)

        # Atualiza partículas
        for p in self.particulas:
            p["y"] -= p["vel_y"]
            p["x"] += p["vel_x"]
            if p["y"] < -10:
                p["y"] = self.altura + 10
                p["x"] = random.randint(0, self.largura)

    def draw(self, screen, fontes, jogo_ja_iniciado=False):
        # 1. Fundo com sobreposição escura translúcida
        if self.fundo_img:
            screen.blit(self.fundo_img, (0, 0))
            overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
            overlay.fill((12, 18, 28, 180))
            screen.blit(overlay, (0, 0))
        else:
            screen.fill((20, 26, 36))

        # 2. Desenha partículas flutuantes
        for p in self.particulas:
            s = pygame.Surface((p["raio"] * 2, p["raio"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, p["cor"], (p["raio"], p["raio"]), p["raio"])
            screen.blit(s, (int(p["x"]), int(p["y"])))

        # 3. Painel do Título Central
        tit_w = 780
        tit_h = 145
        tit_x = (self.largura - tit_w) // 2
        tit_y = 45

        s_tit = pygame.Surface((tit_w, tit_h), pygame.SRCALPHA)
        s_tit.fill((20, 26, 38, 225))
        screen.blit(s_tit, (tit_x, tit_y))
        pygame.draw.rect(screen, COR_AMARELO, (tit_x, tit_y, tit_w, tit_h), width=2, border_radius=16)

        # Título Principal em Destaque
        fonte_tit_grande = pygame.font.SysFont("Arial", 42, bold=True)
        txt_tit = fonte_tit_grande.render("EDEN OF THE ANIMALS", True, COR_AMARELO)
        screen.blit(txt_tit, txt_tit.get_rect(center=(self.largura // 2, tit_y + 40)))

        # Subtítulo 1
        txt_sub1 = fontes["media"].render("Preservação da Fauna • Simulação & Coleção 2D", True, (240, 245, 255))
        screen.blit(txt_sub1, txt_sub1.get_rect(center=(self.largura // 2, tit_y + 80)))

        # Subtítulo Acadêmico
        txt_acad = fontes["pequena"].render("Projeto Acadêmico — Dyogo Emanuel Pires Ramos  |  Ciências da Natureza & Zoologia", True, (200, 215, 230))
        screen.blit(txt_acad, txt_acad.get_rect(center=(self.largura // 2, tit_y + 115)))

        # 4. Vitrine Visual de Animais no Meio da Tela
        vitrine_y = 265
        num_vitrine = len(self.animais_vitrine)
        if num_vitrine > 0:
            espaco = self.largura // (num_vitrine + 1)
            for idx, animal in enumerate(self.animais_vitrine):
                vx = espaco * (idx + 1)
                offset_ondulacao = math.sin((self.tempo_anim / 400.0) + idx * 0.9) * 4
                vy = vitrine_y + int(offset_ondulacao)

                # Base circular verde brilhante
                pygame.draw.ellipse(screen, (30, 42, 54), (vx - 38, vy + 24, 76, 20))
                pygame.draw.ellipse(screen, COR_VERDE, (vx - 38, vy + 24, 76, 20), width=1)

                # Sprite do Animal
                screen.blit(animal.image, animal.image.get_rect(center=(vx, vy)))

                # Nome do Animal
                txt_n = fontes["pequena"].render(animal.nome, True, (225, 230, 240))
                screen.blit(txt_n, txt_n.get_rect(center=(vx, vy + 46)))

        # 5. Botões Principais
        self.btn_comecar.texto = "▶  CONTINUAR" if jogo_ja_iniciado else "▶  COMEÇAR"
        self.btn_comecar.draw(screen, fontes["media"])
        self.btn_config.draw(screen, fontes["media"])
        self.btn_sair.draw(screen, fontes["media"])

        # 6. Rodapé
        txt_rodape = fontes["pequena"].render("Eden of the Animals • Python 3 & Pygame • 60 FPS • Dyogo Emanuel Pires Ramos", True, (150, 160, 175))
        screen.blit(txt_rodape, txt_rodape.get_rect(center=(self.largura // 2, self.altura - 22)))

    def tratar_clique(self, mouse_pos):
        if self.btn_comecar.rect.collidepoint(mouse_pos):
            return "comecar"
        if self.btn_config.rect.collidepoint(mouse_pos):
            return "configuracao"
        if self.btn_sair.rect.collidepoint(mouse_pos):
            return "sair"
        return None


# =============================================================================
# MODAL DE CONFIGURAÇÃO (AJUSTES DE ÁUDIO, VELOCIDADE, DICAS E CRÉDITOS)
# =============================================================================
class ModalConfiguracao:
    """
    Janela de Configurações acessada pelo Menu Inicial ou pelo jogo.
    Permite controlar áudio/volume, velocidade do personagem, dicas no mapa e reiniciar coleção.
    """
    def __init__(self, largura_tela, altura_tela):
        self.largura = largura_tela
        self.altura = altura_tela

        self.w = 680
        self.h = 550
        self.x = (largura_tela - self.w) // 2
        self.y = (altura_tela - self.h) // 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        # Botão Fechar no Canto Superior
        self.btn_fechar = Botao((self.x + self.w - 44, self.y + 14, 32, 32), "X", (192, 57, 43), (231, 76, 60))

        # 1. Controles de Áudio
        self.btn_audio = Botao((self.x + 360, self.y + 80, 140, 36), "Áudio: 100%", (39, 174, 96), (46, 204, 113))
        self.btn_vol_menos = Botao((self.x + 512, self.y + 80, 42, 36), "-", (52, 73, 94), (70, 90, 115))
        self.btn_vol_mais = Botao((self.x + 562, self.y + 80, 42, 36), "+", (52, 73, 94), (70, 90, 115))

        # 2. Controles de Jogabilidade
        self.btn_velocidade = Botao((self.x + 360, self.y + 138, 244, 36), "Velocidade: Normal", (41, 128, 185), (52, 152, 219))
        self.btn_dicas = Botao((self.x + 360, self.y + 196, 244, 36), "Dicas no Mapa: SIM", (142, 68, 173), (155, 89, 182))

        # 3. Reiniciar Coleção
        self.btn_resetar = Botao((self.x + 360, self.y + 254, 244, 36), "Reiniciar Coleção", (211, 84, 0), (230, 126, 34))

        # 4. Botão Voltar Inferior
        self.btn_voltar = Botao((self.x + (self.w - 240) // 2, self.y + self.h - 55, 240, 40), "✔ VOLTAR", COR_AZUL_ESCURO, COR_AZUL)

    def update(self, mouse_pos):
        self.btn_fechar.update(mouse_pos)
        self.btn_audio.update(mouse_pos)
        self.btn_vol_menos.update(mouse_pos)
        self.btn_vol_mais.update(mouse_pos)
        self.btn_velocidade.update(mouse_pos)
        self.btn_dicas.update(mouse_pos)
        self.btn_resetar.update(mouse_pos)
        self.btn_voltar.update(mouse_pos)

    def draw(self, screen, fontes, audio_mutado, volume_audio, vel_jogador, exibir_dicas):
        fonte_p = fontes["pequena"]
        fonte_m = fontes["media"]
        fonte_g = fontes["grande"]

        # Overlay escuro no fundo
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Painel Central
        painel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        painel.fill((25, 30, 42, 245))
        screen.blit(painel, self.rect.topleft)
        pygame.draw.rect(screen, COR_AMARELO, self.rect, width=2, border_radius=14)

        # Cabeçalho
        txt_cab = fonte_g.render("⚙ CONFIGURAÇÕES DO JOGO", True, COR_AMARELO)
        screen.blit(txt_cab, (self.x + 30, self.y + 20))

        self.btn_fechar.draw(screen, fonte_m)

        # Linha Divisória
        pygame.draw.line(screen, (70, 80, 100), (self.x + 30, self.y + 60), (self.x + self.w - 30, self.y + 60), 2)

        # 1. Linha Áudio
        txt_a = fonte_m.render("Efeitos Sonoros & Volume:", True, COR_BRANCO)
        screen.blit(txt_a, (self.x + 35, self.y + 86))
        vol_pct = int(volume_audio * 100) if not audio_mutado else 0
        self.btn_audio.texto = f"Som: {vol_pct}%" if not audio_mutado else "Som: MUDO"
        self.btn_audio.cor_fundo = (39, 174, 96) if not audio_mutado else (90, 100, 115)
        self.btn_audio.draw(screen, fonte_p)
        self.btn_vol_menos.draw(screen, fonte_m)
        self.btn_vol_mais.draw(screen, fonte_m)

        # 2. Linha Velocidade do Personagem
        txt_v = fonte_m.render("Velocidade do Personagem:", True, COR_BRANCO)
        screen.blit(txt_v, (self.x + 35, self.y + 144))
        tipo_vel = "Normal (4.5)" if vel_jogador <= 4.5 else "Rápida (6.0)"
        self.btn_velocidade.texto = f"Velocidade: {tipo_vel}"
        self.btn_velocidade.draw(screen, fonte_p)

        # 3. Linha Dicas no Mapa
        txt_d = fonte_m.render("Auxílio Visual & Dicas:", True, COR_BRANCO)
        screen.blit(txt_d, (self.x + 35, self.y + 202))
        self.btn_dicas.texto = "Dicas na Tela: SIM" if exibir_dicas else "Dicas na Tela: NÃO"
        self.btn_dicas.cor_fundo = (142, 68, 173) if exibir_dicas else (80, 85, 95)
        self.btn_dicas.draw(screen, fonte_p)

        # 4. Linha Reiniciar Coleção
        txt_r = fonte_m.render("Reiniciar Coleção / Zoo:", True, COR_BRANCO)
        screen.blit(txt_r, (self.x + 35, self.y + 260))
        self.btn_resetar.draw(screen, fonte_p)

        # 5. Caixa Informativa / Créditos Acadêmicos
        info_rect = pygame.Rect(self.x + 35, self.y + 315, self.w - 70, 150)
        pygame.draw.rect(screen, (32, 38, 52), info_rect, border_radius=10)
        pygame.draw.rect(screen, (60, 70, 90), info_rect, width=1, border_radius=10)

        tit_info = fonte_m.render("📖 Sobre o Projeto Acadêmico:", True, COR_AMARELO)
        screen.blit(tit_info, (info_rect.x + 16, info_rect.y + 12))

        linhas_info = [
            "• Jogo: Eden of the Animals (Zoologia & Educação Ambiental)",
            "• Autor: Dyogo Emanuel Pires Ramos",
            "• Arquitetura: POO (Classes Animal, Jogador, Zoologico, Colecao, Cenas)",
            "• Tecnologias: Python 3 & Pygame 2D",
            "• Biomas: Savana, Floresta Tropical, Região Aquática, Santuário de Répteis"
        ]
        iy = info_rect.y + 38
        for linha in linhas_info:
            txt_li = fonte_p.render(linha, True, (215, 225, 235))
            screen.blit(txt_li, (info_rect.x + 16, iy))
            iy += 21

        # Botão Voltar Inferior
        self.btn_voltar.draw(screen, fonte_m)

    def tratar_clique(self, pos):
        if self.btn_fechar.rect.collidepoint(pos) or self.btn_voltar.rect.collidepoint(pos):
            return "voltar"
        if self.btn_audio.rect.collidepoint(pos):
            return "alternar_som"
        if self.btn_vol_menos.rect.collidepoint(pos):
            return "vol_menos"
        if self.btn_vol_mais.rect.collidepoint(pos):
            return "vol_mais"
        if self.btn_velocidade.rect.collidepoint(pos):
            return "alternar_velocidade"
        if self.btn_dicas.rect.collidepoint(pos):
            return "alternar_dicas"
        if self.btn_resetar.rect.collidepoint(pos):
            return "resetar"
        return None

