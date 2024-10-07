from screeninfo import get_monitors


coordiantes = [{'Northwest': [47.524726012174284, 10.993590706828368], 'SouthEast': [47.479509900531426, 11.08933115577387]}]

def get_screen_resolution():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height

width, height = get_screen_resolution()
print(f"Screen resolution is {width}x{height}")