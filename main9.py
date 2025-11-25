import pygame
import sys 

# Inicialización de pygame
pygame.init()
Ancho, Alto = 800, 600
screen = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock()

# Constantes del juego
Fps = 60
Suelo_Y = Alto - 50 
player_size = 40
player_x = 100
player_color = (255, 255, 0)
color_piso = (104, 106, 217)
color_pinchos = (226, 92, 250)

# Variables del jugador
player_y = Suelo_Y - player_size
velocidad_y = 0
gravedad = 0.8
fuerza_salto = -15
en_suelo = True

# Cargar fondos (usando superficies de color como placeholder)
FONDO_NIVEL_1 = pygame.Surface((Ancho, Alto))
FONDO_NIVEL_1.fill((50, 50, 100))
FONDO_NIVEL_2 = pygame.Surface((Ancho, Alto))
FONDO_NIVEL_2.fill((100, 50, 50))
FONDO_NIVEL_3 = pygame.Surface((Ancho, Alto))
FONDO_NIVEL_3.fill((50, 100, 50))

class Nivel:
    def __init__(self, fondo, obstaculos_matriz, velocidad=6):
        self.fondo = fondo
        self.velocidad = velocidad
        self.pinchos = [pygame.Rect(x, y, w, h) for x, y, w, h in obstaculos_matriz]

    def actualizar(self):
        for p in self.pinchos[:]:
            p.x -= self.velocidad
            if p.x <= -50:
                self.pinchos.remove(p)

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        for rect in self.pinchos:
            p1 = (rect.x, rect.y + rect.height)
            p2 = (rect.x + rect.width, rect.y + rect.height)
            p3 = (rect.x + rect.width / 2, rect.y)
            pygame.draw.polygon(pantalla, color_pinchos, [p1, p2, p3])

# Definición de niveles
niveles = {
    1: Nivel(FONDO_NIVEL_1, [
        [500, Suelo_Y - 30, 30, 40], [850, Suelo_Y - 30, 30, 40],
        [1200, Suelo_Y - 30, 30, 40], [1550, Suelo_Y - 30, 30, 40],
        [1900, Suelo_Y - 30, 30, 40], [2250, Suelo_Y - 30, 30, 40],
        [2600, Suelo_Y - 30, 30, 40], [2950, Suelo_Y - 30, 30, 40],
        [3300, Suelo_Y - 30, 30, 40], [3650, Suelo_Y - 30, 30, 40]
    ]),
    
    2: Nivel(FONDO_NIVEL_2, [
        [400, Suelo_Y - 30, 30, 40], [650, Suelo_Y - 30, 30, 40],
        [900, Suelo_Y - 30, 30, 40], [1150, Suelo_Y - 30, 30, 40],
        [1400, Suelo_Y - 30, 30, 40], [1650, Suelo_Y - 30, 30, 40],
        [1900, Suelo_Y - 30, 30, 40], [2150, Suelo_Y - 30, 30, 40],
        [600, Suelo_Y - 30, 30, 40], [630, Suelo_Y - 30, 30, 40],
        [1000, Suelo_Y - 30, 30, 40], [1030, Suelo_Y - 30, 30, 40],
        [1500, Suelo_Y - 30, 30, 40], [1530, Suelo_Y - 30, 30, 40],
        [1560, Suelo_Y - 30, 30, 40]
    ]),
    
    3: Nivel(FONDO_NIVEL_3, [
        [300, Suelo_Y - 30, 30, 40], [400, Suelo_Y - 30, 30, 40],
        [500, Suelo_Y - 30, 30, 40], [700, Suelo_Y - 30, 30, 40],
        [730, Suelo_Y - 30, 30, 40], [760, Suelo_Y - 30, 30, 40],
        [950, Suelo_Y - 30, 30, 40], [1100, Suelo_Y - 30, 30, 40],
        [1250, Suelo_Y - 30, 30, 40], [1450, Suelo_Y - 30, 30, 40],
        [1480, Suelo_Y - 30, 30, 40], [1600, Suelo_Y - 30, 30, 40],
        [1630, Suelo_Y - 30, 30, 40], [1800, Suelo_Y - 30, 30, 40],
        [1830, Suelo_Y - 30, 30, 40], [1860, Suelo_Y - 30, 30, 40],
        [2000, Suelo_Y - 30, 30, 40], [2100, Suelo_Y - 30, 30, 40],
        [2200, Suelo_Y - 30, 30, 40]
    ], velocidad=7)
}

def reiniciar_jugador():
    global player_y, velocidad_y, en_suelo
    player_y = Suelo_Y - player_size
    velocidad_y = 0
    en_suelo = True

