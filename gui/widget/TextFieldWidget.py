from gui.widget.ClickableWidget import *
from pygame.font import Font
from pygame.draw import line
from pygame import K_LEFT, K_RIGHT, K_BACKSPACE, K_DELETE


class TextFieldWidget(ClickableWidget):
    def __init__(self, text_renderer: Font, x: int, y: int, width: int, height: int, text: str):
        self.text = ''
        self.focusedTicks = 0
        self.selectionStart = None
        super().__init__(x, y, width, height, text)
        self.textRenderer = text_renderer

    def mouseClicked(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        if not self.isVisible() or button != 1:
            return False
        self.setFocused(self.hovered)
        if self.isFocused() and self.hovered:
            i = 0
            x = mouse_x - self.x
            prev_width = 0
            while i <= len(self.text):
                width = self.textRenderer.render(self.text[:i], True, (0, 0, 0)).get_width()
                if x <= width:
                    if x - prev_width < width - x:
                        i -= 1
                    break
                i += 1
                prev_width = width
            self.setCursor(i)
            return True
        return False

    def keyPressed(self, key_code: int) -> bool:
        if not self.isActive():
            return False
        if key_code == K_LEFT:
            self.moveCursor(-1)
        elif key_code == K_RIGHT:
            self.moveCursor(1)
        elif key_code == K_BACKSPACE:
            self.erase(-1)
        elif key_code == K_DELETE:
            self.erase(1)

    def charTyped(self, char: str) -> bool:
        if not self.isActive():
            return False
        self.write(char)
        return True

    def renderButton(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        if not self.isVisible():
            return
        surface.blit(self.textRenderer.render(self.text, True, (0, 0, 0)), (self.x, self.y))
        if self.isFocused() and self.focusedTicks // 6 % 2 == 0:
            x = self.x + self.textRenderer.render(self.text[:self.selectionStart], True, (0, 0, 0)).get_width()
            line(surface, (0, 0, 0), (x, self.y), (x, self.y + self.textRenderer.get_height()))

    def tick(self) -> None:
        self.focusedTicks += 1

    def setFocused(self, focused: bool) -> None:
        super().setFocused(focused)
        if focused:
            self.focusedTicks = 0

    def isVisible(self) -> bool:
        return self.visible

    def isActive(self) -> bool:
        return self.isVisible() and self.isFocused()

    def write(self, char: str) -> None:
        self.text = self.text[:self.selectionStart] + char + self.text[self.selectionStart:]
        self.setSelectionStart(self.selectionStart + len(char))

    def eraseCharacters(self, character_offset: int) -> None:
        if not self.text:
            return
        if character_offset < 0:
            self.text = self.text[:self.selectionStart + character_offset] + self.text[self.selectionStart:]
            self.setSelectionStart(self.selectionStart + character_offset)
        else:
            self.text = self.text[:self.selectionStart] + self.text[self.selectionStart + character_offset:]

    def erase(self, offset: int) -> None:
        self.eraseCharacters(offset)

    def setSelectionStart(self, cursor: int) -> None:
        self.selectionStart = max(min(cursor, len(self.text)), 0)

    def setCursor(self, cursor: int) -> None:
        self.setSelectionStart(cursor)

    def moveCursor(self, offset: int) -> None:
        self.setCursor(self.selectionStart + offset)
