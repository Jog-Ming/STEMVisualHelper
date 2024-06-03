import os
import pygame
from math import sin, cos, radians
from gui.widget.ButtonWidget import ButtonWidget
from gui.widget.FloatFieldWidget import FloatFieldWidget
from gui.DrawableHelper import DrawableHelper
from Triangle_check import tri_check, tri_solve, area, tri_n

# maybe put the two functions somewhere else
def draw_triangle(v, ori, p):
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

def print_area(v, ori):
    DrawableHelper.drawText(window, textRenderer, text=f"A: {round(area(v[0], v[1], v[2]), 3)}", x=ori[0] + 50,
                            y=ori[1] + 30, color=(0, 0, 0))


os.environ['SDL_IME_SHOW_UI'] = '1'
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
window_width = screen_width // 2
window_height = screen_height // 2
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('STEM Visual Helper')
clock = pygame.time.Clock()
textRenderer = pygame.font.SysFont(('微软雅黑', 'pingfang'), 12)
FPS = 60
frame = 0

# widget = ButtonWidget.builder('', lambda x: None).position(200, 200).build()


# receiving data ---------------------- start
is_tri = 0 # the number of triangles that can be formed
non_ZERO = 0 # the number of data given

# the following list consists of 6 data: 3 sides and 3 angles
# v[i] and v[i + 3] are corresponding sides and angles
triangles = [] # the list of the float field widget
v = [0, 0, 0, 0, 0, 0] # the list of the data given, AND the final list of the final 6 values of a triangle
v1 = [0, 0, 0, 0, 0, 0] # the list of the final 6 values of the two triangles
v2 = [0, 0, 0, 0, 0, 0]
names = ['a', 'b', 'c', 'A', 'B', 'C'] # the names of the side and angle

for i in range(6):
    triangles.append(FloatFieldWidget(textRenderer, x=40, y=30 + i * 20, width=100, height=20, text="0"))
# ------------------------------------- end

running = True
while running:
    # get data for every frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # widget.mouseClicked(mouse_x, mouse_y, event.button)
            for i in range(6):
                triangles[i].mouseClicked(mouse_x, mouse_y, event.button)

        elif event.type == pygame.KEYDOWN:
            # widget.keyPressed(event.key)
            for i in range(6):
                triangles[i].keyPressed(event.key)

        elif event.type == pygame.TEXTINPUT:
            # widget.charTyped(event.text)
            for i in range(6):
                triangles[i].charTyped(event.text)

    if frame == FPS // 20:
        frame = 0
        # widget.tick()
        for i in range(6):
            triangles[i].tick()

    else:
        frame += 1
    window.fill((255, 255, 255))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # widget.render(window, mouse_x, mouse_y)

    # actual coding of the triangle solver
    # ------------------------------------------- start

    # draw the title
    DrawableHelper.drawText(window, textRenderer, text="Triangle Solver", x=int(window_width / 2) - 50, y=0, color=(0, 0, 0))
    # draw the number of data inputted and triangles possible
    DrawableHelper.drawText(window, textRenderer, text=f"There are {non_ZERO} datas inputted", x=500,y=50, color=(0, 0, 0))
    DrawableHelper.drawText(window, textRenderer, text=f"There is {is_tri} triangles formed", x=500,y=70, color=(0, 0, 0))

    # draw the labels for the sides and angles
    for i in range(6):
        DrawableHelper.drawText(window, textRenderer, f'{names[i]}: ', x=20, y=30+20 * i, color=(0, 0, 0))

    # receive data for sides and angles
    for i in range(6):
        triangles[i].render(window, mouse_x, mouse_y)
    for i in range(6):
        if triangles[i].text:
            v[i] = float(triangles[i].text)
        else:
            v[i] = 0

    # find how many datas are given
    non_ZERO = 0
    for i in range(6):
        if v[i]:
            non_ZERO += 1

    # according to the number of data, find the final values of thr triangle(s)

    if non_ZERO == 3:  # if there is only 3 data, solve the triangle.
        sides = {}
        angles = {}
        for i in range(3):
            if v[i]:
                sides[names[i]] = v[i]
        for i in range(3, 6):
            if v[i]:
                angles[names[i]] = v[i]
        values = tri_solve(sides, angles)

        if values[0] == -1:  # There is no triangle
            is_tri = 0
        elif values[0] == 1e10:  # There is inf triangles
            is_tri = float("inf")
            v = values[1]
        elif len(values) == 2:  # There is two triangles
            is_tri = 2
            v1 = values[0]
            v2 = values[1]
        else:  # There is one triangle
            is_tri = 1
            v = values
    elif non_ZERO == 4 or non_ZERO == 5:  # if there is 4 data, solve the triangle with the first three data, and check
        sides = {}
        angles = {}
        for i in range(3):
            if v[i]:
                sides[names[i]] = v[i]
        for i in range(3, 6):
            if v[i]:
                angles[names[i]] = v[i]
        values = tri_n(sides, angles, non_ZERO)
        if values[0] == -1:
            is_tri = 0
        else:
            is_tri = 1
            v = values
    elif non_ZERO == 6:  # if there is 6 data, make sure the triangle is true.
        is_tri = int(tri_check(v[:3], v[3:]))
    else:  # There is not enough of information to even decide a triangle
        is_tri = 0

    p = 100
    if is_tri == 1 or is_tri == float("inf"):  # if there is only 1 possible triangle or inf triangles
        v = sort_triangle(v)

        ori = (150, 150)
        draw_triangle(v, ori, p)
        print_area(v, ori)
    elif is_tri == 2:  # if there is 2 possible triangles
        v1 = sort_triangle(v1)
        v2 = sort_triangle(v2)

        ori1 = (150, 150)
        ori2 = (300, 150)
        draw_triangle(v1, ori1, p)
        print_area(v1, ori1)
        draw_triangle(v2, ori2, p)
        print_area(v2, ori2)
    else:  # If there is no triangle
        pass

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
