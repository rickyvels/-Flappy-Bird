import pygame
import sys

# Inicialización
pygame.init()
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock()

# Constantes globales
SUELO_Y = ALTO - 50
FPS = 60

# ============================================
# 1. CLASE BASE: GameObject (Clase padre)
# ============================================
class GameObject:
    """Clase base para todos los objetos del juego"""
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
    
    def mover(self, velocidad):
        """Mueve el objeto horizontalmente"""
        self.rect.x -= velocidad
    
    def dibujar(self, pantalla):
        """Dibuja el objeto en pantalla"""
        pygame.draw.rect(pantalla, self.color, self.rect)


# ============================================
# 2. CLASE: Pincho (Hereda de GameObject)
# ============================================
class Pincho(GameObject):
    """Obstáculo triangular - HERENCIA"""
    def __init__(self, x, y, ancho=30, alto=40):
        super().__init__(x, y, ancho, alto, (226, 92, 250))
    
    def dibujar(self, pantalla):
        """Dibuja triángulo de pincho"""
        p1 = (self.rect.x, self.rect.bottom)
        p2 = (self.rect.right, self.rect.bottom)
        p3 = (self.rect.centerx, self.rect.top)
        pygame.draw.polygon(pantalla, self.color, [p1, p2, p3])


# ============================================
# 3. CLASE: Plataforma (Hereda de GameObject)
# ============================================
class Plataforma(GameObject):
    """Plataforma flotante - HERENCIA"""
    def __init__(self, x, y, ancho=80, alto=15):
        super().__init__(x, y, ancho, alto, (255, 100, 0))
    
    def dibujar(self, pantalla):
        """Dibuja plataforma con borde"""
        pygame.draw.rect(pantalla, self.color, self.rect)
        pygame.draw.rect(pantalla, (200, 50, 0), self.rect, 3)


# ============================================
# 4. CLASE: Jugador
# ============================================
class Jugador:
    """Personaje controlable del juego"""
    def __init__(self, x, y, tamaño=40):
        self.rect = pygame.Rect(x, y, tamaño, tamaño)
        self.velocidad_y = 0
        self.en_suelo = True
        self.gravedad = 0.8
        self.fuerza_salto = -15
        # Colores personalizados (4 capas)
        self.colores = [(128, 0, 128), (0, 255, 0), (75, 0, 130), (0, 191, 255)]
    
    def saltar(self):
        """Hace saltar al jugador si está en el suelo"""
        if self.en_suelo:
            self.velocidad_y = self.fuerza_salto
            self.en_suelo = False
    
    def actualizar(self, plataformas):
        """Aplica física y detecta colisiones con plataformas"""
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y
        
        # Colisión con suelo
        if self.rect.bottom >= SUELO_Y:
            self.rect.bottom = SUELO_Y
            self.velocidad_y = 0
            self.en_suelo = True
        else:
            self.en_suelo = False
        
        # Colisión con plataformas
        for plat in plataformas:
            if self.rect.colliderect(plat.rect) and self.velocidad_y > 0:
                if self.rect.bottom >= plat.rect.top and self.rect.top < plat.rect.top:
                    self.rect.bottom = plat.rect.top
                    self.velocidad_y = 0
                    self.en_suelo = True
    
    def dibujar(self, pantalla):
        """Dibuja jugador con 4 capas de colores"""
        inflaciones = [0, -6, -14, -22]
        for i, color in enumerate(self.colores):
            rect_capa = self.rect.inflate(inflaciones[i], inflaciones[i])
            pygame.draw.rect(pantalla, color, rect_capa)
    
    def reiniciar(self):
        """Reinicia posición del jugador"""
        self.rect.y = SUELO_Y - self.rect.height
        self.velocidad_y = 0
        self.en_suelo = True


# ============================================
# 5. CLASE BASE: Nivel (Clase padre de niveles)
# ============================================
class Nivel:
    """Clase base para todos los niveles - BASE PARA HERENCIA"""
    def __init__(self, fondo_path, velocidad):
        self.fondo = pygame.transform.scale(pygame.image.load(fondo_path), (ANCHO, ALTO))
        self.velocidad = velocidad
        self.pinchos = []
        self.plataformas = []
    
    def actualizar(self):
        """Mueve todos los obstáculos y limpia los que salen de pantalla"""
        for obj in self.pinchos + self.plataformas:
            obj.mover(self.velocidad)
        
        self.pinchos = [p for p in self.pinchos if p.rect.x > -50]
        self.plataformas = [p for p in self.plataformas if p.rect.x > -100]
    
    def dibujar(self, pantalla):
        """Dibuja fondo, plataformas y pinchos"""
        pantalla.blit(self.fondo, (0, 0))
        for plat in self.plataformas:
            plat.dibujar(pantalla)
        for pincho in self.pinchos:
            pincho.dibujar(pantalla)
        pygame.draw.rect(pantalla, (104, 106, 217), (0, SUELO_Y, ANCHO, 50))
    
    def esta_completo(self):
        """Verifica si el nivel está completo"""
        return len(self.pinchos) == 0


# ============================================
# 6. CLASE: Nivel1 (Hereda de Nivel)
# ============================================
class Nivel1(Nivel):
    """Nivel fácil - HERENCIA"""
    def __init__(self):
        super().__init__("img1.png", 6)
        x = 500
        for _ in range(10):
            self.pinchos.append(Pincho(x, SUELO_Y - 30))
            x += 350


