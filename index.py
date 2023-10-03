import serial
import time
import pygame
from pygame.locals import *

# Define los puertos serie (ajusta el puerto COM o el nombre del dispositivo según tu sistema)
ser = serial.Serial('COM5', 9600)
ser.reset_input_buffer()

pygame.init()


# Configuración de la ventana
width, height = 600, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ping Pong')


# Colores
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

# posicion incial de las barras
bar_x1 = 50
bar_x2 = 530
bar_height = 180


# Posición inicial de la pelota
ball_x = width // 2
ball_y = height // 2
ball_radius = 10

# Velocidad de la pelota
ball_speed_x = 20
ball_speed_y = 20

# Puntajes iniciales de los jugadores
score_player1 = 0
score_player2 = 0

# Fuente para las etiquetas de puntaje
font = pygame.font.Font(None, 36)


# Variable para controlar el estado del juego
game_over = False

clock = pygame.time.Clock()
FPS = 120

try:
    while not game_over:
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                ser.close()
                exit()
        clock.tick(FPS)
        # Lee el valor del dimmer
        dimmerValue1 = ser.readline().decode('utf-8')
        dimmerValue2 = ser.readline().decode('utf-8')

        dimmerValue1_numeric = int(dimmerValue1.split(':')[1].strip())
        dimmerValue2_numeric = int(dimmerValue2.split(':')[1].strip())

        # print("Dimmer Value:", dimmerValue1_numeric)
        # Ajusta la posición de la barra en función del valor del dimmer
        bar_y1 = int((dimmerValue1_numeric / 1023.0) * (height - bar_height))
        bar_y2 = int((dimmerValue2_numeric / 1023.0) * (height - bar_height))

        # Mueve la pelota
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Rebote de la pelota en los bordes
        if ball_x - ball_radius < 0:
            # Incrementar el puntaje del jugador 2 y reiniciar la pelota
            score_player2 += 1
            ball_x = width // 2
            ball_y = height // 2
            # ball_speed_x = 5  # Restablecer la velocidad
        elif ball_x + ball_radius > width:
            # Incrementar el puntaje del jugador 1 y reiniciar la pelota
            score_player1 += 1
            ball_x = width // 2
            ball_y = height // 2
            # ball_speed_x = -5 # Restablecer la velocidad

        if ball_y - ball_radius < 0 or ball_y + ball_radius > height:
            ball_speed_y *= -1
            # Colisión de la pelota con la barra vertical
        if (
            ball_x + ball_radius >= bar_x1 and
            ball_x - ball_radius <= bar_x1 + 20 and
            ball_y + ball_radius >= bar_y1 and
            ball_y - ball_radius <= bar_y1 + bar_height
        ):
            ball_speed_x *= -1
        if (
            ball_x + ball_radius >= bar_x2 and
            ball_x - ball_radius <= bar_x2 + 20 and
            ball_y + ball_radius >= bar_y2 and
            ball_y - ball_radius <= bar_y2 + bar_height
        ):
            ball_speed_x *= -1

        # Borra la pantalla
        window.fill(white)

        # Dibuja la barra en la nueva posición
        pygame.draw.rect(window, blue, (bar_x1, bar_y1, 20, bar_height))
        pygame.draw.rect(window, blue, (bar_x2, bar_y2, 20, bar_height))
        pygame.draw.circle(window, red, (ball_x, ball_y), ball_radius)

         # Dibuja las etiquetas de puntaje
        label_player1 = font.render(
            "Jugador 1: {}".format(score_player1), True, red)
        label_player2 = font.render(
            "Jugador 2: {}".format(score_player2), True, red)
        window.blit(label_player1, (20, 20))
        window.blit(label_player2,
                    (width - label_player2.get_width() - 20, 20))

        if score_player1 >= 5:
            game_over = True
            winner_label = font.render("¡Jugador 1 Gana!", True, red)
            window.blit(winner_label, (width // 2 - winner_label.get_width() //
                        2, height // 2 - winner_label.get_height() // 2))
        elif score_player2 >= 5:
            game_over = True
            winner_label = font.render("¡Jugador 2 Gana!", True, red)
            window.blit(winner_label, (width // 2 - winner_label.get_width() //
                        2, height // 2 - winner_label.get_height() // 2))

        # Actualiza la pantalla
        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                ser.close()
                exit()

except KeyboardInterrupt:
    pygame.quit()
    ser.close()
