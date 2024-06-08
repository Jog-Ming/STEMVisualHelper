from pygame import Surface

from gui.screen.Screen import Screen

from math import sin, cos, radians
from gui.widget.FloatFieldWidget import FloatFieldWidget
from gui.widget.ButtonWidget import ButtonWidget
from gui.DrawableHelper import DrawableHelper
from Triangle_check import tri_type, area, tri_n


def draw_triangle(v, ori, p, window):
    # draw the triangle with 6 datas, point B (or C??) position, and the length of a
    DrawableHelper.drawHorizontalLine(window, ori[0], ori[0] + p, ori[1], (0, 0, 0))
    DrawableHelper.drawLine(
        window,
        ori[0],
        ori[1],
        int(ori[0] + p * v[1] * cos(radians(v[5])) / v[0]),
        int(ori[1] - p * v[1] * sin(radians(v[5])) / v[0]),
        (0, 0, 0)
    )
    DrawableHelper.drawLine(
        window,
        ori[0] + p,
        ori[1],
        # int(ori[0] + p * v[1] * cos(radians(v[5])) / v[0]),
        # int(ori[1] - p * v[1] * sin(radians(v[5])) / v[0]),
        int(ori[0] + p - p * v[2] * cos(radians(v[4])) / v[0]),
        int(ori[1] - p * v[2] * sin(radians(v[4])) / v[0]),
        (0, 0, 0)
    )


def sort_triangle(v):
    # make sure that the v[0] is the longest side
    v_s = v[:3]
    v_a = v[3:]
    v_s.sort(reverse=True)
    v_a.sort(reverse=True)
    v = v_s + v_a
    return v


def print_area(v, ori, window, textRenderer):
    DrawableHelper.drawText(window, textRenderer, text=f"Area: {round(area(v[0], v[1], v[2]), 3)}", x=ori[0] + 40,
                            y=ori[1] + 60, color=(0, 0, 0))


def print_type(v, ori, window, textRenderer):
    DrawableHelper.drawText(window, textRenderer, text= tri_type(v), x=ori[0],
                            y=ori[1] + 30, color=(0, 0, 0))



class TriangleScreen(Screen):
    def __init__(self, parent: Screen):
        super().__init__('Triangle Screen')
        self.parent = parent
        # receiving data ---------------------- start
        self.is_tri = 0  # the number of triangles that can be formed
        self.non_ZERO = 0  # the number of data given

        # the following list consists of 6 data: 3 sides and 3 angles
        # v[i] and v[i + 3] are corresponding sides and angles
        self.v = [0, 0, 0, 0, 0, 0]  # the list of the data given, AND the final list of the final 6 values of a triangle
        self.v1 = [0, 0, 0, 0, 0, 0]  # the list of the final 6 values of the two triangles
        self.v2 = [0, 0, 0, 0, 0, 0]
        self.names = ['a', 'b', 'c', 'A', 'B', 'C']  # the names of the side and angle

    def init(self) -> None:
        for i in range(6):
            self.addDrawableChild(FloatFieldWidget(self.textRenderer, 60, 50 + i * 40, 200, 40, ''))

        self.addDrawableChild(
            ButtonWidget
            .builder('Back', lambda button: self.client.setScreen(self.parent))
            .dimensions(0, 0, 60, 40)
            .build()
        )

    def render(self, surface: Surface, mouse_x: int, mouse_y: int) -> None:
        super().render(surface, mouse_x, mouse_y)

        # draw the title
        DrawableHelper.drawText(surface, self.textRenderer, text="Triangle Solver", x=int(self.width / 2) - 75, y=0,
                                color=(0, 0, 0))
        # draw the number of data inputted and triangles possible
        if self.is_tri:
            DrawableHelper.drawText(surface, self.textRenderer, text=f"There are {self.non_ZERO} datas inputted", x=200, y=370,
                                    color=(0, 0, 0))
        else:
            DrawableHelper.drawText(surface, self.textRenderer, text=f"There are {self.non_ZERO} datas inputted", x=200,
                                    y=370,
                                    color=(255, 0, 0))

        if self.is_tri:
            DrawableHelper.drawText(surface, self.textRenderer, text=f"There is {self.is_tri} triangles formed", x=200, y=410,
                                color=(0, 0, 0))

        else:
            DrawableHelper.drawText(surface, self.textRenderer, text=f"There is {self.is_tri} triangles formed", x=200,
                                    y=410,
                                    color=(255, 0, 0))

        for i in range(6):
            DrawableHelper.drawText(surface, self.textRenderer, f'{self.names[i]}: ', x=20, y=50 + 40 * i, color=(0, 0, 0))

        # receive data for sides and angles AND find how data points are given
        self.non_ZERO = 0

        for i in range(6):
            if self.children()[i].text:
                self.v[i] = float(self.children()[i].text)
                self.non_ZERO += 1
            else:
                self.v[i] = 0

        sides = {}
        angles = {}
        for i in range(3):
            if self.v[i]:
                sides[self.names[i]] = self.v[i]
        for i in range(3, 6):
            if self.v[i]:
                angles[self.names[i]] = self.v[i]

        if self.non_ZERO >= 3:  # if there is only 3 data, solve the triangle.
            values = tri_n(sides, angles, self.non_ZERO)

            if values[0] == -1:  # There is no triangle
                self.is_tri = 0
            elif values[0] == 1e10:  # There is inf triangles
                self.is_tri = float("inf")
                self.v = values[1]
            elif len(values) == 2:  # There is two triangles
                self.is_tri = 2
                self.v1 = values[0]
                self.v2 = values[1]
            else:  # There is one triangle
                self.is_tri = 1
                self.v = values
        else:  # There is not enough of information to even decide a triangle
            self.is_tri = 0

        p = 200
        if self.is_tri == 1:  # if there is only 1 possible triangle or inf triangles
            self.v = sort_triangle(self.v)

            ori = (300, 250)

            draw_triangle(self.v, ori, p, surface)
            print_type(self.v, ori, surface, self.textRenderer)
            print_area(self.v, ori, surface, self.textRenderer)
        if self.is_tri == float("inf"):
            self.v = sort_triangle(self.v)

            ori = (300, 250)

            draw_triangle(self.v, ori, p, surface)
            print_type(self.v, ori, surface, self.textRenderer)
        elif self.is_tri == 2:  # if there is 2 possible triangles
            self.v1 = sort_triangle(self.v1)
            self.v2 = sort_triangle(self.v2)

            ori1 = (170, 250)
            ori2 = (470, 250)

            draw_triangle(self.v1, ori1, p, surface)
            print_type(self.v1, ori1, surface, self.textRenderer)
            print_area(self.v1, ori1, surface, self.textRenderer)
            draw_triangle(self.v2, ori2, p, surface)
            print_type(self.v2, ori2, surface, self.textRenderer)
            print_area(self.v2, ori2, surface, self.textRenderer)
        else:  # If there is no triangle
            pass

