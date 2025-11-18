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
    "screen_size": [600, 400]
}

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump(default_config, f, indent=4)
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

# ------------------- COLORES Y FUENTES -------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

def draw_button(screen, text, rect, mouse_pos, color_active=GRAY, color_hover=DARK_GRAY):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, color_hover, rect)
    else:
        pygame.draw.rect(screen, color_active, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))

# ------------------- ESTADOS -------------------
MENU = "menu"
SETTINGS = "settings"
CONTROLS_SETTINGS = "controls_settings"
SIZE_SETTINGS = "size_settings"
GAME = "game"
state = MENU

# ------------------- VARIABLES -------------------
clock = pygame.time.Clock()
sprite_size = 40
sprite = pygame.Surface((sprite_size, sprite_size))
sprite.fill(RED)
gravity = 0.5
jump_strength = -10
floor_height = 50

# ------------------- BOTONES -------------------
start_btn = pygame.Rect(60, 50, 180, 40)
settings_btn = pygame.Rect(60, 110, 180, 40)
back_btn = pygame.Rect(130, 250, 140, 40)

# ------------------- TAMAÑOS PREDEFINIDOS -------------------
predefined_sizes = [
    (600, 400),
    (800, 600),
    (1024, 768)
]

# ------------------- FUNCIONES -------------------
def run_game():
    global state
    screen_size = tuple(config["screen_size"])
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Juego iniciado")

    sprite_x = screen_size[0] // 2 - sprite_size // 2
    floor_y = screen_size[1] - floor_height
    sprite_y = floor_y - sprite_size
    vertical_velocity = 0
    speed = 4
    is_on_ground = False

    # CORRECCIÓN: Usar key_code para manejar todas las teclas
    key_map = {
        "left": pygame.key.key_code(config['controls']['left']),
        "right": pygame.key.key_code(config['controls']['right']),
        "jump": pygame.key.key_code(config['controls']['jump'])
    }

    running_game = True
    while running_game:
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
        pygame.draw.rect(screen, GREEN, (0, floor_y, screen_size[0], floor_height))
        screen.blit(sprite, (sprite_x, sprite_y))
        info = small_font.render(f"Controles: {config['controls']}", True, BLACK)
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(60)

def run_controls_settings():
    global state
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ajustes de Controles")

    left_btn = pygame.Rect(100, 50, 200, 40)
    right_btn = pygame.Rect(100, 110, 200, 40)
    jump_btn = pygame.Rect(100, 170, 200, 40)

    waiting_key = None

    running_controls = True
    while running_controls:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        draw_button(screen, "Volver", back_btn, mouse_pos)

        draw_button(screen, f"Izquierda: {config['controls']['left']}", left_btn, mouse_pos)
        draw_button(screen, f"Derecha: {config['controls']['right']}", right_btn, mouse_pos)
        draw_button(screen, f"Saltar: {config['controls']['jump']}", jump_btn, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_controls = False
                state = MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    running_controls = False
                    save_config()
                    state = SETTINGS
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
            msg = f"Presiona nueva tecla para {waiting_key.upper()}"
            label = small_font.render(msg, True, RED)
            screen.blit(label, (50, 20))

        pygame.display.flip()
        clock.tick(30)

def run_size_settings():
    global state
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ajustes de Pantalla")

    running_size = True
    btns = []
    for i, size in enumerate(predefined_sizes):
        btns.append(pygame.Rect(100, 50 + i*60, 200, 40))

    while running_size:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        draw_button(screen, "Volver", back_btn, mouse_pos)

        for i, btn in enumerate(btns):
            draw_button(screen, f"{predefined_sizes[i][0]}x{predefined_sizes[i][1]}", btn, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_size = False
                state = MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    running_size = False
                    state = SETTINGS
                for i, btn in enumerate(btns):
                    if btn.collidepoint(event.pos):
                        config["screen_size"] = list(predefined_sizes[i])
                        save_config()

        pygame.display.flip()
        clock.tick(30)

def run_settings():
    global state
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Ajustes")

    controls_btn = pygame.Rect(50, 60, 300, 40)
    size_btn = pygame.Rect(50, 130, 300, 40)

    running_settings = True
    while running_settings:
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
                running_settings = False
                state = MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    running_settings = False
                    state = MENU
                elif controls_btn.collidepoint(event.pos):
                    running_settings = False
                    state = CONTROLS_SETTINGS
                elif size_btn.collidepoint(event.pos):
                    running_settings = False
                    state = SIZE_SETTINGS

        pygame.display.flip()
        clock.tick(30)

# ------------------- BUCLE PRINCIPAL -------------------
running = True
while running:
    if state == MENU:
        screen = pygame.display.set_mode((300, 200))
        pygame.display.set_caption("Menú Principal")
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(WHITE)
        draw_button(screen, "Iniciar Juego", start_btn, mouse_pos)
        draw_button(screen, "Ajustes", settings_btn, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    state = GAME
                elif settings_btn.collidepoint(event.pos):
                    state = SETTINGS

        pygame.display.flip()
        clock.tick(30)

    elif state == SETTINGS:
        run_settings()
    elif state == CONTROLS_SETTINGS:
        run_controls_settings()
    elif state == SIZE_SETTINGS:
        run_size_settings()
    elif state == GAME:
        run_game()

pygame.quit()
sys.exit()
