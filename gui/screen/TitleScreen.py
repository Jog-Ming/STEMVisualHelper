from pygame import Surface

from gui.screen.Screen import Screen
from gui.screen.TriangleScreen import TriangleScreen
from gui.screen.PhysicsScreen import PhysicsScreen
from gui.widget.ButtonWidget import ButtonWidget
from gui.DrawableHelper import DrawableHelper


class TitleScreen(Screen):
    def __init__(self):
        super().__init__('Title Screen')

    def init(self) -> None:
        self.addDrawableChild(
            ButtonWidget
            .builder('                  Triangles', lambda button: self.client.setScreen(TriangleScreen(self)))
            .dimensions(self.width / 2 - 200, self.height / 4 + 48, 400, 40)
            .build()
        )
        self.addDrawableChild(
            ButtonWidget
            .builder('                   Physics', lambda button: self.client.setScreen(PhysicsScreen(self)))
            .dimensions(self.width / 2 - 200, self.height / 4 + 96, 400, 40)
            .build()
        )
        self.addDrawableChild(
            ButtonWidget
            .builder('                     Quit', lambda button: self.client.scheduleStop())
            .dimensions(self.width / 2 - 200, self.height / 4 + 144, 400, 40)
            .build()
        )

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        super().render(surface, mouse_x, mouse_y)
        DrawableHelper.drawText(surface, self.textRenderer, text="STEM Visual Helper", x=int(self.width / 2) - 110,
                                y=50,
                                color=(0, 0, 0))
        DrawableHelper.drawText(surface, self.textRenderer, text="by Justin and Jim", x=int(self.width / 2) - 100,
                                y=400,
                                color=(0, 0, 0))
