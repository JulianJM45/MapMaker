from screeninfo import get_monitors

def get_screen_resolution():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height

width, height = get_screen_resolution()
print(f"Screen resolution is {width}x{height}")