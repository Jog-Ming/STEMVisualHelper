from gui.screen.Screen import Screen
from gui.screen.TriangleScreen import TriangleScreen
from gui.screen.PhysicsScreen import PhysicsScreen
from gui.widget.ButtonWidget import ButtonWidget


class TitleScreen(Screen):
    def __init__(self):
        super().__init__('Title Screen')

    def init(self) -> None:
        self.addDrawableChild(
            ButtonWidget
            .builder('Triangle', lambda button: self.client.setScreen(TriangleScreen(self)))
            .dimensions(self.width / 2 - 200, self.height / 4 + 48, 400, 40)
            .build()
        )
        self.addDrawableChild(
            ButtonWidget
            .builder('Physics', lambda button: self.client.setScreen(PhysicsScreen(self)))
            .dimensions(self.width / 2 - 200, self.height / 4 + 96, 400, 40)
            .build()
        )
        self.addDrawableChild(
            ButtonWidget
            .builder('Quit', lambda button: self.client.scheduleStop())
            .dimensions(self.width / 2 - 200, self.height / 4 + 144, 400, 40)
            .build()
        )
