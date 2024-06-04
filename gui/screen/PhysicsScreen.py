from pygame import Surface
from pygame import draw
from gui.widget.ButtonWidget import ButtonWidget
from gui.screen.Screen import Screen
from typing import Tuple
from math import atan, sin, cos


class PhysicsScreen(Screen):
    class SoftBodyPoint:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y
            self.neighbors = []
            self.distances = []
            self.velocity_x = 0.0
            self.velocity_y = 0.0

        def add_neighbor(self, neighbor):
            self.neighbors.append(neighbor)
            self.distances.append(((self.x - neighbor.x) ** 2 + (self.y - neighbor.y) ** 2) ** 0.5)

        def tick(self):
            force_x = 0
            force_y = 10
            for i, neighbor in enumerate(self.neighbors):
                dx = ((self.x - neighbor.x) ** 2 + (self.y - neighbor.y) ** 2) ** 0.5 - self.distances[i]
                force = 10 * dx
                if self.x - neighbor.x > 0:
                    force = -force
                if self.x == neighbor.x:
                    force_y += -force
                    continue
                theta = atan((self.y - neighbor.y) / (self.x - neighbor.x))
                force_x += force * cos(theta)
                force_y += force * sin(theta)
            self.velocity_x += force_x / 60
            self.velocity_y += force_y / 60
            self.x += self.velocity_x / 60
            self.y += self.velocity_y / 60

        def __repr__(self):
            return str((self.x, self.y))

    @staticmethod
    def point_in_polygon(point: Tuple[float, float], polygon: Tuple[Tuple[int, int], ...]) -> bool:
        x, y = point
        edges = []
        for i in range(len(polygon) - 1):
            edges.append((polygon[i], polygon[i + 1]))
        edges.append((polygon[-1], polygon[0]))
        intersections = 0
        for edge in edges:
            point_1, point_2 = edge
            x1, y1 = point_1
            x2, y2 = point_2
            if y2 < y1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            if not y1 <= y <= y2:
                continue
            if x1 == x2:
                intersections += x >= x1
            else:
                slope = (y2 - y1) / (x2 - x1)
                if slope > 0:
                    intersections += slope * (x - x1) >= (y - y1)
                else:
                    intersections += slope * (x - x1) <= (y - y1)
        return intersections % 2 == 1

    @staticmethod
    def closest_point_on_line(point: Tuple[float, float], line:Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[float, float]:
        p1, p2 = line
        x1, y1 = p1
        x2, y2 = p2
        xt, yt = point
        if y2 < y1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if x1 != x2:
            m = (y2 - y1) / (x2 - x1)
        else:
            m = 1e10
        if y1 != y2:
            rm = 1 / m
        else:
            rm = 1e10
        x = (xt * rm - x1 * m + yt - y1) / (m + rm)
        y = m * (x - x1) + y1
        if y > y2:
            x = x2
            y = y2
        elif y < y1:
            x = x1
            y = y1
        return x, y

    @staticmethod
    def closest_point_in_polygon(point, polygon) -> Tuple[float, float]:
        edges = []
        for i in range(len(polygon) - 1):
            edges.append((polygon[i], polygon[i + 1]))
        edges.append((polygon[-1], polygon[0]))
        min_distance = 1e10
        min_point = None
        for edge in edges:
            p = PhysicsScreen.closest_point_on_line(point, edge)
            distance = ((point[0] - p[0]) ** 2 + (point[1] - p[1]) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                min_point = p
        return min_point

    def __init__(self, parent: Screen):
        super().__init__('Physics Screen')
        self.parent = parent
        self.colliders = (((100, 300), (200, 400), (100, 400)),)
        self.grid_size = 2
        self.grid_length = 100
        self.soft_body = []
        for i in range(self.grid_size + 1):
            for j in range(self.grid_size + 1):
                self.soft_body.append(PhysicsScreen.SoftBodyPoint(j * self.grid_length / self.grid_size + 110, i * self.grid_length / self.grid_size))
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
                        self.soft_body[i * (self.grid_size + 1) + j].add_neighbor(self.soft_body[neighbor_x * (self.grid_size + 1) + neighbor_y])

    def init(self) -> None:
        self.addDrawableChild(
            ButtonWidget
            .builder('Back', lambda button: self.client.setScreen(self.parent))
            .dimensions(0, 0, 60, 40)
            .build()
        )

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        super().render(surface, mouse_x, mouse_y)
        for point in self.soft_body:
            for polygon in self.colliders:
                if PhysicsScreen.point_in_polygon((point.x, point.y), polygon):
                    # x, y = PhysicsScreen.closest_point_in_polygon((point.x, point.y), polygon)
                    # point.x = x
                    # point.y = y
                    point.velocity_x = -0.8 * point.velocity_x
                    point.velocity_y = -0.8 * point.velocity_y
            point.tick()
        for polygon in self.colliders:
            draw.polygon(surface, (0, 0, 0), polygon)
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
        draw.polygon(surface, (255, 0, 0), border_points)
        for point in self.soft_body:
            draw.circle(surface, (0, 0, 0), (point.x, point.y), 2)
