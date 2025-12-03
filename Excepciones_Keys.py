import pygame

#Lista de todas las teclas que pueden ser asignadas como controles
#Si se intentan añadir, se mandara dentro de ajustes del juego un mensaje de error personalizado
NO_KEYS = {
    pygame.K_RETURN,                    #Enter
    pygame.K_ESCAPE,                    #Escape
    pygame.K_TAB,                       #Tabulador
    pygame.K_LSUPER, pygame.K_RSUPER,   #Tecla Windows
    pygame.K_CAPSLOCK,                  #Bloqueo Mayuscula
    pygame.K_NUMLOCK,                   #Bloqueo Numerico
    pygame.K_SCROLLLOCK,                #Bloqueo Desplazamiento
    pygame.K_PRINTSCREEN,               #Imprimir Pantalla
    pygame.K_PAUSE,                     #Pausa
    pygame.K_INSERT,                    #Insert
    pygame.K_DELETE,                    #Eliminar
    pygame.K_HOME,                      #Inicio
    pygame.K_END,                       #Fin    
    pygame.K_PAGEUP,                    #Re Pagina
    pygame.K_PAGEDOWN,                  #Av Pagina
    
    #Todas las teclas de funcion
    pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4,
    pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8,
    pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12,
}