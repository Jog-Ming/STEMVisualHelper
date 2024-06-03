from abc import ABC
from pygame import Surface
from pygame.draw import rect, aaline
from pygame.font import Font


class DrawableHelper(ABC):
    @staticmethod
    def fill(surface: Surface, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int]) -> None:
        rect(surface, color, ((x1, y1), (x2 - x1, y2 - y1)))

    @staticmethod
    def drawHorizontalLine(surface: Surface, x1: int, x2: int, y: int, color: tuple[int, int, int]) -> None:
        if x2 < x1:
            x1, x2 = x2, x1
        DrawableHelper.fill(surface, x1, y, x2 + 1, y + 1, color)

    @staticmethod
    def drawVerticalLine(surface: Surface, x: int, y1: int, y2: int, color: tuple[int, int, int]) -> None:
        if y2 < y1:
            y1, y2 = y2, y1
        DrawableHelper.fill(surface, x, y1 + 1, x + 1, y2, color)

    @staticmethod
    def drawLine(surface: Surface, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int]) -> None:
        aaline(surface, color, (x1, y1), (x2, y2))

    @staticmethod
    def drawText(surface: Surface, text_renderer: Font, text: str, x: int, y: int, color: tuple[int, int, int]) -> None:
        surface.blit(text_renderer.render(text, True, color), (x, y))
