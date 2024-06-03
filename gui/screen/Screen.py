from pygame import Surface
from pygame.font import SysFont
from gui.AbtractParentElement import AbstractParentElement
from gui.Element import Element
from gui.Drawable import Drawable
from abc import ABC
from typing import List


class Screen(AbstractParentElement, Drawable, ABC):
    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.__children: List[Element] = []
        self.drawables: List[Drawable] = []
        self.textRenderer = None
        self.width = None
        self.height = None
        self.screenInitialized = False
        self.client = None

    def getTitle(self) -> str:
        return self.title

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        for drawable in self.drawables:
            drawable.render(surface, mouse_x, mouse_y)

    def addDrawableChild(self, drawable_element):
        self.__children.append(drawable_element)
        self.drawables.append(drawable_element)
        return drawable_element

    def remove(self, child: Element) -> None:
        if isinstance(child, Drawable):
            self.drawables.remove(child)
        self.__children.remove(child)

    def clearChildren(self) -> None:
        self.drawables.clear()
        self.__children.clear()

    def children(self) -> List[Element]:
        return self.__children

    def initWithSize(self, client, width: int, height: int):
        self.client = client
        self.textRenderer = client.textRenderer
        self.width = width
        self.height = height
        if not self.screenInitialized:
            self.init()
        self.screenInitialized = True

    def init(self) -> None:
        pass

    def tick(self) -> None:
        pass