# ============================================
# 7. CLASE: Nivel2 (Hereda de Nivel)
# ============================================
class Nivel2(Nivel):
    """Nivel medio - HERENCIA - DIFICULTAD AUMENTA"""
    def __init__(self):
        super().__init__("img2.png", 7)
        x = 400
        for i in range(15):
            tamaño = (35, 45) if i % 3 == 0 else (30, 40)
            self.pinchos.append(Pincho(x, SUELO_Y - tamaño[1], *tamaño))
            x += 250 if i % 2 == 0 else 320


# ============================================
# 8. CLASE: Nivel3 (Hereda de Nivel)
# ============================================
class Nivel3(Nivel):
    """Nivel difícil - HERENCIA - DIFICULTAD MÁXIMA"""
    def __init__(self):
        super().__init__("img3.png", 8)
        x = 350
        for i in range(25):
            # Añadir plataformas flotantes
            if i % 4 == 0 and i > 0:
                altura = SUELO_Y - 120 - (i % 3) * 30
                self.plataformas.append(Plataforma(x, altura))
                x += 100
            
            # Patrones de pinchos variados
            if i % 6 in [0, 1]:
                self.pinchos.append(Pincho(x, SUELO_Y - 32, 28, 38))
                x += 160
            elif i % 6 == 2:
                self.pinchos.append(Pincho(x, SUELO_Y - 45, 40, 55))
                x += 280
            elif i % 6 == 3:
                self.pinchos.append(Pincho(x, SUELO_Y - 30))
                self.pinchos.append(Pincho(x + 35, SUELO_Y - 30))
                x += 250
            else:
                self.pinchos.append(Pincho(x, SUELO_Y - 30))
                x += 240


# ============================================
# 9. CLASE: Juego (Controla el flujo del juego)
# ============================================
class Juego:
    """Controla menús, niveles y lógica del juego"""
    def __init__(self):
        self.jugador = Jugador(100, SUELO_Y - 40)
        self.nivel_actual = None
        self.estado = "menu"
    
    def cambiar_nivel(self, numero):
        """Cambia al nivel seleccionado"""
        niveles = {1: Nivel1, 2: Nivel2, 3: Nivel3}
        self.nivel_actual = niveles[numero]()
        self.jugador.reiniciar()
        self.estado = "jugando"
    
    def mostrar_texto(self, texto, y, tamaño=60, color=(255, 255, 255)):
        """Muestra texto centrado en pantalla"""
        font = pygame.font.SysFont(None, tamaño)
        superficie = font.render(texto, True, color)
        x = (ANCHO - superficie.get_width()) // 2
        screen.blit(superficie, (x, y))
    
    def game_over(self):
        """Pantalla de derrota - vuelve al menú"""
        self.mostrar_texto("GAME OVER", 250, 60, (255, 0, 0))
        self.mostrar_texto("Presiona ESPACIO para volver al menu", 320, 35)
        pygame.display.flip()
        
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    self.estado = "menu"  # ← VUELVE AL MENÚ PRINCIPAL
                    self.nivel_actual = None
                    self.jugador.reiniciar()
                    esperando = False
    
    def victoria(self):
        """Pantalla de victoria"""
        self.mostrar_texto("¡GANASTE!", 250, 60, (0, 255, 0))
        self.mostrar_texto("Presiona ESPACIO", 320, 40)
        pygame.display.flip()
        
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    self.estado = "niveles"
                    esperando = False
    
    def dibujar_menu(self):
        """Dibuja menú principal"""
        screen.fill((30, 30, 30))
        self.mostrar_texto("Geometry Dash", 100, 80, (255, 255, 0))
        self.mostrar_texto("Presiona ESPACIO para jugar", 350, 35, (200, 200, 200))
    
    def dibujar_menu_niveles(self):
        """Dibuja menú de selección de niveles"""
        screen.fill((20, 20, 60))
        self.mostrar_texto("SELECCIONA NIVEL", 50, 60, (255, 255, 0))
        self.mostrar_texto("Presiona 1, 2 o 3", 120, 35, (200, 200, 200))
        
        niveles = ["1 - Nivel 1 (Fácil)", "2 - Nivel 2 (Medio)", "3 - Nivel 3 (Difícil)"]
        for i, txt in enumerate(niveles):
            self.mostrar_texto(txt, 200 + i * 80, 45)
    
    def ejecutar(self):
        """Bucle principal del juego"""
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                
                if evento.type == pygame.KEYDOWN:
                    # Menú principal
                    if self.estado == "menu" and evento.key == pygame.K_SPACE:
                        self.estado = "niveles"
                    
                    # Selección de niveles
                    elif self.estado == "niveles":
                        if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                            self.cambiar_nivel(int(evento.unicode))
                    
                    # Jugando
                    elif self.estado == "jugando" and evento.key == pygame.K_SPACE:
                        self.jugador.saltar()
            
            # Renderizado según estado
            if self.estado == "menu":
                self.dibujar_menu()
            
            elif self.estado == "niveles":
                self.dibujar_menu_niveles()
            
            elif self.estado == "jugando":
                self.jugador.actualizar(self.nivel_actual.plataformas)
                self.nivel_actual.actualizar()
                
                # Colisión con pinchos - GAME OVER
                if any(self.jugador.rect.colliderect(p.rect) for p in self.nivel_actual.pinchos):
                    self.nivel_actual.dibujar(screen)
                    self.jugador.dibujar(screen)
                    pygame.display.flip()
                    pygame.time.wait(300)  # Pausa breve antes del game over
                    self.game_over()
                    continue  # ← Importante: salta al siguiente frame después del game over
                
                # Victoria
                if self.nivel_actual.esta_completo():
                    self.victoria()
                
                # Dibujar todo
                self.nivel_actual.dibujar(screen)
                self.jugador.dibujar(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()


# ============================================
# EJECUCIÓN DEL JUEGO
# ============================================
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()