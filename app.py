from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def send_message_to_js(message):
    socketio.emit('py-js_communication', message)


from modules.renderMaps import render_maps

@app.route('/send_coordinates', methods=['POST'])
def send_coordinates():
    print('Coordinates receiving')
    data = request.json
    coordinates_list = data.get('coordinates_list')
    config = data.get('config')
    

    # print(f'Coordinates received: {coordinates_list}')
    # print(f'Config received: {config}')
    render_maps(coordinates_list, config)
    # send_message_to_js('communication successful')
    
    return jsonify({'status': 'success', 'message': 'Coordinates received successfully'})




if __name__ == '__main__':
    socketio.run(app, debug=False)