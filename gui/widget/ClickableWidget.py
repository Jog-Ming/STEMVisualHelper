from gui.DrawableHelper import DrawableHelper
from gui.Drawable import Drawable
from gui.Element import Element
from gui.widget.Widget import Widget
from abc import ABC, abstractmethod
from pygame import Surface
from pygame.font import Font
from typing import Tuple


class ClickableWidget(DrawableHelper, Drawable, Element, Widget, ABC):
    def __init__(self, x: int, y: int, width: int, height: int, message: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.message = message
        self.hovered = False
        self.visible = True
        self.focused = False
        self.active = True

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        if not self.visible:
            return
        self.hovered = self.getX() <= mouse_x < self.getX() + self.width\
            and self.getY() <= mouse_y < self.getY() + self.height
        self.renderButton(surface, mouse_x, mouse_y)

    @abstractmethod
    def renderButton(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        pass

    def drawScrollableText(
            self,
            surface: Surface,
            text_renderer: Font,
            x_margin: int,
            color: Tuple[int, int, int]
    ) -> None:
        i = self.getX() + x_margin
        ClickableWidget.drawText(surface, text_renderer, self.getMessage(), i, self.getY(), color)

    def onClick(self, mouse_x: float, mouse_y: float) -> None:
        pass

    def mouseClicked(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        if not self.active or not self.visible:
            return False
        if self.isValidClickButton(button) and self.clicked(mouse_x, mouse_y):
            self.onClick(mouse_x, mouse_y)
            return True
        return False

    @staticmethod
    def isValidClickButton(button: int) -> bool:
        return button == 1

    def clicked(self, mouse_x: float, mouse_y: float) -> bool:
        return (
            self.active
            and self.visible
            and self.getX() <= mouse_x <= self.getX() + self.width
            and self.getY() <= mouse_y <= self.getY() + self.height
        )

    def setX(self, x: int) -> None:
        self.x = x

    def setY(self, y: int) -> None:
        self.y = y

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getWidth(self) -> int:
        return self.width

    def getHeight(self) -> int:
        return self.height

    def getMessage(self) -> str:
        return self.message

    def setFocused(self, focused: bool) -> None:
        self.focused = focused

    def isFocused(self) -> bool:
        return self.focused
