from pygame import Surface
from pygame.font import Font
from gui.widget.ClickableWidget import ClickableWidget
from abc import ABC, abstractmethod
from typing import Tuple


class PressableWidget(ClickableWidget, ABC):
    def __init__(self, x: int, y: int, width: int, height: int, message: str):
        super().__init__(x, y, width, height, message)

    @abstractmethod
    def onPress(self) -> None:
        pass

    def renderButton(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        PressableWidget.drawHorizontalLine(
            surface,
            self.getX(),
            self.getX() + self.getWidth(),
            self.getY(),
            (0, 0, 0)
        )
        PressableWidget.drawHorizontalLine(
            surface,
            self.getX(),
            self.getX() + self.getWidth(),
            self.getY() + self.getHeight(),
            (0, 0, 0)
        )
        PressableWidget.drawVerticalLine(
            surface,
            self.getX(),
            self.getY(),
            self.getY() + self.getHeight(),
            (0, 0, 0)
        )
        PressableWidget.drawVerticalLine(
            surface,
            self.getX() + self.getWidth(),
            self.getY(),
            self.getY() + self.getHeight(),
            (0, 0, 0)
        )
        if self.active:
            i = (0x00, 0x00, 0x00)
        else:
            i = (0xA0, 0xA0, 0xA0)
        from Client import Client
        self.drawMessage(surface, Client.textRenderer, i)

    def drawMessage(self, surface: Surface, text_renderer: Font, color: Tuple[int, int, int]):
        self.drawScrollableText(surface, text_renderer, 2, color)

    def onClick(self, mouse_x: float, mouse_y: float):
        self.onPress()
