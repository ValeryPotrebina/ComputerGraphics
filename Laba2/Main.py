import glfw
from OpenGL.GL import *
from math import *
import numpy as np
import random

angleX = 0.0
angleY = 0.0
angleZ = 0.0
scale = 1
size = 0.3

tetta = asin(0.5 / sqrt(2))
phi = asin(0.5 / sqrt(1.75))


def rotateOx(tetta):
    return np.array([
        [1, 0, 0, 0],
        [0, cos(tetta), sin(tetta), 0],
        [0, -sin(tetta), cos(tetta), 0],
        [0, 0, 0, 1]])


def rotateOy(tetta):
    return np.array([
        [cos(tetta), 0, -sin(tetta), 0],
        [0, 1, 0, 0],
        [sin(tetta), 0, cos(tetta), 0],
        [0, 0, 0, 1]
    ])


def rotateOz(tetta):
    return np.array([
        [cos(tetta), sin(tetta), 0, 0],
        [-sin(tetta), cos(tetta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]])


def scaleMatrix(scale):
    return np.array([
        [scale, 0, 0, 0],
        [0, scale, 0, 0],
        [0, 0, scale, 0],
        [0, 0, 0, 1],
    ])


def translateMatrix(x, y, z):
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [x, y, z, 1]
    ])


largeMatrixTransform = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

projectionMatrix = np.matmul(rotateOy(phi), rotateOx(tetta))
# projectionMatrix = largeMatrixTransform
smallMatrix = np.matmul(translateMatrix(-0.7, 1.4, 0), scaleMatrix(0.5))


def main():
    if not glfw.init():
        return
    window = glfw.create_window(700, 750, "Lab2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global angleZ, angleX, angleY, scale, color, largeMatrixTransform
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            angleZ -= 0.035
        if key == glfw.KEY_LEFT:
            angleZ += 0.035
        if key == glfw.KEY_DOWN:
            angleX += 0.035
        if key == glfw.KEY_UP:
            angleX -= 0.035
        if key == glfw.KEY_D:
            angleY += 0.035
        if key == glfw.KEY_A:
            angleY -= 0.035
        if key == glfw.KEY_F:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if key == glfw.KEY_B:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if key == glfw.KEY_EQUAL:
            scale = scale * 1.05
        if key == glfw.KEY_MINUS:
            scale = scale * 0.95  # scale rotate translate
    largeMatrixTransform = np.matmul(scaleMatrix(scale), rotateOx(angleX))
    largeMatrixTransform = np.matmul(largeMatrixTransform, rotateOy(angleY))
    largeMatrixTransform = np.matmul(largeMatrixTransform, rotateOz(angleZ))


def draw_cube():
    # Левая грань (по часовой - бек, против часовой - френт)
    glBegin(GL_POLYGON)
    glColor3f(0, 1, 0)

    # Green right
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(-size, -size, size)

    glEnd()

    # Правая грань
    glBegin(GL_POLYGON)
    # glColor3f(*color)
    glColor3f(1, 0, 0)
    glVertex3f(size, -size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)
    glEnd()

    # Нижняя грань
    glBegin(GL_POLYGON)
    # glColor3f(*color)
    glColor3f(0, 0, 1)

    # Right blue
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, -size, size)
    glVertex3f(size, -size, size)
    glVertex3f(size, -size, -size)
    glEnd()

    # Верхняя грань
    glBegin(GL_POLYGON)
    # glColor3f(*color)
    glColor3f(1, 1, 0)

    # Yellow right
    glVertex3f(-size, size, -size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, size, -size)

    glEnd()

    # Задняя грань
    glBegin(GL_POLYGON)
    # glColor3f(*color)
    glColor3f(1, 0, 1)

    # pURPLE RIGHT
    glVertex3f(-size, -size, -size)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, -size, -size)
    glEnd()

    # Передняя грань
    glBegin(GL_POLYGON)
    # glColor3f(*color)
    glColor3f(0.4, 0.5, 0)

    # Black Right
    glVertex3f(-size, -size, size)
    glVertex3f(-size, size, size)
    glVertex3f(size, size, size)
    glVertex3f(size, -size, size)

    glEnd()


def display(window):
    global size, color
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    a, b = glfw.get_framebuffer_size(window)
    glViewport(0, 0, a, b)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1 * a / b, 1 * a / b, -1, 1, -5, 5)
    glMultMatrixd(projectionMatrix)

    glMatrixMode(GL_MODELVIEW)

    # Статичный куб

    glLoadIdentity()
    glMultMatrixd(smallMatrix)
    glColor3f(1, 0, 0)
    draw_cube()

    # Двигающийся куб

    glLoadIdentity()
    glMultMatrixd(largeMatrixTransform)
    glPushMatrix()
    glColor3f(1, 0, 1)
    draw_cube()

    glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()


main()
