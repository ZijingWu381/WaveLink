from flask import Flask
from flask_socketio import SocketIO
import random
import asyncio
from CollectData_2 import main
import subprocess
import time 
import os
from surfer.main import main

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Backend is running"

def send_random_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    pythonenv = os.path.join(current_dir, "env/Scripts/python.exe")
    # Paths to your scripts
    script1 = os.path.join(current_dir, "CollectData_1.py")
    script2 = os.path.join(current_dir, "CollectData_2.py")

    # Start each script as a separate process
    process1 = subprocess.Popen([pythonenv, script1])
    process2 = subprocess.Popen([pythonenv, script2])

    while True:
        if len(os.listdir(os.path.join(current_dir, "tempdata"))) == 2:
            value = main()
            socketio.emit('update_data', {'value': value})


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