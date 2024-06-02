from gui.widget.PressableWidget import PressableWidget
from typing import Callable


class ButtonWidget(PressableWidget):
    class Builder:
        def __init__(self, message: str, on_press: Callable[['ButtonWidget'], None]):
            self.message = message
            self.on_press = on_press
            self.x = None
            self.y = None
            self.__width = 150
            self.__height = 20

        def position(self, x: int, y: int) -> 'ButtonWidget.Builder':
            self.x = x
            self.y = y
            return self

        def width(self, width: int) -> 'ButtonWidget.Builder':
            self.__width = width
            return self

        def size(self, width: int, height: int) -> 'ButtonWidget.Builder':
            self.__width = width
            self.__height = height
            return self

        def dimensions(self, x: int, y: int, width: int, height: int) -> 'ButtonWidget.Builder':
            return self.position(x, y).size(width, height)

        def build(self) -> 'ButtonWidget':
            button_widget = ButtonWidget(self.x, self.y, self.__width, self.__height, self.message, self.on_press)
            return button_widget

    def __init__(self, x: int, y: int, width: int, height: int, message: str,
                 on_press: Callable[['ButtonWidget'], None]):
        super().__init__(x, y, width, height, message)
        self.on_press = on_press

    @staticmethod
    def builder(message: str, on_press: Callable[['ButtonWidget'], None]) -> 'ButtonWidget.Builder':
        return ButtonWidget.Builder(message, on_press)

    def onPress(self) -> None:
        print('Pressed')
        self.on_press(self)
