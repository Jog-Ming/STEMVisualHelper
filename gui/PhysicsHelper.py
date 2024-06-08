from abc import ABC
from typing import Tuple
from pygame import Surface
from pygame.draw import circle, polygon
from math import dist


class PhysicsHelper(ABC):
    class Point:
        def __init__(self, x: float, y: float):
            self.x = x
            self.y = y

        def render(self, surface: Surface) -> None:
            circle(surface, (0, 0, 0), (self.x, self.y), 2)

        def __str__(self):
            return f'Point({self.x}, {self.y})'

        def __repr__(self):
            return str(self)

        def __iter__(self):
            yield self.x
            yield self.y

    class Line:
        def __init__(self, point_1: 'PhysicsHelper.Point', point_2: 'PhysicsHelper.Point'):
            self.point_1 = point_1
            self.point_2 = point_2

        def __str__(self):
            return f'Line({self.point_1}, {self.point_2})'

        def __repr__(self):
            return str(self)

        def __iter__(self):
            yield self.point_1
            yield self.point_2

        @property
        def slope(self) -> float:
            if self.point_1.x == self.point_2.x:
                return float('inf')
            return (self.point_2.y - self.point_1.y) / (self.point_2.x - self.point_1.x)

        def closestPoint(self, p: 'PhysicsHelper.Point') -> 'PhysicsHelper.Point':
            p1, p2 = self
            if p2.y < p1.y:
                p1, p2 = p2, p1
            elif p1.y == p2.y:
                if p1.x < p2.x:
                    x = min(max(p.x, p1.x), p2.x)
                else:
                    x = max(min(p.x, p1.x), p2.x)
                return PhysicsHelper.Point(x, p1.y)
            if p1.x == p2.x:
                x = p1.x
                y = p.y
            else:
                x = (p.x / self.slope + p1.x * self.slope + p.y - p1.y) / (self.slope + 1 / self.slope)
                y = self.slope * (x - p1.x) + p1.y
            if y > p2.y:
                x, y = p2
            elif y < p1.y:
                x, y = p1
            return PhysicsHelper.Point(x, y)

        @property
        def length(self) -> float:
            return dist(self.point_1, self.point_2)

    class Polygon:
        def __init__(self, *points: 'PhysicsHelper.Point'):
            self.points = points

        @property
        def edges(self) -> Tuple['PhysicsHelper.Line', ...]:
            result = (PhysicsHelper.Line(self.points[-1], self.points[0]),)
            for i in range(len(self.points) - 1):
                result += (PhysicsHelper.Line(self.points[i], self.points[i + 1]),)
            return result

        def render(self, surface: Surface, color: Tuple[int, int, int]) -> None:
            polygon(surface, color, tuple((point.x, point.y) for point in self.points))

        def __contains__(self, p: 'PhysicsHelper.Point') -> bool:
            result = False
            for edge in self.edges:
                p1, p2 = edge
                if p2.y < p1.y:
                    p1, p2 = p2, p1
                if not p1.y <= p.y <= p2.y:
                    continue
                if p1.x == p2.x:
                    result = not result
                    continue
                if edge.slope > 0:
                    result ^= edge.slope * (p.x - p1.x) >= (p.y - p1.y)
                else:
                    result ^= edge.slope * (p.x - p1.x) <= (p.y - p1.y)
            return result

        def closestPoint(self, point: 'PhysicsHelper.Point') -> 'PhysicsHelper.Point':
            minimum_distance = float('inf')
            result = None
            for edge in self.edges:
                p = edge.closestPoint(point)
                distance = PhysicsHelper.Line(point, p).length
                if distance < minimum_distance:
                    minimum_distance = distance
                    result = p
            return result
