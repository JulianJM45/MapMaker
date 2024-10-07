import webview
import threading
from screeninfo import get_monitors

from .api import *

def get_screen_resolution():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height



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

    # window = webview.create_window("My Webview App", html=html_content, js_api=api)
    width, height = get_screen_resolution()
    window = webview.create_window("MapMaker", html=html_content, js_api=api, width=width, height=height)

    api.set_Window(window)

    threading.Thread(target=api.print_message).start()
    # threading.Thread(target=api.update_message, args=(apiTest,)).start()

    webview.start()


