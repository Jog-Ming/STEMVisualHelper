import os
import pygame
import numpy as np
from gui.screen.TitleScreen import TitleScreen

os.environ['SDL_IME_SHOW_UI'] = '1'
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
window_width = screen_width // 2
window_height = screen_height // 2
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('STEM Visual Helper')
clock = pygame.time.Clock()
textRenderer = pygame.font.SysFont(('微软雅黑', 'pingfang'), 24)
FPS = 60
frame = 0


def lines(polygon):
    result = []
    for i in range(len(polygon) - 1):
        result.append((polygon[i], polygon[i + 1]))
    result.append((polygon[-1], polygon[0]))
    return result


def point_in_polygon(x, y, polygon) -> bool:
    i = 0
    for line in lines(polygon):
        print(line)
        p1, p2 = line
        x1, y1 = p1
        x2, y2 = p2
        if y2 < y1:
            y1, y2 = y2, y1
        if not y1 <= y <= y2:
            continue
        if x1 != x2:
            i += (y2 - y1) * (x - x1) / (x2 - x1) >= y - y1
        else:
            i += x >= x1
    return i % 2 == 1


p = ((300, 300), (400, 400), (300, 400))
grid = []
for i in range(11):
    for j in range(11):
        grid.append((300 + i * 10, 300 + j * 10))
screen = TitleScreen()
screen.initWithSize(window_width, window_height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            screen.mouseClicked(mouse_x, mouse_y, event.button)
        elif event.type == pygame.KEYDOWN:
            screen.keyPressed(event.key)
            pass
        elif event.type == pygame.TEXTINPUT:
            screen.charTyped(event.text)
            pass
    if frame == FPS // 20:
        frame = 0
        screen.tick()
    else:
        frame += 1
    window.fill((255, 255, 255))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.render(window, mouse_x, mouse_y)
    # pygame.draw.polygon(window, (0, 0, 0), p)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
