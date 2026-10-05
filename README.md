# Eden of the Animals 🐾🌿

**Autor:** Dyogo Emanuel Pires Ramos  
**Linha Temática:** Entretenimento & Educação Ambiental  
**Área do Conhecimento:** Ciências da Natureza — Zoologia e Conservação  
**Tecnologias:** Python 3 & Pygame  
**Paradigma:** Programação Orientada a Objetos (POO)

---

## 📖 1. Sobre o Projeto

**Eden of the Animals** é um jogo 2D educativo e de simulação em que o jogador atua como um Guardião e Zoólogo responsável por explorar biomas selvagens, resgatar e catalogar espécies animais e construir um Zoológico sustentável organizado em recintos adequados.

Ao interagir com os animais, o jogador tem acesso a **Fichas Educativas** completas com nome científico, classe zoológica, habitat, dieta alimentar, regulação térmica, tipo de respiração e curiosidades sobre o comportamento e a conservação da espécie.

---

## 🏛️ 2. Arquitetura Orientada a Objetos (POO)

O projeto foi estruturado seguindo rigorosamente a hierarquia exigida no **Game Design Document (GDD)**:

```text
Jogo (main.py)
│
├── Animal (scripts/animais.py)
│   ├── Mamifero
│   ├── Ave
│   ├── Reptil
│   ├── Peixe
│   └── Anfibio
│
├── Jogador (scripts/jogador.py)
├── Zoologico (scripts/zoologico.py)
│   └── Recinto
├── Colecao (scripts/colecao.py)
├── Interface (scripts/interfaces.py)
│   ├── HUD
│   ├── FichaEducativa
│   ├── LivroColecao
│   └── NotificacaoManager
├── Cenas (scripts/cenas.py)
│   ├── CenaExploracao
│   └── CenaZoologico
└── Audio (scripts/audio.py)
```

---

## 🦁 3. Espécies e Classes Zoológicas

O jogo conta com **20 espécies** distribuídas em 5 classes de vertebrados e 4 biomas:

| Classe | Espécies no Jogo | Habitat Natural |
|---|---|---|
| **Mamíferos** | Leão, Elefante, Girafa, Zebra, Guepardo, Macaco, Raposa, Cervo, Javali, Lebre | Savana e Floresta Tropical |
| **Aves** | Pinguim, Arara-Canindé, Tetraz-Negro | Áreas Polares/Costeiras e Floresta Tropical |
| **Répteis** | Crocodilo-do-Nilo, Cobra-Coral, Tartaruga-Marinha | Pântano, Floresta e Águas Costeiras |
| **Peixes** | Peixe-Palhaço, Pirarucu | Recifes de Coral e Rios Tropicais |
| **Anfíbios** | Sapo-Cururu, Salamandra-de-Fogo | Zonas Úmidas, Pântanos e Margens de Rios |

---

## 🎮 4. Controles do Jogo

| Tecla / Ação | Função |
|---|---|
| **W, A, S, D** ou **Setas** | Movimenta o personagem pelo mapa |
| **E** ou **Clique no Animal** | Examina o animal, descobre nova espécie e abre a Ficha Educativa |
| **Z** | Alterna entre o **Safari de Exploração** e o **Zoológico Educativo** |
| **B** | Abre/Fecha a **Enciclopédia da Fauna** (Livro de Coleção) |
| **M** | Ativa ou silencia os efeitos sonoros (**Mudo**) |
| **ESC** | Fecha janelas/fichas abertas ou encerra o jogo |
| **Mouse (Botão Esquerdo)** | Clica em botões, abas, cards de animais e botões de acomodação |

---

## 🏆 5. Sistema de Progressão e Níveis

A evolução do jogador é calculada com base na quantidade de animais catalogados:

- **Nível 1 (0 a 5 animais):** *Explorador Novato (Início da Jornada)*
- **Nível 2 (6 a 10 animais):** *Guardião da Fauna (Avanço da Coleção)*
- **Nível 3 (11 a 19 animais):** *Mestre Zoólogo (Zoológico em Expansão)*
- **Nível 4 (20 animais):** *Éden dos Animais (Coleção 100% Completa!)*

---

## 🏞️ 6. Recintos do Zoológico

O zoológico possui 4 grandes recintos cercados com validação biológica:
1. **Recinto da Savana:** Acomoda leões, elefantes, girafas, zebras, guepardos e lebres.
2. **Recinto Tropical:** Acomoda primatas, araras, raposas, javalis, cervos e aves silvestres.
3. **Recinto Aquático:** Acomoda pinguins, peixes-palhaço, pirarucus e tartarugas.
4. **Recinto dos Répteis & Anfíbios:** Acomoda crocodilos, cobras, sapos e salamandras.

---

## 🚀 7. Como Executar

Certifique-se de possuir o **Python 3** e o **Pygame** instalados:

```bash
pip install pygame
```

Execute o jogo diretamente na raiz do projeto:

```bash
python main.py
```
