from gui.screen.Screen import Screen


class TriangleScreen(Screen):
    def __init__(self, parent: Screen):
        super().__init__('Triangle Screen')
        self.parent = parent

    def init(self) -> None:
        pass

    def tick(self) -> None:
        pass
