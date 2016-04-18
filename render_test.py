import ctypes
import time
from math import sin, cos, tan, radians, pi
import glfw
import OpenGL.GL as gl
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from numpy import array
from scipy.misc import imread

VERTEXS = array([
    -0.5, -0.5, -0.5,  0.0, 0.0,
     0.5, -0.5, -0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5,  0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 0.0,

    -0.5, -0.5,  0.5,  0.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 1.0,
    -0.5,  0.5,  0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,

    -0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5, -0.5,  1.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5,  0.5,  1.0, 0.0,

     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5,  0.5,  0.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,

    -0.5, -0.5, -0.5,  0.0, 1.0,
     0.5, -0.5, -0.5,  1.0, 1.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
     0.5, -0.5,  0.5,  1.0, 0.0,
    -0.5, -0.5,  0.5,  0.0, 0.0,
    -0.5, -0.5, -0.5,  0.0, 1.0,

    -0.5,  0.5, -0.5,  0.0, 1.0,
     0.5,  0.5, -0.5,  1.0, 1.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
     0.5,  0.5,  0.5,  1.0, 0.0,
    -0.5,  0.5,  0.5,  0.0, 0.0,
    -0.5,  0.5, -0.5,  0.0, 1.0
    ], 'f')

CUBEPOSITIONS = (
    ( 0.0,  0.0,  0.0), 
    ( 2.0,  5.0, -15.0), 
    (-1.5, -2.2, -2.5),  
    (-3.8, -2.0, -12.3),  
    ( 2.4, -0.4, -3.5),  
    (-1.7,  3.0, -7.5),  
    ( 1.3, -2.0, -2.5),  
    ( 1.5,  2.0, -2.5), 
    ( 1.5,  0.2, -1.5), 
    (-1.3,  1.0, -1.5)  
        )
VERTEX_SHADERSOURCE = """
#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;

out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection*view*model*vec4(position, 1.0f);
    TexCoord = vec2(texCoord.x, 1.0 - texCoord.y);
}"""

FRAGMENT_SHADERSOURCE = """
#version 330 core
in vec2 TexCoord;
out vec4 color;

uniform sampler2D ourTexture1;
uniform sampler2D ourTexture2;

void main()
{
    color = mix(texture(ourTexture1, TexCoord), texture(ourTexture2, TexCoord), 0.2);
}"""

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def init_window():
    # Initialize the library
    if not glfw.init():
        return None

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "OpenGL Example", None, None)
    if not window:
        glfw.terminate()
        return None

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_cb)
    return window

def get_shader():
    vertex_shader = shaders.compileShader(VERTEX_SHADERSOURCE, gl.GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(FRAGMENT_SHADERSOURCE, gl.GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertex_shader, fragment_shader)
    return shader

def main():
    window = init_window()
    if not window:
        return

    shader = get_shader()
    vao = get_vertex()
    tex = bind_texture("wall.png")
    tex2 = bind_texture("wall2.jpg")
    gl.glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    gl.glEnable(gl.GL_DEPTH_TEST)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        render(shader, vao, tex, tex2)

        # Swap front and back buffers
        glfw.swap_buffers(window)
        time.sleep(0.05)

    gl.glDeleteVertexArrays(1, vao)
    glfw.terminate()

def render(shader, vao, tex, tex2):
    gl.glClearColor(0.2, 0.3, 0.3, 0.4)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT)

    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
    gl.glUseProgram(shader)
    gl.glActiveTexture(gl.GL_TEXTURE0)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
    gl.glUniform1i(gl.glGetUniformLocation(shader, "ourTexture1"), 0)
    gl.glActiveTexture(gl.GL_TEXTURE1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex2)
    gl.glUniform1i(gl.glGetUniformLocation(shader, "ourTexture2"), 1)

    view = gl.glGetUniformLocation(shader, "view")
    view_matrix = array([
        [0.8, 0, 0, 0],
        [0, 0.8, 0, 0],
        [0, 0, 0.8, -4],
        [0, 0, 0, 1],
        ])
    gl.glUniformMatrix4fv(view, 1, gl.GL_TRUE, view_matrix)
    projection = gl.glGetUniformLocation(shader, "projection")
    projection_matrix = get_projection_matrix(45, WINDOW_WIDTH/WINDOW_HEIGHT, 0.1, 100)
    gl.glUniformMatrix4fv(projection, 1, gl.GL_FALSE, projection_matrix)
    gl.glBindVertexArray(vao)
    for idx in range(0, len(CUBEPOSITIONS)):
        model = gl.glGetUniformLocation(shader, "model")
        angel = glfw.get_time()%360
        model_matrix = get_model_matrix(idx, angel)
        gl.glUniformMatrix4fv(model, 1, gl.GL_TRUE, model_matrix)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, VERTEXS.size)
    gl.glBindVertexArray(0)
    gl.glUseProgram(0)

def get_projection_matrix(fov, aspect, zN, zF):
    fov = radians(fov/2)
    h = 1.0/tan(fov)
    return array([[h/aspect, 0.0, 0.0, 0.0],
                  [0.0, h, 0.0, 0.0],
                  [0.0, 0.0, (zF+zN)/(zN-zF), -1.0],
                  [0.0, 0.0, 2.0*zF*zN/(zN-zF), 0.0]],
                 'f')

def get_model_matrix(index, angel):
    (x, y, z) = CUBEPOSITIONS[index]
    return array([
        [1, 0, 0, x],
        [0, cos(angel), -sin(angel), y],
        [0, sin(angel), cos(angel), z],
        [0, 0, 0, 1],
        ])

def get_vertex():
    vertex_array_object = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vertex_array_object)
    _vbo = vbo.VBO(VERTEXS)
    _vbo.bind()
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False,
                             5*ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, False,
                             5*ctypes.sizeof(ctypes.c_float),
                             ctypes.c_void_p(3*ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(1)

    gl.glBindVertexArray(0)
    gl.glDisableVertexAttribArray(0)
    gl.glDisableVertexAttribArray(1)
    _vbo.unbind()

    return vertex_array_object

def bind_texture(img_name):
    """
    open image file and use it to generate texture
    """
    tex = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    im = imread(img_name)
    (width, height, _) = im.shape
    image_bytes = im.data.tobytes()
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB,
                    width, height, 0, gl.GL_RGB,
                    gl.GL_UNSIGNED_BYTE, image_bytes)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    return tex

def key_cb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        # print("quit now")
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()

