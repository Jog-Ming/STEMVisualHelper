from abc import ABC, abstractmethod


class Element(ABC):
    def mouseClicked(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        return False

    def keyPressed(self, key_code: int) -> bool:
        return False

    def charTyped(self, char: str) -> bool:
        return False

    @abstractmethod
    def setFocused(self, focused: bool) -> None:
        pass

    @abstractmethod
    def isFocused(self) -> bool:
        pass
