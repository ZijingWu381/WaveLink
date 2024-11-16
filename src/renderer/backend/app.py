import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Backend is running"

def send_random_data():
    while True:
        value = random.randint(1, 100)
        socketio.emit('update_data', {'value': value})
        time.sleep(5)

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    eventlet.spawn(send_random_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)