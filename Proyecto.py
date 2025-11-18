import pygame
import sys
import os
import json

# ------------------- INICIALIZACIÓN -------------------
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# ------------------- CONFIGURACIÓN -------------------
CONFIG_FILE = "config.json"
default_config = {
    "controls": {"left": "a", "right": "d", "jump": "space"},
    "screen_size": [900, 600]
}

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump(default_config, f, indent=4)
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# ------------------- COLORES -------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY_DARK = (40, 40, 40)
GRAY_METAL = (80, 80, 80)
YELLOW_LIGHT = (255, 230, 120)

# ------------------- FUENTES -------------------
title_font = pygame.font.SysFont("impact", 90)
font = pygame.font.SysFont("impact", 36)
small_font = pygame.font.SysFont("impact", 24)

# ------------------- ESTADOS -------------------
MENU = "menu"
SETTINGS = "settings"
CONTROLS_SETTINGS = "controls_settings"
SIZE_SETTINGS = "size_settings"
GAME = "game"
state = MENU

clock = pygame.time.Clock()

# ------------------- SPRITE SHEET CONFIG -------------------
SPRITE_W = 256
SPRITE_H = 192

def load_auto_frames(sheet):
    frames = []
    rows = 4
    cols = 3
    for row in range(rows):
        for col in range(cols):
            x = col * SPRITE_W
            y = row * SPRITE_H
            frame = sheet.subsurface((x, y, SPRITE_W, SPRITE_H))
            frames.append(frame)
    return frames

# ------------------- BOTONES -------------------
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 260, 60)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, (120,120,120), self.rect, border_radius=8)
        else:
            pygame.draw.rect(screen, (90,90,90), self.rect, border_radius=8)

        pygame.draw.rect(screen, (255,255,255), self.rect, 4, border_radius=8)
        label = font.render(self.text, True, WHITE)
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

button_start = Button("LAUNCH", 600, 200)
button_settings = Button("SETTINGS", 600, 290)
button_exit = Button("EXIT", 600, 380)

# ------------------- FONDO HANGAR -------------------
def draw_hangar(screen):
    screen.fill(GRAY_DARK)

    # Paneles
    for x in range(0, 900, 140):
        pygame.draw.rect(screen, (60, 60, 60), (x, 0, 120, 600))

    # Piso
    for y in range(360, 600, 20):
        pygame.draw.line(screen, (90, 90, 90), (0, y), (900, y), 2)

    pygame.draw.rect(screen, (20,20,20), (0,0,900,25))

# ------------------- LUZ ANIMADA -------------------
def draw_light(screen, t):
    lx = 200 + (pygame.math.sin(t * 2) * 120)
    light = pygame.Surface((400,130), pygame.SRCALPHA)
    pygame.draw.ellipse(light, (255,255,200,110), (0,0,400,130))
    screen.blit(light, (lx, 20))

# ------------------- MENÚ PRINCIPAL -------------------
def run_menu():
    global state

    # Crear ventana ANTES de cargar imágenes
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Car and Gun - Main Menu")

    # Cargar sprites AHORA sí funciona
    sprite_sheet = pygame.image.load("SpriteAuto.png").convert_alpha()
    auto_frames = load_auto_frames(sprite_sheet)

    auto_frame_index = 0
    auto_frame_time = 0

    running = True
    t = 0

    while running and state == MENU:
        dt = clock.tick(60) / 1000
        t += dt

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if button_start.clicked(event):
                state = GAME
            if button_settings.clicked(event):
                state = SETTINGS
            if button_exit.clicked(event):
                pygame.quit()
                sys.exit()

        # Fondo
        draw_hangar(screen)
        draw_light(screen, t)

        # Título
        title = title_font.render("CAR AND GUN", True, YELLOW_LIGHT)
        screen.blit(title, (60, 40))

        # Animación auto
        auto_frame_time += dt
        if auto_frame_time >= 0.10:
            auto_frame_index = (auto_frame_index + 1) % len(auto_frames)
            auto_frame_time = 0

        auto_img = auto_frames[auto_frame_index]
        screen.blit(auto_img, (150, 260))

        # Botones
        button_start.draw(screen)
        button_settings.draw(screen)
        button_exit.draw(screen)

        pygame.display.flip()

