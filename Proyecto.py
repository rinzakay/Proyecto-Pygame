import pygame
import math
import random

# =====================================
#          CONFIGURACIÓN
# =====================================
WIDTH, HEIGHT = 1000, 600
FPS = 60
ENEMY_SPAWN_RATE = 3500  # Milisegundos entre aparición de enemigos

# Colores
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)  # Color de respaldo si la imagen no carga
YELLOW = (255, 220, 0)
RED = (255, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run & Gun Vehicular")
clock = pygame.time.Clock()

# --- Carga de Sprites del Coche ---
try:
    SPRITE_SHEET_IMAGE = pygame.image.load('image/SpriteAuto.png').convert_alpha()
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar 'image/SpriteAuto.png'. Usando color de respaldo. Error: {e}")
    SPRITE_SHEET_IMAGE = pygame.Surface((192, 192), pygame.SRCALPHA)
    SPRITE_SHEET_IMAGE.fill(GREEN)

# Dimensiones y margen entre fotogramas del coche
FRAME_WIDTH = 125
FRAME_HEIGHT = 80
MARGIN = 1  # Ajusta si hay espacio entre fotogramas

excluded_frames = [9, 10, 11]  # Índices de fotogramas a excluir

CAR_ANIMATION_FRAMES = []

for row in range(4):
    for col in range(3):
        frame_index = row * 3 + col
        if frame_index in excluded_frames:
            print(f"Excluyendo fotograma {frame_index}")
            continue
        x = col * (FRAME_WIDTH + MARGIN)
        y = row * (FRAME_HEIGHT + MARGIN)
        frame_rect = pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT)
        frame_image = SPRITE_SHEET_IMAGE.subsurface(frame_rect).copy()
        CAR_ANIMATION_FRAMES.append(frame_image)

print(f"Total fotogramas cargados: {len(CAR_ANIMATION_FRAMES)}")

# --- Carga del sprite sheet de la torreta 24 posiciones ---
try:
    TURRET_SPRITESHEET = pygame.image.load('image/turret_24.png').convert_alpha()
    print("TURRET_SPRITESHEET cargado con éxito.")
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar 'image/turret_24.png'. Usando superficie de respaldo. Error: {e}")
    TURRET_SPRITESHEET = pygame.Surface((512, 192), pygame.SRCALPHA)
    TURRET_SPRITESHEET.fill((0, 0, 0, 0))  # Transparente

# Obtener tamaño real de la imagen para evitar errores
sheet_width = TURRET_SPRITESHEET.get_width()
sheet_height = TURRET_SPRITESHEET.get_height()

# Definir filas y columnas
TURRET_COLS = 8
TURRET_ROWS = 3

# Calcular tamaño de cada fotograma
TURRET_FRAME_WIDTH = sheet_width // TURRET_COLS
TURRET_FRAME_HEIGHT = sheet_height // TURRET_ROWS

# Extraer fotogramas
TURRET_FRAMES = []
for row in range(TURRET_ROWS):
    for col in range(TURRET_COLS):
        x = col * TURRET_FRAME_WIDTH
        y = row * TURRET_FRAME_HEIGHT
        frame_rect = pygame.Rect(x, y, TURRET_FRAME_WIDTH, TURRET_FRAME_HEIGHT)
        frame_image = TURRET_SPRITESHEET.subsurface(frame_rect).copy()
        TURRET_FRAMES.append(frame_image)

print(f"Total fotogramas torreta extraídos: {len(TURRET_FRAMES)}")

# Clases del juego

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_frames = CAR_ANIMATION_FRAMES
        self.current_frame_index = 0
        self.image = self.animation_frames[self.current_frame_index]
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.speed = 5
        self.vel_x = 0

        self.animation_speed = 0.1  # segundos por fotograma
        self.last_frame_update = pygame.time.get_ticks()

    def update(self, keys):
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_d]:
            self.vel_x = self.speed

        self.rect.x += self.vel_x

        # Limitar dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Animación solo si se mueve
        now = pygame.time.get_ticks()
        if self.vel_x != 0 and now - self.last_frame_update > self.animation_speed * 1000:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame_index]
            self.last_frame_update = now
        elif self.vel_x == 0:
            self.current_frame_index = 0
            self.image = self.animation_frames[self.current_frame_index]

class Turret(pygame.sprite.Sprite):
    def __init__(self, vehicle, bullets_group, all_sprites_group):
        super().__init__()

        self.frames = TURRET_FRAMES
        self.num_frames = len(self.frames)
        self.vehicle = vehicle
        self.bullets_group = bullets_group
        self.all_sprites_group = all_sprites_group

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=vehicle.rect.center)

        self.cooldown = 250  # ms
        self.last_shot = pygame.time.get_ticks()

    def update(self, mouse_pos):
        print("Actualizando torreta en posición fija")
        fixed_center = (self.vehicle.rect.centerx, self.vehicle.rect.top - 10)

        mx, my = mouse_pos
        dx = mx - fixed_center[0]
        dy = my - fixed_center[1]

        if dx == 0 and dy == 0:
            angle = 0
        else:
            angle = math.degrees(math.atan2(-dy, dx)) % 360

        frame_index = int((angle / 360) * self.num_frames) % self.num_frames

        self.image = self.frames[frame_index]
        self.rect = self.image.get_rect(center=fixed_center)
        
    def shoot(self, mouse_pos):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.centery, mouse_pos, self.bullets_group)
            self.all_sprites_group.add(bullet)
            self.last_shot = now

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_pos, group):
        super().__init__()
        self.image = pygame.Surface((8, 8), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))

        mx, my = mouse_pos
        dx = mx - x
        dy = my - y
        ang = math.atan2(dy, dx)

        self.speed = 14
        self.vel_x = math.cos(ang) * self.speed
        self.vel_y = math.sin(ang) * self.speed

        group.add(self)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if not screen.get_rect().colliderect(self.rect):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.hp = 3
        self.speed = 2
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.left < 100 or self.rect.right > WIDTH - 100:
            self.direction *= -1
            if self.rect.left < 100:
                self.rect.left = 100
            if self.rect.right > WIDTH - 100:
                self.rect.right = WIDTH - 100

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()

def main():
    running = True

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    vehicle = Vehicle(WIDTH // 4, HEIGHT - 20)
    all_sprites.add(vehicle)

    turret = Turret(vehicle, bullets, all_sprites)
    all_sprites.add(turret)

    enemy1 = Enemy(WIDTH - 100, HEIGHT - 20)
    enemies.add(enemy1)
    all_sprites.add(enemy1)

    last_enemy_spawn = pygame.time.get_ticks()

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    turret.shoot(pygame.mouse.get_pos())

        now = pygame.time.get_ticks()
        if now - last_enemy_spawn >= ENEMY_SPAWN_RATE:
            side = random.choice(["left", "right"])
            if side == "left":
                spawn_x = random.randint(0, WIDTH // 4)
            else:
                spawn_x = random.randint(WIDTH * 3 // 4, WIDTH)

            new_enemy = Enemy(spawn_x, HEIGHT - 20)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

            last_enemy_spawn = now

        keys = pygame.key.get_pressed()

        vehicle.update(keys)
        turret.update(pygame.mouse.get_pos())
        bullets.update()
        enemies.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet_hit, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage()

        screen.fill(BACKGROUND_COLOR)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
