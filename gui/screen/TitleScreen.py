from gui.screen.Screen import Screen
from gui.widget.ButtonWidget import ButtonWidget


class TitleScreen(Screen):
    def __init__(self):
        super().__init__('Title Screen')

    def init(self) -> None:
        self.addDrawableChild(
            ButtonWidget
            .builder('Triangle', lambda button: None)
            .dimensions(self.width / 2 - 200, self.height / 4 + 48, 400, 40)
            .build()
        )
        self.addDrawableChild(
            ButtonWidget
            .builder('Physics', lambda button: None)
            .dimensions(self.width / 2 - 200, self.height / 4 + 96, 400, 40)
            .build()
        )
        self.addDrawableChild(
            ButtonWidget
            .builder('Quit', lambda button: self.client.scheduleStop())
            .dimensions(self.width / 2 - 200, self.height / 4 + 144, 400, 40)
            .build()
        )
