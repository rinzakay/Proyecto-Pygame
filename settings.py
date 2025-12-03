from Excepciones_Keys import NO_KEYS
import pygame

#Colores para el menu
COLOR_TEXT = (255, 255, 255)
COLOR_SELECTED = (255, 255, 0)
COLOR_BOX = (50, 50, 150)

COLOR_WAITING = (200, 200, 200)   #Gris
COLOR_SUCCESS = (0, 255, 0)       #Verde
COLOR_ERROR = (255, 0, 0)         #Rojo

class SettingsMenu:
    def __init__(self, screen, current_controls=None):
        self.screen = screen
        if current_controls is None:
            current_controls = {}

        self.controls = current_controls.copy()
        self.font = pygame.font.SysFont(None, 48)

        self.selected_option = 0
        self.options = list(self.controls.keys()) + ['Guardar y salir']
        self.running = False

        #Visuales
        self.waiting_for_key = False
        self.message = ""

        #Cargar imagen de fondo
        self.background = pygame.image.load("image/Options_BKG.jpg")
        self.background = pygame.transform.scale(
            self.background,
            (self.screen.get_width(), self.screen.get_height())
        )

    def render_text(self, text, color, x, y):
        shadow = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x+2, y+2))
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        for i, option in enumerate(self.options):
            if option == 'Guardar y salir':
                text_str = option
            else:
                key_name = pygame.key.name(self.controls[option])
                text_str = f"{option}: {key_name}"

            text_surface = self.font.render(text_str, True, COLOR_TEXT)
            x = self.screen.get_width()//2 - text_surface.get_width()//2
            y = self.screen.get_height()//2 - (len(self.options)*60)//2 + i*60

            if i == self.selected_option:
                pygame.draw.rect(self.screen, COLOR_BOX,
                                 (x-20, y-10, text_surface.get_width()+40, text_surface.get_height()+20),
                                 border_radius=10)
                color = COLOR_SELECTED
            else:
                color = COLOR_TEXT

            self.render_text(text_str, color, x, y)

        # Mensajes visuales
        if self.waiting_for_key:
            msg_surface = self.font.render("Presiona una nueva tecla...", True, COLOR_WAITING)
            x = self.screen.get_width()//2 - msg_surface.get_width()//2
            y = self.screen.get_height() - 100
            self.screen.blit(msg_surface, (x, y))

        if self.message:
            color = COLOR_SUCCESS if "✔" in self.message else COLOR_ERROR #el emoji solo es para simplificar el coloreado,mas no es necesario que se muestre
            msg_surface = self.font.render(self.message, True, color)
            x = self.screen.get_width()//2 - msg_surface.get_width()//2
            y = self.screen.get_height() - 50
            self.screen.blit(msg_surface, (x, y))

        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return self.controls
                elif event.type == pygame.KEYDOWN:
                    
                    if self.waiting_for_key:
                        option_name = self.options[self.selected_option]
                        if option_name != 'Guardar y salir':
                            
                            if event.key in NO_KEYS: #Carga de excepciones de teclas 
                                key_name = pygame.key.name(event.key).upper()
                                self.message = f"No puedes asignar {key_name}"
                            else:
                                self.controls[option_name] = event.key
                                self.message = "✔ Tecla asignada correctamente"
                        self.waiting_for_key = False
                    else:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.options[self.selected_option] == 'Guardar y salir':
                                self.running = False
                            else:
                                self.waiting_for_key = True
                                self.message = ""
        return self.controls