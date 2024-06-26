class TransparentWindow:
  """
  A class to create a transparent window.
  """
  def __init__(self, title, x, y, width, height):
    self.hwnd = self.create_window(title, x, y, width, height)
    self.set_transparent(self.hwnd)

  def create_window(self, title, x, y, width, height):
    """
    Creates a transparent window with the specified title, position, and size.
    """
    wndproc = lambda hwnd, msg, wparam, lparam: self.wndproc(hwnd, msg, wparam, lparam)
    wc = win32gui.WNDCLASSEX()
    wc.lpfnWndProc = wndproc
    wc.hInstance = win32api.GetModuleHandle(None)
    wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
    wc.hbrBackground = 0  # Transparent background
    wc.lpszClassName = "TransparentWindow"
    win32gui.RegisterClassEx(wc)

    style = win32con.WS_EX_TOPMOST | win32con.WS_EX_LAYERED 
    style |= win32con.WS_EX_TRANSPARENT | win32con.WS_POPUP
    style |= win32con.WS_VISIBLE

    self.hwnd = win32gui.CreateWindowEx(style, "TransparentWindow", title, 
                                         win32con.WS_OVERLAPPEDWINDOW,
                                         x, y, width, height, 
                                         None, None, wc.hInstance, None)
    return self.hwnd

  def wndproc(self, hwnd, msg, wparam, lparam):
    """
    Window procedure to handle messages.
    """
    if msg == win32con.WM_DESTROY:
      win32gui.PostQuitMessage(0)
      return 0
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

  def set_transparent(self, hwnd):
    """
    Sets the window transparency.
    """
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, 0, 0, win32con.LWA_ALPHA, 255)  # 0-255 for transparency

  def show(self):
    """
    Shows the window.
    """
    win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)

  def destroy(self):
    """
    Destroys the window.
    """
    win32gui.DestroyWindow(self.hwnd)

  def draw_dot(self, x, y, color=(0, 255, 0), size=2):  # Green dot by default
    """
    Draws a dot at the specified coordinates within the window.
    """
    hdc = win32gui.GetDC(self.hwnd)
    win32gui.SetPixel(hdc, x, y, win32api.RGB(color[0], color[1], color[2]))
    win32gui.ReleaseDC(self.hwnd, hdc)


# Replace with your desired pixel coordinates and window size
window_x = 100
window_y = 50
window_width = 50
window_height = 50
dot_x = 25  # Offset within the window
dot_y = 25  # Offset within the window

# Create the transparent window and draw a dot
window = TransparentWindow("
