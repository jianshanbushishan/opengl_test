import glfw
from math import sin
import OpenGL.GL as gl
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from numpy import array
import ctypes
import time

VERTEX_SHADERSOURCE = """
    #version 330 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec3 color;
    out vec3 ourColor;
    void main()
    {
    gl_Position = vec4(position, 1.0);
    ourColor = color;
    }"""
FRAGMENT_SHADERSOURCE = """
    #version 330 core
    in vec3 ourColor;
    out vec4 color;
    /*uniform vec4 ourColor;*/
    void main()
    {
    color = vec4(ourColor, 1.0f);
    }"""

def main():
    # Initialize the library
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "OpenGL Example", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_cb)

    vertex_shader = shaders.compileShader(VERTEX_SHADERSOURCE, gl.GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(FRAGMENT_SHADERSOURCE, gl.GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertex_shader, fragment_shader)

    gl.glViewport(0,0,800,600)
    vao = get_vertex(shader)

    # vertexColorLocation = gl.glGetUniformLocation(shader, "ourColor");
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        gl.glClearColor(0.2, 0.3, 0.3, 0.4)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(shader)
        # timeValue = glfw.get_time()
        # greenValue = (sin(timeValue) / 2) + 0.5
        # gl.glUniform4f(vertexColorLocation, 0, greenValue, 0.0, 1.0);
        gl.glBindVertexArray(vao);
        # gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None);
        gl.glBindVertexArray(0);
        gl.glUseProgram(0)

        # Swap front and back buffers
        glfw.swap_buffers(window)
        time.sleep(0.05)

    glfw.terminate()

def get_vertex(shader):
    vertex_array_object = gl.glGenVertexArrays(1)
    gl.glBindVertexArray( vertex_array_object )
    _vbo = vbo.VBO(
        array( [
         0.5,  0.5, 0.0, 1.0, 0.0, 0.0, # Top Right
         0.5, -0.5, 0.0, 0.0, 1.0, 0.0, # Bottom Right
        -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, # Bottom Left
        -0.5,  0.5, 0.0, 0,2, 0,3, 0.6, # Top Left
        ],'f')
        )
    _vbo.bind()
    _ebo = vbo.VBO(
            array([ 0, 1, 2, 1, 2, 3 ], 'I'),
            target = gl.GL_ELEMENT_ARRAY_BUFFER
            )
    _ebo.bind()
    position = gl.glGetAttribLocation(shader, 'position')
    gl.glVertexAttribPointer(position, 3, gl.GL_FLOAT, False, 6*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(position)

    color = gl.glGetAttribLocation(shader, 'color')
    gl.glVertexAttribPointer(color, 3, gl.GL_FLOAT, False, 6*ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3*ctypes.sizeof(ctypes.c_float)))
    gl.glEnableVertexAttribArray(color)

    gl.glBindVertexArray(0)
    gl.glDisableVertexAttribArray(position)
    _vbo.unbind()
    _ebo.unbind()

    return vertex_array_object

def key_cb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        # print("quit now")
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()

