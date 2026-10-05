"""
=============================================================================
PROJETO: Eden of the Animals
GDD: Dyogo Emanuel Pires Ramos
TIPO: Jogo 2D Educativo, Simulação e Coleção (Zoologia e Educação Ambiental)
TECNOLOGIAS: Python 3 & Pygame
ARQUITETURA: Programação Orientada a Objetos (POO)
=============================================================================
Hierarquia Central do Sistema (Seção 8 do GDD):
Jogo
│
├── Animal
│   ├── Mamifero
│   ├── Ave
│   ├── Reptil
│   ├── Peixe
│   └── Anfibio
│
├── Jogador
├── Zoologico
│   └── Recinto
├── Colecao
├── Interface (HUD, FichaEducativa, LivroColecao, Notificacoes)
└── Cenas (CenaExploracao, CenaZoologico)
=============================================================================
"""

import sys
import os
import pygame

# Importação dos módulos orientados a objetos da pasta scripts/
from scripts.animais import (
    Animal, Mamifero, Ave, Reptil, Peixe, Anfibio,
    criar_banco_animais_completo
)
from scripts.jogador import Jogador
from scripts.zoologico import Zoologico, Recinto
from scripts.colecao import Colecao
from scripts.interfaces import HUD, FichaEducativa, LivroColecao, NotificacaoManager
from scripts.cenas import CenaExploracao, CenaZoologico
from scripts.audio import SistemaAudio


# -----------------------------------------------------------------------------
# CONSTANTES DE CONFIGURAÇÃO DO JOGO
# -----------------------------------------------------------------------------
LARGURA_TELA = 1024
ALTURA_TELA = 768
FPS = 60
TITULO_JOGO = "Eden of the Animals — Dyogo Emanuel Pires Ramos"


