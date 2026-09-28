import sys
import math
import os
import pygame

# -----------------------------------------------------------------------------
# CONFIGURAÇÕES GERAIS E CONSTANTES
# -----------------------------------------------------------------------------
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Cores (RGB)
COLOR_BG_GRASS = (76, 153, 0)
COLOR_UI_BG = (30, 30, 30, 220)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (241, 196, 15)
COLOR_GREEN = (46, 204, 113)
COLOR_DARK_GREEN = (34, 112, 62)
COLOR_GRAY = (180, 180, 180)


# -----------------------------------------------------------------------------
# CLASSE: ANIMAL
# -----------------------------------------------------------------------------
class Animal(pygame.sprite.Sprite):
    def __init__(self, name, habitat, diet, classification, trivia, x, y, image_filename):
        super().__init__()
        self.name = name
        self.habitat = habitat
        self.diet = diet
        self.classification = classification
        self.trivia = trivia
        
        self.discovered = False
        self.frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150  # Milissegundos por frame

        # Caminho da imagem dentro da pasta assets/
        sprite_path = os.path.join("assets", image_filename)
        self._load_sprite(sprite_path)

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))

    def _load_sprite(self, sprite_path):
        if os.path.exists(sprite_path):
            try:
                sheet = pygame.image.load(sprite_path).convert_alpha()
                height = sheet.get_height()
                width = sheet.get_width()
                
                # Se for um spritesheet horizontal, divide em frames; se for imagem única, usa-a diretamente
                num_frames = max(1, width // height)
                
                for i in range(num_frames):
                    frame_rect = pygame.Rect(i * height, 0, height, height)
                    frame_surf = sheet.subsurface(frame_rect)
                    scaled_frame = pygame.transform.scale(frame_surf, (64, 64))
                    self.frames.append(scaled_frame)
            except Exception as e:
                print(f"Erro ao carregar {sprite_path}: {e}")

        # Se falhar o carregamento, cria um indicador visual (placeholder)
        if not self.frames:
            placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(placeholder, (200, 100, 50), (32, 32), 24)
            self.frames.append(placeholder)

    def update(self, dt):
        if len(self.frames) > 1:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]


# -----------------------------------------------------------------------------
# CLASSE: JOGADOR
# -----------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((52, 152, 219))  # Azul
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # Normalização do movimento diagonal
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071

        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

        # Limite da tela
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


# -----------------------------------------------------------------------------
# CLASSE: SISTEMA DE COLEÇÃO
# -----------------------------------------------------------------------------
class CollectionSystem:
    def __init__(self, total_animals):
        self.total_animals = total_animals
        self.discovered_animals = []

    def discover(self, animal):
        if not animal.discovered:
            animal.discovered = True
            self.discovered_animals.append(animal)
            return True
        return False

    def get_progress_percentage(self):
        if self.total_animals == 0:
            return 0.0
        return (len(self.discovered_animals) / self.total_animals) * 100

    def get_tier_label(self):
        count = len(self.discovered_animals)
        if count >= 5:
            return "Coleção Completa"
        elif count >= 3:
            return "Avanço da Coleção"
        elif count >= 1:
            return "Início da Coleção"
        return "Explorador Novato"


