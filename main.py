import webview
import threading
from screeninfo import get_monitors
from app import app, socketio

def get_screen_resolution():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height

def run_flask():
    socketio.run(app)

def create_webview():
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Create and start the pywebview window
    width, height = get_screen_resolution()
    window = webview.create_window('MapMaker', 'http://127.0.0.1:5000', width=width, height=height)
    # window = webview.create_window('MapMaker', 'http://127.0.0.1:5000', width=1080, height=720)

    webview.start()

if __name__ == '__main__':
    create_webview()
