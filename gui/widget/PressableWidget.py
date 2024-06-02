from pygame import Surface
from pygame.draw import line
from gui.widget.ClickableWidget import ClickableWidget
from abc import ABC, abstractmethod


class PressableWidget(ClickableWidget, ABC):
    def __init__(self, x: int, y: int, width: int, height: int, message: str):
        super().__init__(x, y, width, height, message)

    @abstractmethod
    def onPress(self) -> None:
        pass

    def renderButton(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        line(surface, (0, 0, 0),
             (self.getX(), self.getY()),
             (self.getX() + self.getWidth(), self.getY()))
        line(surface, (0, 0, 0),
             (self.getX() + self.getWidth(), self.getY()),
             (self.getX() + self.getWidth(), self.getY() + self.getHeight()))
        line(surface, (0, 0, 0),
             (self.getX() + self.getWidth(), self.getY() + self.getHeight()),
             (self.getX(), self.getY() + self.getHeight()))
        line(surface, (0, 0, 0),
             (self.getX(), self.getY() + self.getHeight()),
             (self.getX(), self.getY()))

    def onClick(self, mouse_x: float, mouse_y: float):
        self.onPress()
