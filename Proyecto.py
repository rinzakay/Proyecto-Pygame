# Proyecto final corregido - menú estilo "Metal Slug" (encuadre 600x400 a la izquierda, UI a la derecha)
import pygame
import sys
import os
import json
import math

# -------------------- CONFIG INICIAL --------------------
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

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

# -------------------- CONSTANTES --------------------
ENC_W, ENC_H = 600, 400   # encuadre (left art area)
WIDTH, HEIGHT = config.get("screen_size", [900, 600])
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY_DARK = (40,40,40)
GRAY_METAL = (80,80,80)
YELLOW = (255,230,120)

font = pygame.font.SysFont("impact", 32)
small_font = pygame.font.SysFont("impact", 20)
title_font = pygame.font.SysFont("impact", 64)

# -------------------- ESTADOS --------------------
MENU = "menu"
SETTINGS = "settings"
CONTROLS_SETTINGS = "controls_settings"
SIZE_SETTINGS = "size_settings"
GAME = "game"
state = MENU
clock = pygame.time.Clock()

# -------------------- BOTÓN SIMPLE --------------------
class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = pygame.Rect(rect)
    def draw(self, surf):
        m = pygame.mouse.get_pos()
        if self.rect.collidepoint(m):
            pygame.draw.rect(surf, (140,140,140), self.rect, border_radius=6)
        else:
            pygame.draw.rect(surf, GRAY_METAL, self.rect, border_radius=6)
        pygame.draw.rect(surf, WHITE, self.rect, 3, border_radius=6)
        lab = font.render(self.text, True, WHITE)
        surf.blit(lab, lab.get_rect(center=self.rect.center))
    def clicked(self, event):
        return event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and self.rect.collidepoint(event.pos)

# -------------------- UTIL HELPERS --------------------
def load_scaled_image(path, size, colorkey_alpha=True):
    try:
        img = pygame.image.load(path)
        img = pygame.transform.smoothscale(img, size)
        if colorkey_alpha:
            return img.convert_alpha()
        return img.convert()
    except Exception:
        s = pygame.Surface(size)
        s.fill(GRAY_DARK)
        return s