def mostrar_mensaje(texto, color, y_pos, tamaño=60):
    font = pygame.font.SysFont(None, tamaño)
    texto_render = font.render(texto, True, color)
    x_pos = (Ancho - texto_render.get_width()) // 2
    screen.blit(texto_render, (x_pos, y_pos))
    return texto_render

def esperar_tecla_espacio():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False
        clock.tick(Fps)

def game_over():
    screen.fill((0, 0, 0))
    mostrar_mensaje("GAME OVER", (255, 0, 0), 250)
    mostrar_mensaje("Presiona ESPACIO para volver al menu", (255, 255, 255), 320, 30)
    pygame.display.flip()
    esperar_tecla_espacio()
    return "menu"

def victoria(nivel_actual):
    screen.fill((0, 0, 0))
    
    if nivel_actual < 3:
        mostrar_mensaje(f"¡Nivel {nivel_actual} Completado!", (0, 255, 0), 250)
        mostrar_mensaje("Presiona ESPACIO para siguiente nivel", (255, 255, 255), 320, 30)
    else:
        mostrar_mensaje("¡VICTORIA FINAL!", (0, 255, 255), 250)
        mostrar_mensaje("Presiona ESPACIO para volver al menu", (255, 255, 255), 320, 30)
    
    pygame.display.flip()
    esperar_tecla_espacio()
    
    if nivel_actual < 3:
        return nivel_actual + 1
    else:
        return "menu"

def dibujar_menu():
    screen.fill((30, 30, 30))
    mostrar_mensaje("Geometry Dash", (255, 255, 0), 100, 80)
    
    boton = pygame.Rect(300, 250, 200, 60)
    pygame.draw.rect(screen, (100, 100, 255), boton)
    mostrar_mensaje("JUGAR", (255, 255, 255), 260, 50)
    
    return boton

def dibujar_menu_niveles():
    screen.fill((20, 20, 60))
    mostrar_mensaje("SELECCIONA NIVEL", (255, 255, 0), 50)
    
    botones = []
    colores = [(150, 0, 200), (200, 100, 0), (0, 150, 150)]
    
    for i in range(3):
        boton = pygame.Rect(250, 150 + i * 100, 300, 60)
        pygame.draw.rect(screen, colores[i], boton)
        mostrar_mensaje(f"Nivel {i+1}", (255, 255, 255), 160 + i * 100, 50)
        botones.append(boton)
    
    return botones

# Estado inicial del juego
nivel_numero = 1
estado_juego = "menu"
nivel_actual_obj = niveles[1]

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if estado_juego == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN and 'boton_jugar' in locals() and boton_jugar.collidepoint(evento.pos):
                estado_juego = "niveles"

        elif estado_juego == "niveles":
            if evento.type == pygame.MOUSEBUTTONDOWN and 'botones_niveles' in locals():
                for i, boton in enumerate(botones_niveles):
                    if boton.collidepoint(evento.pos):
                        nivel_numero = i + 1
                        nivel_actual_obj = niveles[nivel_numero]
                        reiniciar_jugador()
                        estado_juego = "jugando"
                        break

        elif estado_juego == "jugando":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                if en_suelo:
                    velocidad_y = fuerza_salto
                    en_suelo = False

    # Dibujado según el estado
    if estado_juego == "menu":
        boton_jugar = dibujar_menu()

    elif estado_juego == "niveles":
        botones_niveles = dibujar_menu_niveles()

    elif estado_juego == "jugando":
        # Actualizar física del jugador
        velocidad_y += gravedad
        player_y += velocidad_y

        if player_y >= Suelo_Y - player_size:
            player_y = Suelo_Y - player_size
            velocidad_y = 0
            en_suelo = True

        # Actualizar nivel
        nivel_actual_obj.actualizar()

        # Detectar colisiones
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if any(player_rect.colliderect(p) for p in nivel_actual_obj.pinchos):
            estado_juego = game_over()
        elif len(nivel_actual_obj.pinchos) == 0:
            nuevo_estado = victoria(nivel_numero)
            if nuevo_estado == "menu":
                estado_juego = "menu"
            else:
                nivel_numero = nuevo_estado
                nivel_actual_obj = niveles[nivel_numero]
                reiniciar_jugador()

        # Dibujar elementos del juego
        nivel_actual_obj.dibujar(screen)
        pygame.draw.rect(screen, color_piso, (0, Suelo_Y, Ancho, 50))
        pygame.draw.rect(screen, player_color, player_rect)
        mostrar_mensaje(f"Nivel {nivel_numero}", (255, 255, 255), 20, 30)

    pygame.display.flip()
    clock.tick(Fps)