# -----------------------------------------------------------------------------
# CLASSE PRINCIPAL DO JOGO
# -----------------------------------------------------------------------------
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Eden of the Animals")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.SysFont("Arial", 22, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 16)

        # Grupos de Sprites
        self.all_sprites = pygame.sprite.Group()
        self.animals_group = pygame.sprite.Group()

        # Jogador
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.player)

        # Popula os animais
        self._load_animals()
        
        # Sistema de Coleção
        self.collection = CollectionSystem(len(self.animals_group))
        
        # Estados
        self.selected_animal = None
        self.show_book = False

    def _load_animals(self):
        animals_data = [
            {
                "name": "Girafa", "habitat": "Savanas e Bosques Abertos", 
                "diet": "Herbívoro (Folhas de acácia)", "classification": "Mamífero (Artiodactyla)",
                "trivia": "É o animal terrestre mais alto do mundo.",
                "x": 200, "y": 200, "filename": "girafa.png"
            },
            {
                "name": "Leão", "habitat": "Savanas e Pastagens", 
                "diet": "Carnívoro (Grandes mamíferos)", "classification": "Mamífero (Carnivora)",
                "trivia": "Os machos possuem uma juba característica para proteção e exibição.",
                "x": 800, "y": 200, "filename": "leao.png"
            },
            {
                "name": "Guepardo", "habitat": "Savanas e Planícies", 
                "diet": "Carnívoro (Gazelas e lebres)", "classification": "Mamífero (Carnivora)",
                "trivia": "É o animal terrestre mais rápido, atingindo mais de 100 km/h.",
                "x": 200, "y": 600, "filename": "guepardo.png"
            },
            {
                "name": "Zebra", "habitat": "Savanas e Campos Abertos", 
                "diet": "Herbívoro (Gramíneas e arbustos)", "classification": "Mamífero (Perissodactyla)",
                "trivia": "Cada zebra possui um padrão único de listras pretas e brancas.",
                "x": 800, "y": 600, "filename": "zebra.png"
            },
            {
                "name": "Elefante", "habitat": "Savanas, Florestas e Desertos", 
                "diet": "Herbívoro (Ervas, cascas e frutos)", "classification": "Mamífero (Proboscidea)",
                "trivia": "É o maior animal terrestre vivo e possui uma memória excelente.",
                "x": 512, "y": 150, "filename": "elefante.png"
            }
        ]

        for data in animals_data:
            animal = Animal(
                data["name"], data["habitat"], data["diet"],
                data["classification"], data["trivia"],
                data["x"], data["y"], data["filename"]
            )
            self.all_sprites.add(animal)
            self.animals_group.add(animal)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_e:
                    self.interact()
                if event.key == pygame.K_b:
                    self.show_book = not self.show_book
        return True

    def interact(self):
        for animal in self.animals_group:
            dist = math.hypot(self.player.rect.centerx - animal.rect.centerx,
                              self.player.rect.centery - animal.rect.centery)
            if dist <= 70:
                self.collection.discover(animal)
                self.selected_animal = animal
                return

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self):
        self.screen.fill(COLOR_BG_GRASS)
        pygame.draw.rect(self.screen, COLOR_DARK_GREEN, (50, 50, 924, 668), 3)

        self.all_sprites.draw(self.screen)

        for animal in self.animals_group:
            dist = math.hypot(self.player.rect.centerx - animal.rect.centerx,
                              self.player.rect.centery - animal.rect.centery)
            if dist <= 70:
                pygame.draw.rect(self.screen, COLOR_YELLOW, animal.rect.inflate(10, 10), 2)
                txt = self.font_text.render("Pressiona 'E' para examinar", True, COLOR_WHITE)
                self.screen.blit(txt, (animal.rect.x - 30, animal.rect.y - 25))

        self.draw_hud()

        if self.selected_animal:
            self.draw_animal_card(self.selected_animal)

        if self.show_book:
            self.draw_collection_book()

        pygame.display.flip()

    def draw_hud(self):
        bar_bg = pygame.Rect(10, 10, 320, 50)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bar_bg, border_radius=8)

        prog_pct = self.collection.get_progress_percentage()
        tier = self.collection.get_tier_label()
        
        txt_prog = self.font_text.render(f"Coleção: {len(self.collection.discovered_animals)}/{self.collection.total_animals} ({prog_pct:.1f}%)", True, COLOR_WHITE)
        txt_tier = self.font_text.render(f"Status: {tier}", True, COLOR_YELLOW)
        
        self.screen.blit(txt_prog, (20, 15))
        self.screen.blit(txt_tier, (20, 35))

        txt_book = self.font_text.render("[B] Abrir Coleção | WASD: Mover", True, COLOR_WHITE)
        self.screen.blit(txt_book, (SCREEN_WIDTH - txt_book.get_width() - 20, 15))

    def draw_animal_card(self, animal):
        card_rect = pygame.Rect(SCREEN_WIDTH - 360, 80, 340, 250)
        
        surf = pygame.Surface((card_rect.width, card_rect.height), pygame.SRCALPHA)
        surf.fill(COLOR_UI_BG)
        self.screen.blit(surf, card_rect.topleft)
        pygame.draw.rect(self.screen, COLOR_YELLOW, card_rect, 2, border_radius=6)

        y_off = card_rect.y + 15
        x_off = card_rect.x + 15

        title = self.font_title.render(animal.name, True, COLOR_YELLOW)
        self.screen.blit(title, (x_off, y_off))
        y_off += 30

        lines = [
            f"Habitat: {animal.habitat}",
            f"Alimentação: {animal.diet}",
            f"Classificação: {animal.classification}",
            f"Curiosidade: {animal.trivia}"
        ]

        for line in lines:
            words = line.split(' ')
            current_line = ""
            for word in words:
                test_line = current_line + word + " "
                if self.font_text.size(test_line)[0] < 310:
                    current_line = test_line
                else:
                    txt_s = self.font_text.render(current_line, True, COLOR_WHITE)
                    self.screen.blit(txt_s, (x_off, y_off))
                    y_off += 20
                    current_line = word + " "
            if current_line:
                txt_s = self.font_text.render(current_line, True, COLOR_WHITE)
                self.screen.blit(txt_s, (x_off, y_off))
                y_off += 22

    def draw_collection_book(self):
        book_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        
        surf = pygame.Surface((book_rect.width, book_rect.height), pygame.SRCALPHA)
        surf.fill((20, 20, 20, 240))
        self.screen.blit(surf, book_rect.topleft)
        pygame.draw.rect(self.screen, COLOR_GREEN, book_rect, 3, border_radius=10)

        title = self.font_title.render("--- COLEÇÃO DE ANIMAIS DESCOBERTOS ---", True, COLOR_GREEN)
        self.screen.blit(title, (book_rect.x + 80, book_rect.y + 20))

        y_off = book_rect.y + 70
        for animal in self.animals_group:
            status_color = COLOR_WHITE if animal.discovered else COLOR_GRAY
            status_str = f"[DESCOBERTO] {animal.name}" if animal.discovered else f"[???] Desconhecido"
            
            txt = self.font_text.render(status_str, True, status_color)
            self.screen.blit(txt, (book_rect.x + 40, y_off))
            y_off += 35


# -----------------------------------------------------------------------------
# PONTO DE ENTRADA DO PROGRAMA
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.run()