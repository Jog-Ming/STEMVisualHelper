from abc import ABC, abstractmethod
from pygame import Surface


class Drawable(ABC):
    @abstractmethod
    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        pass
