import pygame

class SettingsMenu:
    def __init__(self, screen, current_controls):
        self.screen = screen
        self.controls = current_controls.copy()  # Diccionario con controles actuales
        self.font = pygame.font.SysFont(None, 36)
        self.selected_option = 0
        self.options = list(self.controls.keys()) + ['Guardar y salir']
        self.running = False

    def draw(self):
        self.screen.fill((30, 30, 30))
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            if option == 'Guardar y salir':
                text = self.font.render(option, True, color)
            else:
                key_name = pygame.key.name(self.controls[option])
                text = self.font.render(f"{option}: {key_name}", True, color)
            self.screen.blit(text, (50, 50 + i * 40))
        pygame.display.flip()

    def run(self):
        self.running = True
        waiting_for_key = False
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return self.controls  # Salir sin guardar
                elif event.type == pygame.KEYDOWN:
                    if waiting_for_key:
                        # Cambiar la tecla asignada a la opción seleccionada
                        option_name = self.options[self.selected_option]
                        self.controls[option_name] = event.key
                        waiting_for_key = False
                    else:
                        if event.key == pygame.K_UP:
                            self.selected_option = (self.selected_option - 1) % len(self.options)
                        elif event.key == pygame.K_DOWN:
                            self.selected_option = (self.selected_option + 1) % len(self.options)
                        elif event.key == pygame.K_RETURN:
                            if self.options[self.selected_option] == 'Guardar y salir':
                                self.running = False
                            else:
                                waiting_for_key = True
        return self.controls