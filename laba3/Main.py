import glfw
from OpenGL.GL import *
from math import *
import numpy as np
from PIL import Image
#  исправить анимации
#  м
#  текстуры

angleX = 0.0
angleY = 0.0
angleZ = 0.0

k1 = 10
k2 = 10
k3 = 10

scale = 0.7

size = 0.0

radiusOfCircle = 0.5
heightOfConus = [0.5, 1, 0.5]

y = 0

tetta = asin(0.5 / sqrt(2))
phi = asin(0.5 / sqrt(1.75))
# материал конуса
AMBIENT1 = [20 / 255, 55 / 255, 64 / 255, 0.2]
DIFFUSE1 = [38 / 255, 124 / 255, 145 / 255, 0.8]
SPECULAR1 = [208 / 255, 239 / 255, 247 / 255, 0.7]
SHININESS1 = 5
# материал плоскости
AMBIENT2 = [25/ 255, 10/ 255, 48 / 255, 0.2]
DIFFUSE2 = [38 / 255, 124 / 255, 145 / 255, 0.8]
SPECULAR2 = [0.05, 0.05, 0.05, 0.1]
SHININESS2 = 5
# свет конуса
AMBIENT_LIGHT0 = [1, 1, 1, 0.2]
DIFFUSE_LIGHT0 = [1, 1, 1, 0.8]
SPECULAR_LIGHT0 = [0.05, 0.05, 0.05, 0.1]
SHININESS_LIGHT0 = 2
DIRECTION_LIGHT0 = [-1, -1, 1, 0] # 0 - солнце, 1 - лампа
# флаг анимации
animation = False
velocity = 0
gravity = -0.98
lastFrame = 0
minCoord = 0
# флаг определения текстуры
isTexture = False
def vectMult(vect1, vect2):
    arr = [vect1[1] * vect2[2] - vect1[2] * vect2[1],
            vect1[2] * vect2[0] - vect1[0] * vect2[2],
            vect1[0] * vect2[1] - vect1[1] * vect2[0]]
    length = sqrt(arr[0] ** 2 + arr[1] ** 2 + arr[2] ** 2)
    return list(map(lambda a: a / length, arr))

def calcVect(point1, point2):
    return list(map(lambda a, b: b - a, point1, point2))

def makeCircle(k1, k2, k3):
    global radiusOfCircle
    global heightOfConus

    points = []
    normal = []
    textCoord = []
    deltaPhi = ( 2 * pi) / k1
    deltaRadius = radiusOfCircle / k2
    for i in range(k1):
        for j in range(k2):
            p0 = [cos(deltaPhi*i)*deltaRadius*j, 0, sin(deltaPhi*i)*deltaRadius*j]
            p1 = [cos(deltaPhi*i)*deltaRadius*(j+1), 0, sin(deltaPhi*i)*deltaRadius*(j+1)]
            p2 = [cos(deltaPhi*(i+1))*deltaRadius*(j+1), 0, sin(deltaPhi*(i+1))*deltaRadius*(j+1)]
            p3 = [cos(deltaPhi*(i+1))*deltaRadius*(j), 0, sin(deltaPhi*(i+1))*deltaRadius*(j)]
            textCoord.extend([[1 / k1 * i, 1 / k2 * j], [1 / k1 * i, 1 / k2 * (j + 1)], [1 / k1 * (i + 1), 1 / k2 * (j + 1)], [1 / k1 * (i + 1), 1 / k2 * j]])
            points.extend([p0, p1, p2, p3])
            vect1 = calcVect(p2, p3)
            vect2 = calcVect(p2, p1)
            normal.append(vectMult(vect1, vect2))
    for i in range(k1):
        for j in range(k3):
            help1 = [cos(deltaPhi*i)*radiusOfCircle, 0, sin(deltaPhi*i)*radiusOfCircle]
            help2 = [cos(deltaPhi*(i+1))*radiusOfCircle, 0, sin(deltaPhi*(i+1))*radiusOfCircle]
            vectorp1A = list(map(lambda x, y: (x - y) / k3, heightOfConus, help1))
            vectorp2A = list(map(lambda x, y: (x - y) / k3, heightOfConus, help2))
            p0 = list(map(lambda p, vector: p + j*vector, help1, vectorp1A))
            p1 = list(map(lambda p, vector: p + (j+1)*vector, help1, vectorp1A))
            p2 = list(map(lambda p, vector: p + (j+1)*vector, help2, vectorp2A))
            p3 = list(map(lambda p, vector: p + j*vector, help2, vectorp2A))
            textCoord.extend([[1 / k1 * i, 1 / k2 * j], [1 / k1 * i, 1 / k2 * (j + 1)], [1 / k1 * (i + 1), 1 / k2 * (j + 1)], [1 / k1 * (i + 1), 1 / k2 * j]])
            points.extend([p0, p1, p2, p3])
            vect1 = calcVect(p0, p1)
            vect2 = calcVect(p0, p3)
            normal.append(vectMult(vect1, vect2))

    return points, normal, textCoord

