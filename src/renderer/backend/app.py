from flask import Flask
from flask_socketio import SocketIO
import subprocess
import os
import time
from RunModel import main_func

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
if len(os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tempdata"))) > 0:
    for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tempdata")):
        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tempdata", file))

if len(os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "moretemp"))) > 0:
    for file in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "moretemp")):
        os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), "moretemp", file))



@app.route('/')
def index():
    return "Backend is running"

def background_task():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pythonenv = os.path.join(current_dir, "new_env/Scripts/python.exe")
    script1 = os.path.join(current_dir, "CollectData_1.py")
    script2 = os.path.join(current_dir, "CollectData_2.py")

    try:
        process1 = subprocess.Popen([pythonenv, script1])
        process2 = subprocess.Popen([pythonenv, script2])

        while True:
            if len(os.listdir(os.path.join(current_dir, "tempdata"))) == 2:
                time.sleep(1)
                value = main_func()
                print(f"Emitting value: {value}")
                socketio.emit('update_data', {'value': int(value * 100)})
            time.sleep(0.05)
    except Exception as e:
        print(f"Error in background task: {e}")
        socketio.emit('error', {'message': str(e)})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(background_task)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)