# -----------------------------------------------------------------------------
# CLASSE PRINCIPAL: JOGO (COORDENADORA POO - SEÇÃO 8 DO GDD)
# -----------------------------------------------------------------------------
class Jogo:
    """
    Classe mestre do jogo.
    Coordena ciclo de execução, eventos, transições de cena, áudio e interfaces.
    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITULO_JOGO)
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.clock = pygame.time.Clock()

        # Carrega fontes com fallback para fontes do sistema
        self.fontes = {
            "pequena": pygame.font.SysFont("Arial", 14),
            "media": pygame.font.SysFont("Arial", 18, bold=True),
            "grande": pygame.font.SysFont("Arial", 24, bold=True)
        }

        # Sistema de Áudio Procedural Puro
        self.audio = SistemaAudio()

        # Banco de Dados de Animais e Coleção (GDD 2, 4, 8)
        self.lista_animais = criar_banco_animais_completo()
        self.colecao = Colecao(self.lista_animais)

        # Avatar do Jogador (GDD 8)
        self.jogador = Jogador(x=400, y=300)

        # Sistema do Zoológico e Recintos (GDD 5.5, 8)
        self.zoologico = Zoologico()

        # Cenas do Jogo
        self.cena_exploracao = CenaExploracao(LARGURA_TELA, ALTURA_TELA, self.lista_animais, self.jogador)
        self.cena_zoologico = CenaZoologico(LARGURA_TELA, ALTURA_TELA, self.zoologico, self.jogador)
        self.modo_atual = "exploracao"  # "exploracao" ou "zoologico"

        # Interfaces de Usuário (HUD, Modais e Notificações)
        self.hud = HUD(LARGURA_TELA, ALTURA_TELA)
        self.notificacoes = NotificacaoManager(LARGURA_TELA)
        self.ficha_ativa = None
        self.livro_colecao = None
        self.animal_em_foco = None

        # Histórico de Nível para Notificações de Level Up (GDD 4)
        self.nivel_anterior = self.colecao.obter_nivel()[0]

        # Mensagem inicial de boas-vindas
        self.notificacoes.exibir(
            "Bem-vindo ao Eden of the Animals!",
            "Explore os biomas com WASD e aproxime-se dos animais para examinar.",
            (241, 196, 15),
            duracao_ms=4500
        )

    def alternar_modo(self):
        """Alterna entre o Safari Selvagem e a Gestão do Zoológico (GDD 1, 5)."""
        self.audio.tocar("clique")
        if self.modo_atual == "exploracao":
            self.modo_atual = "zoologico"
            # Centraliza o jogador na praça do zoológico
            self.jogador.pos_x = float(LARGURA_TELA // 2)
            self.jogador.pos_y = float(390)
            self.notificacoes.exibir("Zoológico Educativo", "Visite os recintos e acompanhe os animais acomodados.")
        else:
            self.modo_atual = "exploracao"
            # Retorna o jogador ao bioma de exploração
            self.jogador.pos_x = float(450)
            self.jogador.pos_y = float(350)
            self.notificacoes.exibir("Exploração Silvestre", "Explore a Savana, Floresta Tropical, Águas e Pântano.")

    def abrir_ficha_animal(self, animal):
        """Descobre o animal (se novo) e abre sua Ficha Educativa detalhada."""
        nova_descoberta = self.colecao.descobrir(animal)
        if nova_descoberta:
            self.audio.tocar("descoberta")
            self.notificacoes.exibir(
                f"🎉 Nova Espécie Descoberta: {animal.nome}!",
                f"Classe: {animal.classe_bio} | Habitat: {animal.habitat}",
                cor=(46, 204, 113),
                duracao_ms=4000
            )
            self._verificar_progressao_nivel()
        else:
            self.audio.tocar("clique")

        self.ficha_ativa = FichaEducativa(animal, self.zoologico, LARGURA_TELA, ALTURA_TELA)

    def _verificar_progressao_nivel(self):
        """Verifica se o jogador atingiu novo patamar segundo a Seção 4 do GDD."""
        nivel_atual, titulo_atual = self.colecao.obter_nivel()
        if nivel_atual > self.nivel_anterior:
            self.nivel_anterior = nivel_atual
            self.audio.tocar("conquista")
            self.notificacoes.exibir(
                f"🏆 Subiu de Nível! Nível {nivel_atual}: {titulo_atual}",
                f"{self.colecao.quantidade_descobertos} animais catalogados na enciclopédia!",
                cor=(255, 215, 0),
                duracao_ms=5000
            )

    def run(self):
        """Ciclo principal (Game Loop) em 60 FPS."""
        rodando = True
        while rodando:
            dt = self.clock.tick(FPS)
            rodando = self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()

        pygame.quit()
        sys.exit()

    def tratar_eventos(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # Tecla ESC: fecha modais ou encerra se nenhum modal estiver ativo
                if event.key == pygame.K_ESCAPE:
                    if self.ficha_ativa:
                        self.ficha_ativa = None
                        self.audio.tocar("clique")
                    elif self.livro_colecao:
                        self.livro_colecao = None
                        self.audio.tocar("clique")
                    else:
                        return False

                # Tecla E: interagir com animal próximo
                elif event.key == pygame.K_e:
                    if not self.ficha_ativa and not self.livro_colecao and self.animal_em_foco:
                        self.abrir_ficha_animal(self.animal_em_foco)
                    elif self.ficha_ativa:
                        self.ficha_ativa = None
                        self.audio.tocar("clique")

                # Tecla Z: alternar entre exploração e zoológico
                elif event.key == pygame.K_z:
                    if not self.ficha_ativa and not self.livro_colecao:
                        self.alternar_modo()

                # Tecla B: abrir/fechar enciclopédia de coleção
                elif event.key == pygame.K_b:
                    self.audio.tocar("clique")
                    if self.livro_colecao:
                        self.livro_colecao = None
                    else:
                        self.ficha_ativa = None
                        self.livro_colecao = LivroColecao(self.colecao, LARGURA_TELA, ALTURA_TELA)

                # Tecla M: mutar/desmutar som
                elif event.key == pygame.K_m:
                    mutado = self.audio.alternar_mudo()
                    msg = "Áudio desativado (Mudo)" if mutado else "Áudio ativado"
                    self.notificacoes.exibir("Controle de Som", msg, duracao_ms=2000)

            # Eventos do Mouse (Cliques na interface e nos animais)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # 1. Se Ficha Educativa estiver aberta
                if self.ficha_ativa:
                    if self.ficha_ativa.btn_fechar.hover:
                        self.audio.tocar("clique")
                        self.ficha_ativa = None
                        continue

                    if self.ficha_ativa.btn_alocar.hover:
                        animal = self.ficha_ativa.animal
                        if not animal.no_zoologico:
                            sucesso, msg = self.zoologico.alocar_automaticamente(animal)
                            if sucesso:
                                self.audio.tocar("sucesso")
                                self.notificacoes.exibir("Zoológico Atualizado", msg, cor=(46, 204, 113))
                                # Atualiza botão na ficha
                                self.ficha_ativa.btn_alocar.texto = "No Zoológico ✓"
                                self.ficha_ativa.btn_alocar.cor_fundo = (60, 70, 80)
                            else:
                                self.audio.tocar("aviso")
                                self.notificacoes.exibir("Aviso de Acomodação", msg, cor=(231, 76, 60))
                        else:
                            self.audio.tocar("clique")
                            self.notificacoes.exibir("Status", f"{animal.nome} já reside no {animal.recinto_atual.nome}.")
                        continue

                # 2. Se Livro de Coleção estiver aberto
                elif self.livro_colecao:
                    acao, dados = self.livro_colecao.tratar_clique(event.pos)
                    if acao == "fechar":
                        self.audio.tocar("clique")
                        self.livro_colecao = None
                    elif acao == "aba":
                        self.audio.tocar("clique")
                    elif acao == "abrir_animal" and dados:
                        self.audio.tocar("clique")
                        self.abrir_ficha_animal(dados)
                    continue

                # 3. Cliques nos botões do HUD
                if self.hud.btn_modo.hover:
                    self.alternar_modo()
                    continue
                if self.hud.btn_livro.hover:
                    self.audio.tocar("clique")
                    self.livro_colecao = LivroColecao(self.colecao, LARGURA_TELA, ALTURA_TELA)
                    continue
                if self.hud.btn_som.hover:
                    mutado = self.audio.alternar_mudo()
                    msg = "Áudio desativado (Mudo)" if mutado else "Áudio ativado"
                    self.notificacoes.exibir("Controle de Som", msg, duracao_ms=2000)
                    continue

                # 4. Clique direto em um animal no cenário
                if not self.ficha_ativa and not self.livro_colecao:
                    if self.animal_em_foco:
                        self.abrir_ficha_animal(self.animal_em_foco)

        return True

    def atualizar(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.hud.update(mouse_pos)
        self.notificacoes.update(dt)

        # Se houver modal aberto, pausa atualização do jogo de fundo
        if self.ficha_ativa:
            self.ficha_ativa.update(mouse_pos)
            return

        if self.livro_colecao:
            self.livro_colecao.update(mouse_pos)
            return

        # Atualiza a cena ativa
        if self.modo_atual == "exploracao":
            self.cena_exploracao.update(dt)
        else:
            self.cena_zoologico.update(dt)

    def desenhar(self):
        # 1. Desenha a cena ativa e obtém animal sob foco de interação
        if self.modo_atual == "exploracao":
            self.animal_em_foco = self.cena_exploracao.draw(self.screen, self.fontes)
        else:
            self.animal_em_foco = self.cena_zoologico.draw(self.screen, self.fontes)

        # 2. Desenha HUD Superior e Inferior
        self.hud.draw(
            self.screen,
            self.colecao,
            self.modo_atual,
            self.audio.mutado,
            self.fontes
        )

        # 3. Notificações flutuantes no topo
        self.notificacoes.draw(self.screen, self.fontes)

        # 4. Modais (Ficha Educativa ou Livro da Coleção)
        if self.ficha_ativa:
            self.ficha_ativa.draw(self.screen, self.fontes)
        elif self.livro_colecao:
            self.livro_colecao.draw(self.screen, self.fontes)

        pygame.display.flip()


# -----------------------------------------------------------------------------
# PONTO DE ENTRADA DO SISTEMA
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    jogo = Jogo()
    jogo.run()