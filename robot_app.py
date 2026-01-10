import os
import signal
import requests
import subprocess
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/launch_bringup', methods=['POST'])
def launch_bringup():
    try:
        subprocess.Popen([
            "gnome-terminal", "--",
            "bash", "-c",
            "echo $$ > /tmp/bringup.pid; ros2 launch omorobot_bringup bringup_launch.py"
        ])
        return "bringup successfully", 200
    except Exception as e:
        return str(e), 500

@app.route('/cancel_bringup', methods=['POST'])
def cancel_bringup():
    try:
        with open('/tmp/bringup.pid', 'r') as f:
            pid = int(f.read().strip())
        os.killpg(os.getpgid(pid), signal.SIGINT)
        os.remove('/tmp/bringup.pid')
        return "bringup terminated", 200
    except Exception as e:
        return str(e), 400

@app.route('/launch_cartographer', methods=['POST'])
def launch_cartographer():
    try:
        subprocess.Popen([
            "gnome-terminal", "--",
            "bash", "-c",
            "echo $$ > /tmp/cartographer.pid; ros2 launch omorobot_cartographer cartographer_launch.py"
        ])
        return "cartographer successfully", 200
    except Exception as e:
        return str(e), 500

@app.route('/cancel_cartographer', methods=['POST'])
def cancel_cartographer():
    try:
        with open('/tmp/cartographer.pid', 'r') as f:
            pid = int(f.read().strip())
        os.killpg(os.getpgid(pid), signal.SIGINT)
        os.remove('/tmp/cartographer.pid')
        return "cartographer terminated", 200
    except Exception as e:
        return str(e), 400

@app.route('/save_map', methods=['POST'])
def save_map():
    try:
        subprocess.Popen([
            "gnome-terminal", "--",
            "bash", "-c",
            "ros2 run nav2_map_server map_saver_cli -f ~/map; echo 'close in 5sec'; sleep 1; echo 'close in 4sec'; sleep 1; echo 'close in 3sec'; sleep 1; echo 'close in 2sec'; sleep 1; echo 'close in 1sec'; sleep 1; exit"
        ])
        return "map save successfully", 200
    except Exception as e:
        return str(e), 500
    
@app.route('/launch_navigation', methods=['POST'])
def launch_navigation():
    try:
        subprocess.Popen([
            "gnome-terminal", "--",
            "bash", "-c",
            "echo $$ > /tmp/navigation.pid; ros2 launch omorobot_navigation2 navigation2_launch.py map:=$HOME/map.yaml; exec bash"
        ])
        return "navigation successfully", 200
    except Exception as e:
        return str(e), 500

@app.route('/cancel_navigation', methods=['POST'])
def cancel_navigation():
    try:
        with open('/tmp/navigation.pid', 'r') as f:
            pid = int(f.read().strip())
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        os.remove('/tmp/navigation.pid')
        return "navigation terminated", 200
    except Exception as e:
        return str(e), 400

remote_server_ip = 'http://192.168.1.119'

@app.route('/launch_teleop', methods=['POST'])
def launch_teleop():
    try:
        requests.post(remote_server_ip + ":9090/launch_teleop", timeout=5)
        return "launch_teleop request sent", 200
    except requests.RequestException as e:
        return f"failed to call remote: {e}", 502

@app.route('/cancel_teleop', methods=['POST'])
def cancel_teleop():
    try:
        requests.post(remote_server_ip + ":9090/cancel_teleop", timeout=5)
        return "cancel_teleop request sent", 200
    except requests.RequestException as e:
        return f"failed to call remote: {e}", 502

@app.route('/launch_cartographer_rviz', methods=['POST'])
def launch_cartographer_rviz():
    try:
        requests.post(remote_server_ip + ":9090/launch_cartographer_rviz", timeout=5)
        return "launch_cartographer_rviz request sent", 200
    except requests.RequestException as e:
        return f"failed to call remote: {e}", 502

@app.route('/cancel_cartographer_rviz', methods=['POST'])
def cancel_cartographer_rviz():
    try:
        requests.post(remote_server_ip + ":9090/cancel_cartographer_rviz", timeout=5)
        return "cancel_cartographer_rviz request sent", 200
    except requests.RequestException as e:
        return f"failed to call remote: {e}", 502

@app.route('/launch_navigation_rviz', methods=['POST'])
def launch_navigation_rviz():
    try:
        requests.post(remote_server_ip + ":9090/launch_navigation_rviz", timeout=5)
        return "launch_navigation_rviz request sent", 200
    except requests.RequestException as e:
        return f"failed to call remote: {e}", 502

@app.route('/cancel_navigation_rviz', methods=['POST'])
def cancel_navigation_rviz():
    try:
        requests.post(remote_server_ip + ":9090/cancel_navigation_rviz", timeout=5)
        return "cancel_navigation_rviz request sent", 200
    except requests.RequestException as e:
        return f"failed to call remote: {e}", 502

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
