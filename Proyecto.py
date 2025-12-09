import pygame
import math
import random

# Importar los menús desde archivos separados
from main_menu import MainMenu
from settings import SettingsMenu

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

COLOR_HIT = (255, 80, 80)
BACKGROUND_COLOR = (20, 20, 20)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run & Gun Vehicular")
icon = pygame.image.load("image/car.png")
pygame.display.set_icon(icon)
background_image = pygame.image.load("image/spotlight.png").convert() 
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) #Fondo adaptado al tamaño exacto de pantalla
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
            continue
        x = col * (FRAME_WIDTH + MARGIN)
        y = row * (FRAME_HEIGHT + MARGIN)
        frame_rect = pygame.Rect(x, y, FRAME_WIDTH, FRAME_HEIGHT)
        frame_image = SPRITE_SHEET_IMAGE.subsurface(frame_rect).copy()
        CAR_ANIMATION_FRAMES.append(frame_image)

# --- Carga del sprite sheet de la torreta 24 posiciones ---
try:
    TURRET_SPRITESHEET = pygame.image.load('image/turret_24.png').convert_alpha()
except pygame.error as e:
    print(f"Advertencia: No se pudo cargar 'image/turret_24.png'. Usando superficie de respaldo. Error: {e}")
    TURRET_SPRITESHEET = pygame.Surface((512, 192), pygame.SRCALPHA)
    TURRET_SPRITESHEET.fill((0, 0, 0, 0))  # Transparente

sheet_width = TURRET_SPRITESHEET.get_width()
sheet_height = TURRET_SPRITESHEET.get_height()

TURRET_COLS = 8
TURRET_ROWS = 3

TURRET_FRAME_WIDTH = sheet_width // TURRET_COLS
TURRET_FRAME_HEIGHT = sheet_height // TURRET_ROWS

TURRET_FRAMES = []
for row in range(TURRET_ROWS):
    for col in range(TURRET_COLS):
        x = col * TURRET_FRAME_WIDTH
        y = row * TURRET_FRAME_HEIGHT
        frame_rect = pygame.Rect(x, y, TURRET_FRAME_WIDTH, TURRET_FRAME_HEIGHT)
        frame_image = TURRET_SPRITESHEET.subsurface(frame_rect).copy()
        TURRET_FRAMES.append(frame_image)

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
        
        self.max_hp = 4
        self.hp = self.max_hp


    def update(self, keys):
        global current_controls
        
        self.vel_x = 0
        if keys[current_controls['Moverse a la izquierda']]:
            self.vel_x = -self.speed
        if keys[current_controls['Moverse a la derecha']]:
            self.vel_x = self.speed

        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        now = pygame.time.get_ticks()
        if self.vel_x != 0 and now - self.last_frame_update > self.animation_speed * 1000:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame_index]
            self.last_frame_update = now
        elif self.vel_x == 0:
            self.current_frame_index = 0
            self.image = self.animation_frames[self.current_frame_index]
            
    #Funcion para restar vida
    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            return True  #El vehiculo se destrozo
        return False


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, max_hp):
        super().__init__()
        self.max_hp = max_hp
        self.hp = max_hp

        # Dimensiones de la barra
        self.width = 120
        self.height = 25

        # Colores según la vida
        self.colors = [
            (0, 255, 0),    # Verde → 4 vidas
            (255, 165, 0),  # Naranja → 3 vidas
            (255, 255, 0),  # Amarillo → 2 vidas
            (255, 0, 0)     # Rojo → 1 vida
        ]
        #Luego de la ultima vida, al perder todas se va a la pantalla de game over

        # Imagen inicial
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.update(self.hp)

    def update(self, hp):
        self.hp = hp

        #Limitar valores
        if self.hp < 0:
            self.hp = 0
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        #Calcular cuanta vida tiene el vehiculo
        ratio = self.hp / self.max_hp

        #color según la vida (se crean sprites en el mismo programa) 
        if ratio > 0.75:
            color = self.colors[0]  # verde
        elif ratio > 0.5:
            color = self.colors[1]  # naranja
        elif ratio > 0.25:
            color = self.colors[2]  # amarillo
        else:
            color = self.colors[3]  # rojo

        # Dibujar barra
        self.image.fill((0, 0, 0, 0))  # limpiar transparente
        pygame.draw.rect(self.image, (50, 50, 50), (0, 0, self.width, self.height), border_radius=5)  # fondo gris
        pygame.draw.rect(self.image, color, (0, 0, int(self.width * ratio), self.height), border_radius=5)  # vida
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, self.width, self.height), 2, border_radius=5)  # borde blanco



