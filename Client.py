from typing import Optional
import pygame
from gui.screen.Screen import Screen
from gui.screen.TitleScreen import TitleScreen


class Client:
    pygame.init()
    textRenderer = pygame.font.SysFont(('微软雅黑', 'pingfang'), 24)

    def __init__(self):
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        window_width = screen_width // 2
        window_height = screen_height // 2
        self.window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('STEM Visual Helper')
        self.clock = pygame.time.Clock()
        self.currentFPS = 60
        self.running = True
        self.currentScreen = None

    def setScreen(self, screen: Optional[Screen]) -> None:
        if screen is None:
            screen = TitleScreen()
        self.currentScreen = screen
        if screen is not None:
            self.currentScreen.initWithSize(self, self.window.get_width(), self.window.get_height())

    def run(self) -> None:
        self.setScreen(None)
        frame = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    self.currentScreen.mouseClicked(mouse_x, mouse_y, event.button)
                elif event.type == pygame.KEYDOWN:
                    self.currentScreen.keyPressed(event.key)
                    pass
                elif event.type == pygame.TEXTINPUT:
                    self.currentScreen.charTyped(event.text)
                    pass
            if frame == self.currentFPS // 20:
                frame = 0
                self.currentScreen.tick()
            else:
                frame += 1
            self.window.fill((255, 255, 255))
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.currentScreen.render(self.window, mouse_x, mouse_y)
            pygame.display.flip()
            self.clock.tick(self.currentFPS)

    def scheduleStop(self) -> None:
        self.running = False


if __name__ == '__main__':
    import os

    os.environ['SDL_IME_SHOW_UI'] = '1'
    client = Client()
    client.run()
