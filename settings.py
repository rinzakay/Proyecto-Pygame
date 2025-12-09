from Excepciones_Keys import NO_KEYS
import sys
import pygame

#Colores para el menú
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

        #Volumenes separados (se cargan desde controls si existen)
        self.music_volume = self.controls.get("music_volume", 1.0)
        self.sfx_volume = self.controls.get("sfx_volume", 1.0)

        #Opciones del menu
        # EXCLUIR claves de volumen para no remapearlas como teclas
        action_keys = [k for k in self.controls.keys() if k not in ("music_volume", "sfx_volume")]
        self.options = action_keys + ['Volumen Música', 'Volumen Efectos', 'Guardar y salir']
        self.running = False

        #Visuales
        self.waiting_for_key = False
        self.message = ""

        #Inicializar sonidos
        try:
            pygame.mixer.init()
        except pygame.error:
            print("No se pudo inicializar el mezclador de audio")

        try:
            self.buttonSound = pygame.mixer.Sound("Sound/SFX_Button.mp3")
        except pygame.error:
            self.buttonSound = None

        try:
            self.successSound = pygame.mixer.Sound("Sound/SFX_Success.wav")
        except pygame.error:
            self.successSound = None

        try:
            self.errorSound = pygame.mixer.Sound("Sound/SFX_Error.wav")
        except pygame.error:
            self.errorSound = None

        #Fondo
        try:
            self.background = pygame.image.load("image/Options_BKG.jpg")
            self.background = pygame.transform.scale(
                self.background,
                (self.screen.get_width(), self.screen.get_height())
            )
        except pygame.error:
            self.background = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            self.background.fill((0, 0, 0))

    def render_text(self, text, color, x, y):
        shadow = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x + 2, y + 2))
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
            elif option == 'Volumen Música':
                porcentaje = int(self.music_volume * 100)
                text_str = f"{option}: {porcentaje}%"
            elif option == 'Volumen Efectos':
                porcentaje = int(self.sfx_volume * 100)
                text_str = f"{option}: {porcentaje}%"
            else:
                key_value = self.controls.get(option, None)
                key_name = pygame.key.name(key_value) if isinstance(key_value, int) else "N/A"
                text_str = f"{option}: {key_name}"

            text_surface = self.font.render(text_str, True, COLOR_TEXT)
            x = self.screen.get_width() // 2 - text_surface.get_width() // 2
            y = self.screen.get_height() // 2 - (len(self.options) * 60) // 2 + i * 60

            if i == self.selected_option:
                pygame.draw.rect(
                    self.screen,
                    COLOR_BOX,
                    (x - 20, y - 10, text_surface.get_width() + 40, text_surface.get_height() + 20),
                    border_radius=10
                )
                color = COLOR_SELECTED
            else:
                color = COLOR_TEXT

            self.render_text(text_str, color, x, y)

        #Mensajes
        if self.waiting_for_key:
            msg_surface = self.font.render("Presiona una nueva tecla...", True, COLOR_WAITING)
            x = self.screen.get_width() // 2 - msg_surface.get_width() // 2
            y = self.screen.get_height() - 100
            self.screen.blit(msg_surface, (x, y))

        if self.message:
            if "✔" in self.message:
                color = COLOR_SUCCESS
            else:
                color = COLOR_ERROR
            msg_surface = self.font.render(self.message, True, color)
            x = self.screen.get_width() // 2 - msg_surface.get_width() // 2
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

                if event.type == pygame.KEYDOWN:
                    if self.waiting_for_key:
                        option_name = self.options[self.selected_option]
                        if option_name not in ['Guardar y salir', 'Volumen Música', 'Volumen Efectos']:
                            if event.key in NO_KEYS:
                                key_name = pygame.key.name(event.key).upper()
                                self.message = f"No puedes asignar {key_name}"
                                if self.errorSound:
                                    self.errorSound.set_volume(self.sfx_volume)
                                    self.errorSound.play()
                            elif event.key in [v for v in self.controls.values() if isinstance(v, int)]:
                                self.message = f"Ya está asignada a otra acción"
                                if self.errorSound:
                                    self.errorSound.set_volume(self.sfx_volume)
                                    self.errorSound.play()
                            else:
                                self.controls[option_name] = event.key
                                self.message = "✔ Tecla asignada correctamente"
                                if self.successSound:
                                    self.successSound.set_volume(self.sfx_volume)
                                    self.successSound.play()
                        self.waiting_for_key = False
                    else:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                            if self.buttonSound:
                                self.buttonSound.set_volume(self.sfx_volume)
                                self.buttonSound.play()
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                            if self.buttonSound:
                                self.buttonSound.set_volume(self.sfx_volume)
                                self.buttonSound.play()
                        elif event.key == pygame.K_LEFT:
                            if self.options[self.selected_option] == 'Volumen Música':
                                self.music_volume = max(0.0, round(self.music_volume - 0.1, 1))
                                try:
                                    pygame.mixer.music.set_volume(self.music_volume)
                                except pygame.error:
                                    pass
                            elif self.options[self.selected_option] == 'Volumen Efectos':
                                self.sfx_volume = max(0.0, round(self.sfx_volume - 0.1, 1))
                        elif event.key == pygame.K_RIGHT:
                            if self.options[self.selected_option] == 'Volumen Música':
                                self.music_volume = min(1.0, round(self.music_volume + 0.1, 1))
                                try:
                                    pygame.mixer.music.set_volume(self.music_volume)
                                except pygame.error:
                                    pass
                            elif self.options[self.selected_option] == 'Volumen Efectos':
                                self.sfx_volume = min(1.0, round(self.sfx_volume + 0.1, 1))
                        elif event.key == pygame.K_RETURN:
                            if self.options[self.selected_option] == 'Guardar y salir':
                                #Guardar volúmenes antes de salir
                                self.controls["music_volume"] = self.music_volume
                                self.controls["sfx_volume"] = self.sfx_volume
                                self.running = False
                            elif self.options[self.selected_option] not in ['Volumen Música', 'Volumen Efectos']:
                                self.waiting_for_key = True
                                self.message = ""

        return self.controls