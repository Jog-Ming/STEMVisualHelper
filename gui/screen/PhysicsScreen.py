from pygame import Surface
from pygame import draw
from gui.widget.ButtonWidget import ButtonWidget
from gui.screen.Screen import Screen
from gui.PhysicsHelper import PhysicsHelper
from math import atan2, sin, cos, dist


class PhysicsScreen(Screen, PhysicsHelper):
    class SoftBodyPoint(PhysicsHelper.Point):
        TPS = 600

        def __init__(self, mass: float, x: float, y: float):
            super().__init__(x, y)
            self.mass = mass
            self.neighbors = []
            self.distances = []
            self.velocity_x = 0.0
            self.velocity_y = 0.0

        def addNeighbor(self, neighbor):
            self.neighbors.append(neighbor)
            self.distances.append(dist((self.x, self.y), (neighbor.x, neighbor.y)))

        def updateVelocity(self):
            force_x = 0.0
            force_y = 0.0
            for i in range(len(self.neighbors)):
                neighbor = self.neighbors[i]
                dx = dist((self.x, self.y), (neighbor.x, neighbor.y)) - self.distances[i]
                theta = atan2(neighbor.y - self.y, neighbor.x - self.x)
                force = dx * 40.0
                force_x += force * cos(theta)
                force_y += force * sin(theta)
            self.velocity_x += force_x / self.TPS / self.mass
            self.velocity_y += force_y / self.TPS / self.mass
            self.velocity_y += 50.0 / self.TPS

        def updatePosition(self):
            self.x += self.velocity_x / self.TPS
            self.y += self.velocity_y / self.TPS

        def render(self, surface: Surface) -> None:
            pass

        def __repr__(self):
            return str((self.x, self.y))

    def __init__(self, parent: Screen):
        super().__init__('Physics Screen')
        self.parent = parent
        self.colliders = (
            PhysicsHelper.Polygon(
                PhysicsHelper.Point(100, 200),
                PhysicsHelper.Point(220, 320),
                PhysicsHelper.Point(100, 320),
            ),
            PhysicsHelper.Polygon(
                PhysicsHelper.Point(500, 300),
                PhysicsHelper.Point(380, 420),
                PhysicsHelper.Point(500, 420),
            )
        )
        self.grid_size = 5
        self.grid_pixels = 100
        self.soft_body = []
        for i in range(self.grid_size + 1):
            for j in range(self.grid_size + 1):
                self.soft_body.append(
                    PhysicsScreen.SoftBodyPoint(
                        1.0 / (self.grid_size + 1) ** 2,
                        j * self.grid_pixels / self.grid_size + 110,
                        i * self.grid_pixels / self.grid_size + 0,
                    )
                )
        for i in range(self.grid_size + 1):
            for j in range(self.grid_size + 1):
                neighbors = (
                    (i - 1, j - 1),
                    (i, j - 1),
                    (i + 1, j - 1),
                    (i - 1, j),
                    (i + 1, j),
                    (i - 1, j + 1),
                    (i, j + 1),
                    (i + 1, j + 1)
                )
                for neighbor in neighbors:
                    neighbor_x, neighbor_y = neighbor
                    if 0 <= neighbor_x <= self.grid_size and 0 <= neighbor_y <= self.grid_size:
                        self.soft_body[i * (self.grid_size + 1) + j].addNeighbor(
                            self.soft_body[neighbor_x * (self.grid_size + 1) + neighbor_y])

    def init(self) -> None:
        self.addDrawableChild(
            ButtonWidget
            .builder('Back', lambda button: self.client.setScreen(self.parent))
            .dimensions(0, 0, 60, 40)
            .build()
        )

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        super().render(surface, mouse_x, mouse_y)
        for polygon in self.colliders:
            polygon.render(surface, (0, 0, 0))
        for _ in range(PhysicsScreen.SoftBodyPoint.TPS // 60):
            for point in self.soft_body:
                for polygon in self.colliders:
                    if point in polygon:
                        x, y = polygon.closestPoint(point)
                        dx = x - point.x
                        dy = y - point.y
                        point.x = x
                        point.y = y
                        velocity = (point.velocity_x ** 2 + point.velocity_y ** 2) ** 0.5
                        theta = atan2(dy, dx)
                        point.velocity_x = velocity * cos(theta)
                        point.velocity_y = velocity * sin(theta)
                point.updateVelocity()
            for point in self.soft_body:
                point.updatePosition()
        border_points = []
        for i in range(self.grid_size):
            point = self.soft_body[i]
            border_points.append((point.x, point.y))
        for i in range(self.grid_size):
            point = self.soft_body[i * (self.grid_size + 1) + self.grid_size]
            border_points.append((point.x, point.y))
        for i in range(self.grid_size):
            point = self.soft_body[(self.grid_size + 1) * self.grid_size + self.grid_size - i]
            border_points.append((point.x, point.y))
        for i in range(self.grid_size):
            point = self.soft_body[(self.grid_size + 1) * self.grid_size - i * (self.grid_size + 1)]
            border_points.append((point.x, point.y))
        draw.polygon(surface, (255, 128, 128), border_points)
        for point in self.soft_body:
            point.render(surface)
