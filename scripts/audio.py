import math
import struct
import pygame

class SistemaAudio:
    """
    Sistema de áudio com síntese procedural pura de ondas sonoras (PCM 16-bit).
    Permite efeitos sonoros instantâneos e música ambiente relaxante sem necessidade
    de arquivos de áudio externos, garantindo 100% de confiabilidade e portabilidade.
    """
    def __init__(self):
        self.disponivel = False
        self.mutado = False
        self.canal_musica = None
        self.sons = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.disponivel = True
            self._gerar_sons_procedurais()
        except Exception as e:
            print(f"Aviso de inicialização de áudio: {e}")
            self.disponivel = False

    def _gerar_onda_senoidal(self, freq, duracao_ms, volume=0.3, decaimento=True):
        """Gera bytes de onda senoidal de 16 bits com envelope suave."""
        taxa = 22050
        num_amostras = int(taxa * (duracao_ms / 1000.0))
        amostras = []
        for i in range(num_amostras):
            t = float(i) / taxa
            fator_fade = 1.0
            if decaimento:
                # Envelope de decaimento suave para evitar estalidos
                fator_fade = max(0.0, 1.0 - (i / num_amostras))
            val = math.sin(2.0 * math.pi * freq * t) * 32767.0 * volume * fator_fade
            amostras.append(int(val))

        buffer = bytearray()
        for s in amostras:
            buffer.extend(struct.pack('<h', max(-32767, min(32767, s))))

        return pygame.mixer.Sound(buffer=bytes(buffer))

    def _gerar_sons_procedurais(self):
        if not self.disponivel:
            return

        # 1. Clique de menu
        self.sons["clique"] = self._gerar_onda_senoidal(580, 45, volume=0.25)

        # 2. Descoberta de animal (Arpeggio alegre C-E-G-C)
        taxa = 22050
        notas = [523.25, 659.25, 783.99, 1046.50]  # Dó5, Mi5, Sol5, Dó6
        buffer = bytearray()
        dur_por_nota = int(taxa * 0.1)
        for nota in notas:
            for i in range(dur_por_nota):
                t = float(i) / taxa
                fade = 1.0 - (i / dur_por_nota)
                val = int(math.sin(2.0 * math.pi * nota * t) * 32767 * 0.28 * fade)
                buffer.extend(struct.pack('<h', max(-32767, min(32767, val))))
        self.sons["descoberta"] = pygame.mixer.Sound(buffer=bytes(buffer))

        # 3. Alocar no Zoológico (Acorde suave de sucesso)
        self.sons["sucesso"] = self._gerar_onda_senoidal(880, 180, volume=0.3)

        # 4. Aviso / Erro (Tom baixo sutil)
        self.sons["aviso"] = self._gerar_onda_senoidal(220, 150, volume=0.25)

        # 5. Conquista / Level Up (Fanfarra harmônica)
        notas_fanfarra = [440, 554.37, 659.25, 880]
        buf_fanfarra = bytearray()
        for n in notas_fanfarra:
            amostras_n = int(taxa * 0.12)
            for i in range(amostras_n):
                t = float(i) / taxa
                val = int(math.sin(2.0 * math.pi * n * t) * 32767 * 0.3 * (1.0 - i / amostras_n))
                buf_fanfarra.extend(struct.pack('<h', max(-32767, min(32767, val))))
        self.sons["conquista"] = pygame.mixer.Sound(buffer=bytes(buf_fanfarra))

    def tocar(self, nome_som):
        """Reproduz um som procedural se o áudio estiver habilitado."""
        if not self.disponivel or self.mutado:
            return
        som = self.sons.get(nome_som)
        if som:
            try:
                som.play()
            except Exception:
                pass

    def alternar_mudo(self):
        """Ativa ou desativa o áudio do jogo."""
        self.mutado = not self.mutado
        return self.mutado
