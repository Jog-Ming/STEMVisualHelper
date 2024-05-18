from abc import ABC, abstractmethod


class Widget(ABC):
    @abstractmethod
    def setX(self, x: int) -> None:
        pass

    @abstractmethod
    def setY(self, y: int) -> None:
        pass

    @abstractmethod
    def getX(self) -> int:
        pass

    @abstractmethod
    def getY(self) -> int:
        pass

    @abstractmethod
    def getWidth(self) -> int:
        pass

    @abstractmethod
    def getHeight(self) -> int:
        pass

    def setPosition(self, x: int, y: int) -> None:
        self.setX(x)
        self.setY(y)
