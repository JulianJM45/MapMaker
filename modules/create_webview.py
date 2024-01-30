
import webview

from .api import *

# class Api:
#     def send_coordinates(self, coordinates_list, MAP_STYLE, WIDTH, HEIGHT, SCALE, ZOOM, upscale, Overview, AutoZoom, PDF):
#         print("Sending coordinates to Python:", coordinates_list)
#         print("Selected Tile Layer:", MAP_STYLE)



def createWebview(htmlfile, cssfile, jsfile):
    api = Api()

    with open(htmlfile, 'r') as f:
        html_content = f.read()

    # Insert the CSS code into the HTML content
    with open(cssfile, 'r') as f:
        css_content = f.read()
    html_content = html_content.replace('</head>', '<style>\n' + css_content + '\n</style>\n</head>')

    # Insert the JavaScript code into the HTML content
    with open(jsfile, 'r') as f:
        js_content = f.read()
    html_content = html_content.replace('</body>', '<script>\n' + js_content + '\n</script>\n</body>')

    window = webview.create_window("My Webview App", html=html_content, js_api=api)
    # webview.create_window("My Webview App", html=html_content, js_api=api, width=1920, height=1080)
    webview.start()