from gui.DrawableHelper import DrawableHelper
from gui.ParentElement import ParentElement
from gui.Element import Element
from abc import ABC
from typing import Optional


class AbstractParentElement(DrawableHelper, ParentElement, ABC):
    def __init__(self):
        self.focused: Optional[Element] = None

    def getFocused(self) -> Optional[Element]:
        return self.focused

    def setFocusedElement(self, focused: Optional[Element]) -> None:
        if self.focused is not None:
            self.focused.setFocused(False)
        if focused is not None:
            focused.setFocused(True)
        self.focused = focused
