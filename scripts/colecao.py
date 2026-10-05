class Colecao:
    """
    Sistema central de Coleção e Progressão Zoológica (GDD 4, 5.4 e 8.1).
    Gerencia descobertas, níveis de progressão, porcentagem e estatísticas.
    """
    def __init__(self, lista_animais):
        self.todos_animais = lista_animais
        self.total = len(lista_animais)

    @property
    def descobertos(self):
        return [a for a in self.todos_animais if a.descoberto]

    @property
    def quantidade_descobertos(self):
        return len(self.descobertos)

    def descobrir(self, animal):
        """Marca animal como descoberto e retorna True se foi uma nova descoberta."""
        if not animal.descoberto:
            animal.descoberto = True
            return True
        return False

    def porcentagem_progresso(self):
        """Retorna porcentagem de conclusão (0.0 a 100.0)."""
        if self.total == 0:
            return 0.0
        return (self.quantidade_descobertos / self.total) * 100.0

    def obter_nivel(self):
        """
        Retorna (nivel: int, titulo: str) conforme Seção 4 do GDD:
        - Nível 1: 0–5 animais
        - Nível 2: 6–10 animais
        - Nível 3: 11–19 animais
        - Nível 4: 20+ animais (100% da coleção)
        """
        qtd = self.quantidade_descobertos
        if qtd >= 20:
            return 4, "Éden dos Animais (Coleção Completa!)"
        elif qtd >= 11:
            return 3, "Mestre Zoólogo (Zoológico em Expansão)"
        elif qtd >= 6:
            return 2, "Guardião da Fauna (Avanço da Coleção)"
        else:
            return 1, "Explorador Novato (Início da Jornada)"

    def animais_por_classe(self, classe_filtro=None):
        """Filtra animais por classe biológica (ou retorna todos se None/'Todos')."""
        if not classe_filtro or classe_filtro == "Todos":
            return self.todos_animais
        return [a for a in self.todos_animais if a.classe_bio == classe_filtro]

    def estatisticas_por_classe(self):
        """Gera resumo de quantos animais de cada classe foram descobertos."""
        classes = ["Mamífero", "Ave", "Réptil", "Peixe", "Anfíbio"]
        resumo = {}
        for c in classes:
            total_classe = sum(1 for a in self.todos_animais if a.classe_bio == c)
            desc_classe = sum(1 for a in self.todos_animais if a.classe_bio == c and a.descoberto)
            resumo[c] = (desc_classe, total_classe)
        return resumo
