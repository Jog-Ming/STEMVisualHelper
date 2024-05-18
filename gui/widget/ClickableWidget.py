from gui.Drawable import *
from gui.Element import *
from gui.widget.Widget import *


class ClickableWidget(Drawable, Element, ABC):
    def __init__(self, x: int, y: int, width: int, height: int, message: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.message = message
        self.hovered = False
        self.visible = True
        self.focused = False

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        if not self.visible:
            return
        self.hovered = self.getX() <= mouse_x < self.getX() + self.width\
            and self.getY() <= mouse_y < self.getY() + self.height
        self.renderButton(surface, mouse_x, mouse_y)

    @abstractmethod
    def renderButton(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        pass

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

    def setFocused(self, focused: bool) -> None:
        self.focused = focused

    def isFocused(self) -> bool:
        return self.focused
