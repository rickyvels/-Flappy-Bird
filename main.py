import pygame
import sys 

Ancho=800
Alto=600

Fps=60

pygame.init()
pygame.display.set_caption("Gemoetri dash ")
screen =pygame.display.set_mode((Ancho,Alto))
clock=pygame.time.Clock()

def mostrar_menu():
  print("n\=====Menu====")
  print("1.Jugar")
  print("2.opciones")
  print("3.Salir")
def main ():
  while True:
    mostrar_menu()
    opcion=input("seleciona una opcion")

    if opcion=="1":
      print("Iniciando el juegon\n")
      #logica del juego poner aqui
    else opcion
      

ejecutando=True
while ejecutando:
  for evento in pygame.event.get():
    if evento.type==pygame.QUIT:
      ejecutando=False
  pygame.display.flip()

  clock.tick(Fps)

pygame.quit()








