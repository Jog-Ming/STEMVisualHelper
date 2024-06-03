import os
import pygame
from math import sin, cos, radians
from gui.widget.ButtonWidget import ButtonWidget
from gui.widget.FloatFieldWidget import FloatFieldWidget
from gui.DrawableHelper import DrawableHelper
from Triangle_check import tri_check, tri_solve, area

def draw_triangle(v, ori, p):
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
    v_s = v[:3]
    v_a = v[3:]
    v_s.sort(reverse=True)
    v_a.sort(reverse=True)
    v = v_s + v_a
    return v

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

#widget = ButtonWidget.builder('', lambda x: None).position(200, 200).build()

# receiving data
is_tri = 0
non_ZERO = 0
triangles = []
v = [0, 0, 0, 0, 0, 0]
v1 = [0, 0, 0, 0, 0, 0]
v2 = [0, 0, 0, 0, 0, 0]
names = ['a', 'b', 'c', 'A', 'B', 'C']

for i in range(6):
    triangles.append(FloatFieldWidget(textRenderer, x=40, y=30 + i * 20, width=100, height=20, text="0"))
# end here

running = True
while running:
    # get data for every frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            #widget.mouseClicked(mouse_x, mouse_y, event.button)
            for i in range(6):
                triangles[i].mouseClicked(mouse_x, mouse_y, event.button)

        elif event.type == pygame.KEYDOWN:
            #widget.keyPressed(event.key)
            for i in range(6):
                triangles[i].keyPressed(event.key)

        elif event.type == pygame.TEXTINPUT:
            #widget.charTyped(event.text)
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

    # actual coding
    # -----------------------------------------------------------------------


    # draw the title
    DrawableHelper.drawText(window, textRenderer, text="Triangle Solver", x=int(window_width / 2) - 50, y=0, color=(0, 0, 0))
    # draw the number of data inputted
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

    # Process the data
    non_ZERO = 0
    for i in range(6):
        if v[i]:
            non_ZERO += 1
            #print(v[i], end=" ")
    #print()


    # if there is only 3 data, solve the triangle.
    if (non_ZERO == 3):
        sides = {}
        angles = {}
        for i in range(3):
            if v[i]:
                sides[names[i]] = v[i]
        for i in range(3, 6):
            if v[i]:
                angles[names[i]] = v[i]
        values = tri_solve(sides, angles)
        if values[0] == -1:
            is_tri = 0
        elif values[0] == 1e10:
            is_tri = float("inf")
            v = values[1]
        elif len(values) == 2:
            is_tri = 2
            v1 = values[0]
            v2 = values[1]
        else:
            is_tri = 1
            v = values

    # if there is 6 data, make sure the triangle is true.
    elif non_ZERO == 6:
        is_tri = int(tri_check(v[:3], v[3:]))
    # print(is_tri)

    else:
        is_tri = 0

    if is_tri == 1: # if there is only 1 possible triangle
        v = sort_triangle(v)

        p = 100
        ori = (150, 150)
        draw_triangle(v, ori, p)
        DrawableHelper.drawText(window, textRenderer, text=f"A: {round(area(v[0], v[1], v[2]), 3)}", x=ori[0] + 50, y=ori[1] + 30, color=(0, 0, 0))
    elif is_tri == float("inf"):
        v = sort_triangle(v)

        p = 100
        ori = (150, 150)
        draw_triangle(v, ori, p)
    elif is_tri == 2: # if there is 2 possible triangles
        v1 = sort_triangle(v1)
        v2 = sort_triangle(v2)

        p = 100
        ori1 = (150, 150)
        ori2 = (300, 150)
        draw_triangle(v1, ori1, p)
        DrawableHelper.drawText(window, textRenderer, text=f"A: {round(area(v1[0], v1[1], v1[2]), 3)}", x=ori1[0], y=ori1[1] + 30, color=(0, 0, 0))
        draw_triangle(v2, ori2, p)
        DrawableHelper.drawText(window, textRenderer, text=f"A: {round(area(v2[0], v2[1], v2[2]), 3)}", x=ori2[1], y=ori2[1] + 30, color=(0, 0, 0))
    else:
        pass

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
