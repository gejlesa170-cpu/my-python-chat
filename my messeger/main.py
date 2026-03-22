from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()
active_connections = []

html_content = """
<!DOCTYPE html>
<html>
    <head><title>Python Chat</title><meta charset="utf-8"></head>
    <body style="font-family: sans-serif; background: #f0f0f0; padding: 20px;">
        <h2>Чат работает!</h2>
        <div id="messages" style="background: white; height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;"></div>
        <input type="text" id="m" placeholder="Сообщение..." style="width: 70%; padding: 10px;">
        <button onclick="send()">OK</button>
        <script>
            let name = prompt("Твое имя:") || "Аноним";
            let ws = new WebSocket("ws://" + window.location.host + "/ws");
            ws.onmessage = (e) => {
                let d = document.getElementById('messages');
                d.innerHTML += '<div><b>' + e.data + '</b></div>';
                d.scrollTop = d.scrollHeight;
            };
            function send() {
                let i = document.getElementById("m");
                if (i.value) { ws.send(name + ": " + i.value); i.value = ''; }
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get(): return HTMLResponse(html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in active_connections: await conn.send_text(data)
    except WebSocketDisconnect: active_connections.remove(websocket)