import glfw
from OpenGL.GL import *
import math
from PIL import Image

delta = 0.1
angle = 0.0
deltax = 0.0
deltay = 0.0
posx = 0.0
posy = 0.0
size = 0.0
alfa = 0
beta = 0
a = 0.6
b = 0.6
c = 0.6
flag = False

diffCoef=0
ambCoef=0
specCoef=0

staks=100
slices = 100
position=[]
normals=[]
text=[]
radiusX=1
radiusY=0.7
radiusZ=0.7
down=False
v0=0
h0=0
g = 0.0051


def main():
    if not glfw.init():
        return
    window = glfw.create_window(800, 800, "Lab8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


def light():
    """diffuseLight = (0.7+diffCoef, 0.7+diffCoef, 0.7+diffCoef, 0.7+diffCoef)
    ambientLight = (0+ambCoef, 0+ambCoef, 0+ambCoef, 1+ambCoef)
    specular = (1.0+specCoef, 1.0+specCoef, 1.0+specCoef, 1.0+specCoef)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.5, 0.7, 0, 1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)

    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 70)
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 70)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [-0.5, -0.5, -0.5])

    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)"""



    vertex = create_shader(GL_VERTEX_SHADER, """
    varying vec3 n;
    varying vec3 v;
    varying vec2 uv;
    out vec4 vertexColor;
    void main()
    {   
        uv = gl_MultiTexCoord0.xy;
        v = vec3(gl_ModelViewMatrix * gl_Vertex);
        n = normalize(gl_NormalMatrix * gl_Normal);
        gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0;
        gl_Position = ftransform();
        vertexColor = vec4(0.5f, 0.0f, 1.0f, 1.0f);
    }
    """)

    fragment = create_shader(GL_FRAGMENT_SHADER, """
    varying vec3 n;
    varying vec3 v; 
    uniform sampler2D tex;
    in vec4 vertexColor; // Входная переменная из вершинного шейдера (то же название и тот же тип)

    out vec4 color;
    void main ()  
    {  
        vec3 L = normalize(gl_LightSource[0].position.xyz - v);   
        vec3 E = normalize(-v);
        vec3 R = normalize(-reflect(L,n));  

        //calculate Ambient Term:  
        vec4 Iamb = gl_FrontLightProduct[0].ambient;    

        //calculate Diffuse Term:  
        vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 0.0);
        Idiff = clamp(Idiff, 1.5, 1.0);     

        // calculate Specular Term:
        vec4 Ispec = gl_LightSource[0].specular 
                        * pow(max(dot(R,E),0.0),0.3);
        Ispec = clamp(Ispec, 1.0, 1.0); 

        vec4 texColor = texture2D(tex, gl_TexCoord[0].st);
        gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
        //vec4 texColor = vec4(0.5f, 0.texColor0f, 0.0f, 1.0f);
        //gl_FragColor = (Idiff + Iamb + Ispec) * vertexColor;
    }
    """)


    program = glCreateProgram()

    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)

    glUseProgram(program)


def texture():
    glColorMaterial(GL_FRONT,GL_AMBIENT)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    image = Image.open("img.png")
    w = image.width
    h = image.height
    img_data = image.convert("RGBA").tobytes()

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL) #GL_REPLACE)

    glEnable(GL_NORMALIZE)


def display(window):
    sizeX, sizeY = 800, 800
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0,0,0,0)
    glViewport(0, 0, sizeX, sizeY)

    glPushMatrix()
    if flag:
        glEnable(GL_TEXTURE_2D)
    else:
        glDisable(GL_TEXTURE_2D)

    rotx = (1, 0, 0, 0,
            0, math.cos(alfa), -math.sin(alfa), 0,
            0, math.sin(alfa), math.cos(alfa), 0,
            0, 0, 0, 1)

    roty = (math.cos(beta), 0, math.sin(beta), 0,
            0, 1, 0, 0,
            -math.sin(beta), 0,  math.cos(beta), 0,
            0, 0, 0, 1)
    scaling = (a, 0, 0, 0,
               0, b, 0, 0,
               0, 0, c, 0,
               0, 0, 0, 1)

    glMultMatrixd(roty)
    glMultMatrixd(rotx)
    glMultMatrixd(scaling)
    
    glBegin(GL_TRIANGLE_STRIP);
    global v0, h0

    if down:
        h0+=v0
        v0-=g
        if h0<= -1 or h0>1:
            v0=-1*v0


    for i in range (int(staks/2)):
        theta1=i*2*math.pi/staks-(math.pi/2)
        theta2=(i+1)*2*math.pi/staks-(math.pi/2)
        for j in range (slices):
            theta3=j*2*math.pi/slices

            ex=math.cos(theta2)*math.cos(theta3)
            ey=math.sin(theta2)
            ez=math.cos(theta2)*math.sin(theta3)
            px=radiusX*ex
            py=radiusY*ey+h0
            pz=radiusZ*ez
            glNormal3f(ex,ey,ez)
            glColor3f(0.5, 0.0, 0.5)
            glTexCoord2f(-(j/slices), (2*(i+1)/slices))
            glVertex3f(px, py, pz)

            ex=math.cos(theta1)*math.cos(theta3)
            ey=math.sin(theta1)
            ez=math.cos(theta1)*math.sin(theta3)
            px=radiusX*ex
            py=radiusY*ey+h0
            pz=radiusZ*ez
            glNormal3f(ex,ey,ez)
            glColor3f(0.5, 0.0, 0.5)
            glTexCoord2f(-(j/slices), (2*i/slices))
            glVertex3f(px, py, pz)

    glEnd()
    glPopMatrix()

    light()

    texture()
    glfw.swap_buffers(window)
    glfw.poll_events()

def create_shader(stype, source):
    shader=glCreateShader(stype)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader

def key_callback(window, key, scancode, action, mods):
    global a, b, c, flag, alfa, beta, staks, slices, diffCoef, ambCoef, specCoef, down
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            beta += 0.17
        if key == glfw.KEY_LEFT:  # glfw.KEY_LEFT
            beta += -0.17
        if key == glfw.KEY_UP:
            alfa += 0.17
        if key == glfw.KEY_DOWN:
            alfa += -0.17
        if key == 32:  # space
            flag = not flag
        if key == 87:  # w
            staks+=10
            slices+=10
        if key == 83:  # s
            staks-=10
            slices-=10
        if key == glfw.KEY_L:
            diffCoef+=1
        if key == glfw.KEY_K:
            diffCoef-=1
        if key == glfw.KEY_Q:
            a-=0.05
            b-=0.05
            c-=0.05
        if key == glfw.KEY_E:
            a+=0.05
            b+=0.05
            c+=0.05
        if key == glfw.KEY_P:
            ambCoef+=1
        if key == glfw.KEY_O:
            ambCoef-=1
        if key == glfw.KEY_M:
            specCoef+=0.5
        if key == glfw.KEY_N:
            specCoef-=0.5
        if key == glfw.KEY_G:
            down = not down
                


if __name__ == "__main__":
    main()
