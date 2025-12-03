import pygame
import math
import sys

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 50)

        self.options = ["Jugar", "Ajustes", "Salir"]
        self.selected_option = 0
        self.running = True
        self.menu_start_y = 290
        
        
        #Inicializar los sonidos
        pygame.mixer.init()

        #Música del menu
        try:
            pygame.mixer.music.load("Sound/MUSIC_Menu.mp3")
            pygame.mixer.music.set_volume(0.5)  #Configurar volumen de 0.1 hasta 1.0
            pygame.mixer.music.play(-1)  #loopearlo 
        except pygame.error:
            print("No se pudo cargar la música de fondo.")

        #sonidos al seleccionar
        try:
            self.buttonSound = pygame.mixer.Sound("Sound/SFX_Button.mp3")
        except pygame.error:
            self.buttonSound = None

        try:
            self.background = pygame.image.load("image/Menu_BKG.jpg").convert()
            self.background = pygame.transform.scale(self.background, self.screen.get_size())
        except pygame.error:
            self.background = None


        try:
            self.background = pygame.image.load("image/Menu_BKG.jpg").convert()
            self.background = pygame.transform.scale(self.background, self.screen.get_size())
        except pygame.error:
            self.background = None



    def render_text(self, text, color, x, y):
        shadow = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x+2, y+2))
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def get_pulse_color(self, base_color, time):
        factor = (math.sin(time/200) + 1) / 2
        r = int(base_color[0] * factor + 255 * (1-factor))
        g = int(base_color[1] * factor + 255 * (1-factor))
        b = int(base_color[2] * factor + 255 * (1-factor))
        return (r, g, b)

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        try:
            logo = pygame.image.load("image/title.png")
            logo = pygame.transform.scale_by(logo, 0.25)
            logo_x = self.screen.get_width() // 2 - logo.get_width() // 2
            logo_y = 60
            self.screen.blit(logo, (logo_x, logo_y))
        except pygame.error:
            title = self.font.render("Car And Gun", True, (255, 255, 255))
            self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 100))

        time = pygame.time.get_ticks()
        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, (255, 255, 255))
            x = self.screen.get_width()//2 - text_surface.get_width()//2
            y = self.menu_start_y + i*60

            if i == self.selected_option:
                pygame.draw.rect(self.screen, (50, 50, 150),
                                 (x-20, y-10, text_surface.get_width()+40, text_surface.get_height()+20),
                                 border_radius=10)
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)

            self.render_text(option, color, x, y)

        pygame.display.flip()

    def countdown_exit(self):
        """Muestra una cuenta regresiva antes de cerrar el juego"""
        for i in range(3, 0, -1):  # 3, 2, 1
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((0, 0, 0))

            text = self.font.render(f"Saliendo en {i}...", True, (255, 0, 0))
            x = self.screen.get_width()//2 - text.get_width()//2
            y = self.screen.get_height()//2 - text.get_height()//2
            self.screen.blit(text, (x, y))

            pygame.display.flip()
            pygame.time.delay(1000)  # espera 1 segundo

        pygame.quit()
        sys.exit()

    def run(self):
        self.running = True
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        choice = self.options[self.selected_option].lower()
                        if choice == "salir":
                            self.countdown_exit()
                        else:
                            return choice