def game_over_screen():
    """Pantalla de Game Over"""
    font = pygame.font.SysFont(None, 80)
    text = font.render("GAME OVER", True, (255, 0, 0))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    screen.fill((0, 0, 0))
    screen.blit(text, rect)
    pygame.display.flip()

    # Esperar unos segundos antes de salir
    pygame.time.delay(3000)
    return


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

        self.cooldown = 250  #Milisegundos de cooldown por disparo 
        self.last_shot = 0


    def update(self, mouse_pos):
        fixed_center = (self.vehicle.rect.centerx, self.vehicle.rect.top - 10)

        dx, dy = mouse_pos[0] - fixed_center[0], mouse_pos[1] - fixed_center[1]
        angle = math.degrees(math.atan2(-dy, dx)) % 360 if (dx or dy) else 0

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
        # 🔵 Círculo amarillo con borde
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (6, 6), 6)
        pygame.draw.circle(self.image, (255, 200, 0), (6, 6), 6, 2)
        self.rect = self.image.get_rect(center=(x, y))

        dx, dy = mouse_pos[0] - x, mouse_pos[1] - y
        ang = math.atan2(dy, dx)

        self.speed = 14
        self.vel_x = math.cos(ang) * self.speed
        self.vel_y = math.sin(ang) * self.speed

        self.lifetime = 2000  # ms
        self.spawn_time = pygame.time.get_ticks()

        group.add(self)
        

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        if not screen.get_rect().colliderect(self.rect):
            self.kill()

#hacer el efecto para cuando el enemigo recibe daño
def lerp_color(c1, c2, t):
    """Interpolación lineal entre dos colores (c1 → c2) según factor t [0..1]."""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.hp = 3
        self.speed = 2
        self.direction = 1

      #Visualizador de daño
        self.is_hit = False
        self.hit_duration = 350  #Duracion del efecto de daño
        self.hit_time = 0

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.left < 100 or self.rect.right > WIDTH - 100:
            self.direction *= -1
            if self.rect.left < 100:
                self.rect.left = 100
            if self.rect.right > WIDTH - 100:
                self.rect.right = WIDTH - 100
                
        if self.is_hit:
            elapsed = pygame.time.get_ticks() - self.hit_time
            if elapsed < self.hit_duration:
                t = elapsed / self.hit_duration
                new_color = lerp_color(COLOR_HIT, GRAY, t)
                self.image.fill(new_color)
            else:
                self.image.fill(GRAY)
                self.is_hit = False




    def take_damage(self):
        self.hp -= 1
    
        self.is_hit = True
        self.hit_time = pygame.time.get_ticks()
        self.image.fill(COLOR_HIT)


        if self.hp <= 0:
            self.kill()

def run_game(current_controls):
    running = True

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    vehicle = Vehicle(WIDTH//2, HEIGHT- 20)
    all_sprites.add(vehicle)

    turret = Turret(vehicle, bullets, all_sprites)
    all_sprites.add(turret)

    health_bar = HealthBar(10, 10, vehicle.max_hp)
    all_sprites.add(health_bar)
    health_bar.update(vehicle.hp)


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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = SettingsMenu(screen, current_controls)
                    updated_controls = menu.run()
                    if updated_controls:
                        current_controls.update(updated_controls)

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
        health_bar.update(vehicle.hp)
        
    
        
        #Colisión entre vehículo y enemigos
        collisions = pygame.sprite.spritecollide(vehicle, enemies, False)
        for enemy in collisions:
            if vehicle.take_damage(): #generacion de la pantalla de game over
                game_over_screen() 
                running = False   #Romper el bucle para regresar al main
                break
                health_bar.update(vehicle.hp)#Conectar la barra con la vida actual del vehiculo


            
            # Calcular dirección de retroceso
            # si el enemigo choca de un lado,el vehiculo retrocede en direccion opuesta,y viceversa
            if vehicle.rect.centerx < enemy.rect.centerx:
                vehicle.rect.x -= 45
                enemy.rect.x += 45
            else:
                vehicle.rect.x += 45
                enemy.rect.x -= 45

            # Evitar que se salgan de la pantalla
            if vehicle.rect.left < 0:
                vehicle.rect.left = 0
            if vehicle.rect.right > WIDTH:
                vehicle.rect.right = WIDTH
            if enemy.rect.left < 100:
                enemy.rect.left = 100
            if enemy.rect.right > WIDTH - 100:
                enemy.rect.right = WIDTH - 100        
        

        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for bullet_hit, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)
        
        pygame.display.flip()


def main():
    global current_controls
    current_controls = {
        'Moverse a la izquierda': pygame.K_a,
        'Moverse a la derecha': pygame.K_d,
        'Disparo': pygame.K_SPACE,
    }

    menu = MainMenu(screen)
    while True:
        choice = menu.run()
        if choice == "salir":
            break
        elif choice == "ajustes":
            settings_menu = SettingsMenu(screen, current_controls)
            updated_controls = settings_menu.run()
            if updated_controls:
                current_controls.update(updated_controls)
        elif choice == "jugar":
            run_game(current_controls)

    pygame.quit()

if __name__ == "__main__":
    main()