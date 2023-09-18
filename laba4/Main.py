import glfw
from OpenGL.GL import *
from math import *
import numpy as np


pixelsize = 700
pixels = [0] * pixelsize * pixelsize


points = []

matrixAntiAliasing = [[1]*3 for _ in range(3)]
cursorX, cursorY = 0, 0


DRAW_BEGIN = 0
DRAW_END = 1
FILL = 2

isAntiAliasing = False

stage = DRAW_BEGIN

x, y = 0, 0

viewSize = 0


for i in range(10, 20):
    for j in range(10, 200):
        pixels[i*pixelsize + j] = 1


def main():
    if not glfw.init():
        return
    window = glfw.create_window(500, 500, "lab4", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

def key_callback(window, key, scancode, action, mods):
    global stage, isAntiAliasing
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_SPACE:
            if stage == FILL:
                stage = DRAW_END
            elif stage == DRAW_END:
                stage = FILL
        if key == glfw.KEY_ENTER:
            isAntiAliasing = not isAntiAliasing



def mouse_callback(window, button, action, mods):
    global x, y, stage, points
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        print(x, y)
        if stage == DRAW_BEGIN:
            points.append([x, y])
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        if stage == DRAW_BEGIN:
            points.append([x, y])
            stage = DRAW_END
            fillFigure()
        else:
            points = []
            stage = DRAW_BEGIN


def cursor_position_callback(window, xpos, ypos):
    global x, y, viewSize, pixelsize
    # передаем в переменные координаты позиции мыши
    x = xpos / viewSize * pixelsize
    y = ypos / viewSize * pixelsize


def fillFigure():
    global pixelsize, pixels
    pixels = [0] * pixelsize * pixelsize
    lines = [[] for _ in range(pixelsize)]
    edges = makeEdges(points)
    for edge in edges:
        if edge[0][1] == edge[1][1]:
            continue
        yMinIndex = 0 if edge[0][1] < edge[1][1] else 1
        x = lambda y: (((y - edge[0][1])*(edge[1][0] - edge[0][0])) / (edge[1][1] - edge[0][1])) + edge[0][0]
        for i in range(edge[yMinIndex][1], edge[(yMinIndex + 1) % 2][1] ):
            lines[i].append(round(x(i)))

    for line in lines:
        line.sort()
    for i in range(len(lines)):
        for k in range(len(lines[i]) // 2):
            for j in range(lines[i][2*k], lines[i][2*k+1] + 1):
                pixels[i * pixelsize + j] = 1



def antiAliasing(arr, width, height, AAMatrix):
    AAwidth = len(AAMatrix)
    AAheight = len(AAMatrix[0])
    res = [0] * width * height
    for i in range(width):
        for j in range(height):
            sum = 0
            weight = 0
            for ii in range(AAwidth):
                for jj in range(AAheight):
                    currX = i+ii-AAwidth//2
                    currY = j+jj-AAheight//2
                    if 0 <= currX < width and 0 <= currY < height:
                        sum += arr[width*currX + currY]*AAMatrix[ii][jj]
                        weight += AAMatrix[ii][jj]
            sum /= weight
            res[i * width + j] = sum
    return res



def makeEdges(points):
    edges = []
    for i in range(len(points)):
        if i == (len(points) - 1):
            edges.append([points[i], points[0]])
            continue
        edges.append([points[i], points[i+1]])
    for edge in edges:
        for point in edge:
            for i in range(len(point)):
                point[i] = int(point[i])
        print(edge)

    return edges




def display(window):
    global pixelsize, stage, matrixAntiAliasing, viewSize
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    width, height = glfw.get_framebuffer_size(window)
    viewSize = height if height > width else width
    glViewport(0, height - viewSize, viewSize, viewSize)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, pixelsize, pixelsize, 0, 0, 1)
    zoom = viewSize / pixelsize
    # glPixelZoom - увеличивает и уменьшает пиксели
    glPixelZoom(zoom, -zoom)
    # glRasterPos2f - показывает откуда нужно начинать рисовать
    glRasterPos2f(0, 0)

    if stage == DRAW_END or stage == DRAW_BEGIN:
        if len(points) > 0:
            glBegin(GL_LINE_LOOP)
            for point in points:
                glColor3f(0, 0, 1)
                glVertex2fv(point)
            if stage == DRAW_BEGIN:
                glVertex2f(x, y)
            glEnd()
    else:
        glDrawPixels(pixelsize, pixelsize, GL_BLUE, GL_FLOAT, antiAliasing(pixels, pixelsize, pixelsize, matrixAntiAliasing) if isAntiAliasing else pixels)
    # swap_buffers and poll_events have to be in the end of display
    glfw.swap_buffers(window)
    glfw.poll_events()


main()
