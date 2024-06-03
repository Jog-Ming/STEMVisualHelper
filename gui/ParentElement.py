from abc import ABC, abstractmethod
from gui.Element import Element
from typing import List, Optional


class ParentElement(Element, ABC):
    @abstractmethod
    def children(self) -> List[Element]:
        pass

    def mouseClicked(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        for element in self.children():
            if not element.mouseClicked(mouse_x, mouse_y, button):
                continue
            self.setFocusedElement(element)
            return True
        return False

    def keyPressed(self, key_code: int) -> bool:
        return self.getFocused() is not None and self.getFocused().keyPressed(key_code)

    def charTyped(self, char: str) -> bool:
        return self.getFocused() is not None and self.getFocused().charTyped(char)

    @abstractmethod
    def getFocused(self) -> Optional[Element]:
        pass

    @abstractmethod
    def setFocusedElement(self, focused: Optional[Element]) -> None:
        pass

    def setFocused(self, focused: bool) -> None:
        pass

    def isFocused(self) -> bool:
        return self.getFocused() is not None