# ------------------- MENÚ PRINCIPAL (ESTILO METAL SLUG) -------------------
def run_menu():
    global state

    # Crear ventana ANTES de cargar imágenes
    screen = pygame.display.set_mode((900, 600))
    pygame.display.set_caption("Car and Gun - Main Menu")

    # Cargar sprite sheet correctamente
    sprite_sheet = pygame.image.load("SpriteAuto.png").convert_alpha()
    auto_frames = load_auto_frames(sprite_sheet)

    # variables de animación locales
    auto_frame_index = 0
    auto_frame_time = 0.0

    t = 0.0
    running = True

    while running and state == MENU:
        dt = clock.tick(60) / 1000.0
        t += dt

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if button_start.clicked(event):
                state = GAME
            if button_settings.clicked(event):
                state = SETTINGS
            if button_exit.clicked(event):
                pygame.quit()
                sys.exit()

        # FONDO
        draw_hangar(screen)
        draw_light(screen, t)

        # TÍTULO
        title = title_font.render("CAR AND GUN", True, YELLOW_LIGHT)
        screen.blit(title, (60, 40))

        # ANIMACIÓN AUTO (actualiza índice)
        auto_frame_time += dt
        if auto_frame_time >= 0.10:
            auto_frame_index = (auto_frame_index + 1) % len(auto_frames)
            auto_frame_time = 0.0

        auto_img = auto_frames[auto_frame_index]
        screen.blit(auto_img, (150, 260))

        # BOTONES
        button_start.draw(screen)
        button_settings.draw(screen)
        button_exit.draw(screen)

        pygame.display.flip()


# ------------------- TU JUEGO ORIGINAL (sin cambios) -------------------
def run_game():
    global state
    screen_size = tuple(config["screen_size"])
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Juego iniciado")

    sprite_size = 40
    sprite = pygame.Surface((sprite_size, sprite_size))
    sprite.fill((255, 0, 0))

    sprite_x = screen_size[0] // 2 - sprite_size // 2
    floor_y = screen_size[1] - 50
    sprite_y = floor_y - sprite_size

    gravity = 0.5
    jump_strength = -10
    vertical_velocity = 0
    speed = 4
    is_on_ground = False

    key_map = {
        "left": pygame.key.key_code(config['controls']['left']),
        "right": pygame.key.key_code(config['controls']['right']),
        "jump": pygame.key.key_code(config['controls']['jump'])
    }

    running_game = True
    while running_game and state == GAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
                state = MENU

        keys = pygame.key.get_pressed()
        if keys[key_map["left"]]:
            sprite_x -= speed
        if keys[key_map["right"]]:
            sprite_x += speed
        if keys[key_map["jump"]] and is_on_ground:
            vertical_velocity = jump_strength
            is_on_ground = False

        vertical_velocity += gravity
        sprite_y += vertical_velocity

        if sprite_y >= floor_y - sprite_size:
            sprite_y = floor_y - sprite_size
            vertical_velocity = 0
            is_on_ground = True

        sprite_x = max(0, min(sprite_x, screen_size[0] - sprite_size))

        screen.fill(WHITE)
        pygame.draw.rect(screen, (0,255,0), (0, floor_y, screen_size[0], 50))
        screen.blit(sprite, (sprite_x, sprite_y))

        info = small_font.render(f"Controles: {config['controls']}", True, BLACK)
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# ------------------- AJUSTES (sin cambios) -------------------
def run_settings():
    global state
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ajustes")

    controls_btn = pygame.Rect(50, 60, 300, 40)
    size_btn = pygame.Rect(50, 130, 300, 40)
    back_btn = pygame.Rect(130, 250, 140, 40)

    running_settings = True
    while running_settings and state == SETTINGS:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        draw_button(screen, "Volver al Menú", back_btn, mouse_pos)
        draw_button(screen, "Configurar Controles", controls_btn, mouse_pos)
        draw_button(screen, "Cambiar Tamaño de Pantalla", size_btn, mouse_pos)

        text1 = small_font.render(f"Controles: {config['controls']}", True, BLACK)
        text2 = small_font.render(f"Tamaño: {config['screen_size']}", True, BLACK)
        screen.blit(text1, (50, 200))
        screen.blit(text2, (50, 230))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = MENU
                running_settings = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    state = MENU
                    running_settings = False
                elif controls_btn.collidepoint(event.pos):
                    state = CONTROLS_SETTINGS
                    running_settings = False
                elif size_btn.collidepoint(event.pos):
                    state = SIZE_SETTINGS
                    running_settings = False

        pygame.display.flip()
        clock.tick(30)

