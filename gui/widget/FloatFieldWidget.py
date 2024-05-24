from gui.widget.TextFieldWidget import *


class FloatFieldWidget(TextFieldWidget):
    def write(self, char: str) -> None:
        if char.isdigit() or '.' in char and '.' not in self.text:
            super().write(char)
