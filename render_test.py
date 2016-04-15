import glfw
import OpenGL.GL as gl

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_cb)
    
    gl.glViewport(0,0,800,600)
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()

        # Render here, e.g. using pyOpenGL
        gl.glClearColor(0.2, 0.3, 0.3, 0.4)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

def key_cb(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        print("quit now")
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()