points, normal, textCoord = makeCircle(k1, k2, k3)

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
    [0.7, 0, 0, 0],
    [0, 0.7, 0, 0],
    [0, 0, 0.7, 0],
    [0, 0, 0, 1]
])

projectionMatrix = np.matmul(rotateOy(phi), rotateOx(tetta))


def main():
    if not glfw.init():
        return
    window = glfw.create_window(1000, 1050, "lab3", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.STICKY_KEYS, GL_TRUE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    setup()
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def key_callback(window, key, scancode, action, mods):
    global angleZ, angleX, angleY, scale, color, largeMatrixTransform, k1, k2, k3, points, normal, y, animation, velocity, minCoord, textCoord, isTexture
    if action == glfw.REPEAT or action == glfw.PRESS:
        if key == glfw.KEY_D and not animation:
            angleZ -= 0.035
        if key == glfw.KEY_A and not animation:
            angleZ += 0.035
        if key == glfw.KEY_S and not animation:
            angleX += 0.035
        if key == glfw.KEY_W and not animation:
            angleX -= 0.035
        if key == glfw.KEY_Q and not animation:
            angleY += 0.035
        if key == glfw.KEY_E and not animation:
            angleY -= 0.035
        if key == glfw.KEY_F :
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        if key == glfw.KEY_B:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        if key == glfw.KEY_EQUAL:
            k1, k2, k3 = k1 + 1, k2,  k3
        if key == glfw.KEY_MINUS:
            if (k1 == 3 or k2 == 3 or k3 == 3):
                return
            k1, k2, k3 = k1 - 1, k2, k3
        if key == glfw.KEY_X:
            scale = scale * 1.05
        if key == glfw.KEY_Z:
            scale = scale * 0.95
        if key == glfw.KEY_UP and not animation:
            y += 0.01
        if key == glfw.KEY_DOWN and not animation:
            y -= 0.01
        if key == glfw.KEY_ENTER:
            animation = not animation
            if animation:
                velocity = 0
                angleX, angleY, angleZ = 0, 0, 0
        if key == glfw.KEY_SPACE:
            isTexture = not isTexture
    points, normal, textCoord = makeCircle(k1, k2, k3)
    largeMatrixTransform = np.matmul(scaleMatrix(scale), rotateOx(angleX))
    largeMatrixTransform = np.matmul(largeMatrixTransform, rotateOy(angleY))
    largeMatrixTransform = np.matmul(largeMatrixTransform, rotateOz(angleZ))
    largeMatrixTransform = np.matmul(largeMatrixTransform, translateMatrix(0, y, 0))


def draw_ploskost():
    global AMBIENT2, DIFFUSE2, SPECULAR2, SHININESS2
    countPartition = 30

    glBegin(GL_TRIANGLES)
    glMaterialfv(GL_FRONT, GL_AMBIENT, AMBIENT2)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, DIFFUSE2)
    glMaterialfv(GL_FRONT, GL_SPECULAR, SPECULAR2)
    glMaterialfv(GL_FRONT, GL_SHININESS, SHININESS2)

    for i in range(countPartition):
        for j in range(countPartition):
            glNormal3fv([0, 1, 0])
            glVertex3fv([-1 + i * 2 / countPartition, 0, -1 + j * 2 / countPartition])
            glVertex3fv([-1 + (i + 1) * 2 / countPartition, 0, -1 + j * 2 / countPartition])
            glVertex3fv([-1 + i * 2 / countPartition, 0, -1 + (j + 1) * 2 / countPartition])
            glVertex3fv([-1 + i * 2 / countPartition, 0, -1 + (j + 1) * 2 / countPartition])
            glVertex3fv([-1 + (i + 1) * 2 / countPartition, 0, -1 + j * 2 / countPartition])
            glVertex3fv([-1 + (i + 1) * 2 / countPartition, 0, -1 + (j + 1) * 2 / countPartition])
    glEnd()


