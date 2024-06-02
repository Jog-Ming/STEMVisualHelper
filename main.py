import os
import pygame
from gui.widget.ButtonWidget import ButtonWidget

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
textRenderer = pygame.font.SysFont(('微软雅黑', 'pingfang'), 12)
FPS = 60
frame = 0

widget = ButtonWidget.builder('', lambda x: None).position(0, 0).build()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            widget.mouseClicked(mouse_x, mouse_y, event.button)
        elif event.type == pygame.KEYDOWN:
            widget.keyPressed(event.key)
        elif event.type == pygame.TEXTINPUT:
            widget.charTyped(event.text)
    if frame == FPS // 20:
        frame = 0
        # widget.tick()
    else:
        frame += 1
    window.fill((255, 255, 255))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    widget.render(window, mouse_x, mouse_y)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