def draw_button(screen, text, rect, mouse_pos, color_active=GRAY_METAL, color_hover=GRAY_DARK):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, color_hover, rect)
    else:
        pygame.draw.rect(screen, color_active, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))

# ------------------- CONTROL SETTINGS & SIZE SETTINGS SIGUEN IGUAL -------------------
def run_controls_settings():
    global state
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ajustes de Controles")

    left_btn = pygame.Rect(100, 50, 200, 40)
    right_btn = pygame.Rect(100, 110, 200, 40)
    jump_btn = pygame.Rect(100, 170, 200, 40)
    back_btn = pygame.Rect(130, 250, 140, 40)

    waiting_key = None
    running_controls = True

    while running_controls and state == CONTROLS_SETTINGS:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        draw_button(screen, "Volver", back_btn, mouse_pos)

        draw_button(screen, f"Izquierda: {config['controls']['left']}", left_btn, mouse_pos)
        draw_button(screen, f"Derecha: {config['controls']['right']}", right_btn, mouse_pos)
        draw_button(screen, f"Saltar: {config['controls']['jump']}", jump_btn, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = MENU
                running_controls = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    save_config()
                    state = SETTINGS
                    running_controls = False
                elif left_btn.collidepoint(event.pos):
                    waiting_key = "left"
                elif right_btn.collidepoint(event.pos):
                    waiting_key = "right"
                elif jump_btn.collidepoint(event.pos):
                    waiting_key = "jump"
            if event.type == pygame.KEYDOWN and waiting_key:
                key_name = pygame.key.name(event.key)
                config["controls"][waiting_key] = key_name
                waiting_key = None
                save_config()

        if waiting_key:
            label = small_font.render(f"Presiona nueva tecla para {waiting_key}", True, (255,0,0))
            screen.blit(label, (50, 20))

        pygame.display.flip()
        clock.tick(30)

def run_size_settings():
    global state
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ajustes de Pantalla")

    predefined_sizes = [(600,400), (800,600), (1024,768)]
    back_btn = pygame.Rect(130, 250, 140, 40)
    btns = [pygame.Rect(100, 50+i*60, 200, 40) for i in range(3)]

    running_size = True
    while running_size and state == SIZE_SETTINGS:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        draw_button(screen, "Volver", back_btn, mouse_pos)

        for i, btn in enumerate(btns):
            draw_button(screen, f"{predefined_sizes[i][0]}x{predefined_sizes[i][1]}", btn, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = MENU
                running_size = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    state = SETTINGS
                    running_size = False
                for i, btn in enumerate(btns):
                    if btn.collidepoint(event.pos):
                        config["screen_size"] = list(predefined_sizes[i])
                        save_config()

        pygame.display.flip()
        clock.tick(30)

# ------------------- BUCLE PRINCIPAL -------------------
while True:
    if state == MENU:
        run_menu()
    elif state == SETTINGS:
        run_settings()
    elif state == CONTROLS_SETTINGS:
        run_controls_settings()
    elif state == SIZE_SETTINGS:
        run_size_settings()
    elif state == GAME:
        run_game()