def draw_circle():
    global points, normal, AMBIENT1, DIFFUSE1, SPECULAR1, SHININESS1, textCoord
    # Левая грань


    glMaterialfv(GL_FRONT, GL_AMBIENT, AMBIENT1)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, DIFFUSE1)
    glMaterialfv(GL_FRONT, GL_SPECULAR, SPECULAR1)
    glMaterialfv(GL_FRONT, GL_SHININESS, SHININESS1)

    if (isTexture):
        glEnable(GL_TEXTURE_2D)
    glBegin(GL_TRIANGLES)
    for i in range(len(points) // 4):
        glNormal3fv(normal[i])
        glTexCoord2fv(textCoord[4 * i])
        glVertex3fv(points[4*i])
        glTexCoord2fv(textCoord[4 * i + 1])
        glVertex3fv(points[4*i+1])
        glTexCoord2fv(textCoord[4 * i + 3])
        glVertex3fv(points[4*i+3])
        glTexCoord2fv(textCoord[4 * i + 3])
        glVertex3fv(points[4*i+3])
        glTexCoord2fv(textCoord[4 * i + 1])
        glVertex3fv(points[4*i+1])
        glTexCoord2fv(textCoord[4 * i + 2])
        glVertex3fv(points[4*i+2])


    glEnd()
    glDisable(GL_TEXTURE_2D)

def getLight():
    global AMBIENT_LIGHT0, DIFFUSE_LIGHT0, SPECULAR_LIGHT0, SHININESS_LIGHT0, DIRECTION_LIGHT0
    glLightfv(GL_LIGHT0, GL_AMBIENT, AMBIENT_LIGHT0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, DIFFUSE_LIGHT0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, SPECULAR_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, DIRECTION_LIGHT0)


def fallFigure(time):
    global velocity, gravity, y, largeMatrixTransform

    d = velocity ** 2 - 2 * gravity * y
    t0 =  max((- velocity + sqrt(d)) / gravity, (- velocity - sqrt(d)) / gravity)

    if time > t0:
        y = 0
        velocity = - (velocity + gravity * t0)
    else:
        y += velocity * time + (gravity * time ** 2) / 2
        velocity += gravity * time


    print(velocity, gravity, y, time)
    largeMatrixTransform = np.matmul(scaleMatrix(scale), rotateOx(angleX))
    largeMatrixTransform = np.matmul(largeMatrixTransform, rotateOy(angleY))
    largeMatrixTransform = np.matmul(largeMatrixTransform, rotateOz(angleZ))
    largeMatrixTransform = np.matmul(largeMatrixTransform, translateMatrix(0, y, 0))

def setup():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_BLEND)
    load_texture()


def load_texture():
    img = Image.open("img.png")
    img_data = np.array(img)

    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

def display(window):
    global size, color, lastFrame, animation
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame
    if animation:
        fallFigure(deltaTime)

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    a, b = glfw.get_framebuffer_size(window)
    glViewport(0, 0, a, b)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1 * a / b, 1 * a / b, -1, 1, -5, 5)
    glMultMatrixd(projectionMatrix)

    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    getLight()
    draw_ploskost()
    glMultMatrixd(largeMatrixTransform)
    glPushMatrix()
    glColor3f(1, 0, 1)
    draw_circle()


    glPopMatrix()

    glfw.swap_buffers(window)
    glfw.poll_events()

main()