# -------------------- MENÚ PRINCIPAL --------------------
def run_menu():
    global state, WIDTH, HEIGHT
    # ensure window size from config
    WIDTH, HEIGHT = config.get("screen_size", [900,600])
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car and Gun - Menu")

    # encuadre pos (left area)
    enc_x = 40
    enc_y = (HEIGHT - ENC_H) // 2

    # cargar assets del encuadre (fondo y title)
    background = load_scaled_image("fondo.png", (ENC_W, ENC_H))
    title_img = None
    try:
        tmp = pygame.image.load("title.png")
        # scale title to fit inside encuadre width with margin
        max_w = ENC_W - 40
        if tmp.get_width() > max_w:
            new_h = int(max_w * tmp.get_height() / tmp.get_width())
            title_img = pygame.transform.smoothscale(tmp, (max_w, new_h)).convert_alpha()
        else:
            title_img = tmp.convert_alpha()
    except Exception:
        title_img = title_font.render("CAR AND GUN", True, YELLOW)

    # botones UI (right column)
    btn_w, btn_h = 220, 56
    right_x = enc_x + ENC_W + 40
    start_y = enc_y + 100
    btn_gap = 24
    b_start = Button("LAUNCH", (right_x, start_y, btn_w, btn_h))
    b_settings = Button("SETTINGS", (right_x, start_y + (btn_h+btn_gap), btn_w, btn_h))
    b_exit = Button("EXIT", (right_x, start_y + 2*(btn_h+btn_gap), btn_w, btn_h))

    running = True
    while running and state == MENU:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if b_start.clicked(event):
                state = GAME
            if b_settings.clicked(event):
                state = SETTINGS
            if b_exit.clicked(event):
                pygame.quit(); sys.exit()

        # Draw full background (dark)
        screen.fill(BLACK)
        # Draw encuadre (left) and title inside it
        screen.blit(background, (enc_x, enc_y))
        # title centered near top of encuadre
        trect = title_img.get_rect(center=(enc_x + ENC_W//2, enc_y + 48))
        screen.blit(title_img, trect)

        # ground / floor inside encuadre bottom (visual)
        floor_y = enc_y + ENC_H - 40
        pygame.draw.rect(screen, (30,30,30), (enc_x, floor_y, ENC_W, 40))
        # subtle metallic stripes on floor
        for x in range(enc_x, enc_x+ENC_W, 40):
            pygame.draw.line(screen, (50,50,50), (x, floor_y), (x, floor_y+40), 1)

        # Draw buttons on right
        b_start.draw(screen); b_settings.draw(screen); b_exit.draw(screen)

        pygame.display.flip()

# -------------------- AJUSTES --------------------
def run_settings():
    global state, WIDTH, HEIGHT
    WIDTH, HEIGHT = config.get("screen_size", [900,600])
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Settings")

    # buttons inside main window (right side)
    enc_x = 40
    enc_y = (HEIGHT - ENC_H) // 2
    right_x = enc_x + ENC_W + 40
    btn_w, btn_h = 220, 56
    y0 = enc_y + 80
    b_controls = Button("CONTROLS", (right_x, y0, btn_w, btn_h))
    b_size = Button("RESOLUTION", (right_x, y0+80, btn_w, btn_h))
    b_back = Button("BACK", (right_x, y0+160, btn_w, btn_h))

    while state == SETTINGS:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if b_controls.clicked(event):
                state = CONTROLS_SETTINGS
            if b_size.clicked(event):
                state = SIZE_SETTINGS
            if b_back.clicked(event):
                state = MENU

        screen.fill(BLACK)
        # draw encuadre left as reference so layout stays consistent
        bg = load_scaled_image("fondo.png", (ENC_W, ENC_H))
        screen.blit(bg, (enc_x, enc_y))
        # header
        screen.blit(title_font.render("SETTINGS", True, YELLOW), (right_x, enc_y))

        b_controls.draw(screen); b_size.draw(screen); b_back.draw(screen)
        pygame.display.flip(); clock.tick(60)

# -------------------- CONTROLES --------------------
def run_controls_settings():
    global state
    WIDTH, HEIGHT = config.get("screen_size", [900,600])
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Controls")

    enc_x = 40
    enc_y = (HEIGHT - ENC_H) // 2
    back = Button("BACK", (enc_x+ENC_W+40, enc_y+220, 220, 56))

    waiting = None
    msg = ""
    while state == CONTROLS_SETTINGS:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if back.clicked(event):
                    save_config(); state = SETTINGS

        screen.fill(BLACK)
        screen.blit(load_scaled_image("fondo.png", (ENC_W, ENC_H)), (enc_x, enc_y))
        lbl = small_font.render("Edit controls in config.json", True, WHITE)
        screen.blit(lbl, (enc_x+ENC_W+40, enc_y+40))
        back.draw(screen)
        pygame.display.flip(); clock.tick(60)


def run_size_settings():
    global state
    WIDTH, HEIGHT = config.get("screen_size", [900,600])
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Resolution")

    enc_x = 40
    enc_y = (HEIGHT - ENC_H) // 2
    right_x = enc_x + ENC_W + 40
    opts = [((right_x, enc_y+40+i*70, 220, 56), label) for i,label in enumerate(["900x600","1280x720","1600x900"])]
    buttons = [Button(l, r) for r,l in opts]
    back = Button("BACK", (right_x, enc_y+240, 220, 56))

    while state == SIZE_SETTINGS:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            for i,(rect,label) in enumerate(opts):
                btn = Button(label, rect)
                if btn.clicked(event):
                    size = list(map(int,label.split('x')))
                    config["screen_size"] = size
                    save_config()
                   
                    WIDTH, HEIGHT = size
                    state = MENU
            if back.clicked(event):
                state = SETTINGS

        screen.fill(BLACK)
        screen.blit(load_scaled_image("fondo.png", (ENC_W, ENC_H)), (enc_x, enc_y))
        for r,l in opts:
            pygame.draw.rect(screen, GRAY_METAL, r, border_radius=6)
            screen.blit(font.render(l, True, WHITE), pygame.Rect(r).move(30,12))
        back.draw(screen)
        pygame.display.flip(); clock.tick(60)

# -------------------- JUEGO --------------------
def run_game():
    global state
    WIDTH, HEIGHT = config.get("screen_size", [900,600])
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

 
    player = pygame.Rect(100, 0, 36, 36)
    enc_x = 40
    enc_y = (HEIGHT - ENC_H) // 2
    floor_y = enc_y + ENC_H - 40
    player.bottom = floor_y

    vel_y = 0
    gravity = 0.6
    speed_x = 3

    running = True
    while running and state == GAME:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                state = MENU

        keys = pygame.key.get_pressed()
        if keys[pygame.key.key_code(config['controls']['left'])]: player.x -= speed_x
        if keys[pygame.key.key_code(config['controls']['right'])]: player.x += speed_x
        if keys[pygame.key.key_code(config['controls']['jump'])] and player.bottom>=floor_y:
            vel_y = -10

        vel_y += gravity
        player.y += vel_y
        if player.bottom >= floor_y:
            player.bottom = floor_y
            vel_y = 0

        # clamp inside encuadre
        if player.left < enc_x + 8: player.left = enc_x + 8
        if player.right > enc_x + ENC_W - 8: player.right = enc_x + ENC_W - 8

        # draw
        screen.fill(BLACK)
        # encuadre background
        screen.blit(load_scaled_image("fondo.png", (ENC_W, ENC_H)), (enc_x, enc_y))
        # floor
        pygame.draw.rect(screen, (30,30,30), (enc_x, floor_y, ENC_W, 40))
        # player
        pygame.draw.rect(screen, (200,30,30), player)

        pygame.display.flip(); clock.tick(60)

# -------------------- BUCLE PRINCIPAL --------------------
if __name__ == '__main__':
    # ensure starting state and apply saved size
    state = MENU
    WIDTH, HEIGHT = config.get("screen_size", [900,600])
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
