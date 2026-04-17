import pygame
import sys
import os
import math
from datetime import datetime


def run_clock():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    timer = pygame.time.Clock()

    base_path = os.path.dirname(__file__)
    img_path = os.path.join(base_path, "images", "mickey_clock.png")

    bg = pygame.image.load(img_path).convert_alpha()
    bg = pygame.transform.scale(bg, (700, 700))

    bg_x = 50
    bg_y = 50


    center_x = 400
    center_y = 400

    def draw_hand(length, angle, color, width):
        rad = math.radians(angle - 90)

        end_x = center_x + length * math.cos(rad)
        end_y = center_y + length * math.sin(rad)

        pygame.draw.line(screen, color, (center_x, center_y), (end_x, end_y), width)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = minutes * 6
        second_angle = seconds * 6

        screen.fill((255, 255, 255))
        screen.blit(bg, (bg_x, bg_y))

        # новые руки
        draw_hand(140, minute_angle, (0, 0, 255), 10)
        draw_hand(170, second_angle, (255, 0, 0), 6)

        # точка центра, чтобы было видно откуда идут руки
        pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), 8)

        pygame.display.flip()
        timer.tick(60)

    pygame.quit()
    sys.exit()