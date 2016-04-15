import glfw
from math import sin
import OpenGL.GL as gl
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from numpy import array
from scipy.misc import imread
import ctypes
import time

VERTEXS = array( [
         0.5,  0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,# Top Right
         0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,# Bottom Right
        -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,# Bottom Left
        -0.5,  0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, # Top Left
        ],'f')

INDICES = array([ 0, 1, 3, 1, 2, 3 ], 'I')

VERTEX_SHADERSOURCE = """
    #version 330 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 color;
    layout (location = 2) in vec2 texCoord;
    out vec3 ourColor;
    out vec2 TexCoord;
    void main()
    {
        gl_Position = vec4(position, 1.0);
        ourColor = color;
        TexCoord = texCoord;
    }"""
FRAGMENT_SHADERSOURCE = """
    #version 330 core
    in vec3 ourColor;
    in vec2 TexCoord;
    out vec4 color;
    uniform sampler2D ourTexture;
    void main()
    {
        color = texture(ourTexture, TexCoord)* vec4(ourColor, 1.0f);
    }"""

WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600

def main():
    # Initialize the library
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "OpenGL Example", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_cb)

    vertex_shader = shaders.compileShader(VERTEX_SHADERSOURCE, gl.GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(FRAGMENT_SHADERSOURCE, gl.GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertex_shader, fragment_shader)

    gl.glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    vao = get_vertex(shader)
    tex = bind_texture("wall.png")

    # vertexColorLocation = gl.glGetUniformLocation(shader, "ourColor");
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        gl.glClearColor(0.2, 0.3, 0.3, 0.4)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
        gl.glUseProgram(shader)
        gl.glBindVertexArray(vao);
        gl.glDrawElements(gl.GL_TRIANGLES, INDICES.size, gl.GL_UNSIGNED_INT, None);
        gl.glBindVertexArray(0);
        gl.glUseProgram(0)

        # Swap front and back buffers
        glfw.swap_buffers(window)
        time.sleep(0.05)

    # gl.glDeleteVertexArrays(vao);
    glfw.terminate()

def get_vertex(shader):
    vertex_array_object = gl.glGenVertexArrays(1)
    gl.glBindVertexArray( vertex_array_object )
    _vbo = vbo.VBO(VERTEXS)
    _vbo.bind()
    _ebo = vbo.VBO(INDICES, target = gl.GL_ELEMENT_ARRAY_BUFFER)
    _ebo.bind()
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False,
            8*ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False,
            8*ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(3*ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(1)

    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, False,
            8*ctypes.sizeof(ctypes.c_float),
            ctypes.c_void_p(6*ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(2)

    gl.glBindVertexArray(0)
    gl.glDisableVertexAttribArray(0)
    gl.glDisableVertexAttribArray(1)
    gl.glDisableVertexAttribArray(2)
    _vbo.unbind()
    _ebo.unbind()

    return vertex_array_object

def bind_texture(img_name):
    tex = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR);
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR);
    im = imread(img_name)
    (width, height, _) = im.shape
    image_bytes = im.data.tobytes()
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB,  width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, image_bytes)
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
    return tex

def key_cb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        # print("quit now")
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()

