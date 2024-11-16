from flask import Flask
from flask_socketio import SocketIO
import random
import asyncio
from CollectData import main

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Backend is running"

async def send_random_data():
    asyncio.create_task(main())
    while True:
        value = random.randint(1, 100)
        socketio.emit('update_data', {'value': value})
        await asyncio.sleep(5)

def start_send_random_data():
    asyncio.run(send_random_data())

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(start_send_random_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)