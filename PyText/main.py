import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- THE FRONTEND (Mobile-Optimized) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Live Chat 2026</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body, html { height: 100%; width: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #e5ddd5; }
            
            /* Full screen container */
            .app-container { display: flex; flex-direction: column; height: 100vh; width: 100vw; }

            /* Header */
            .header { background: #075e54; color: white; padding: 15px; text-align: center; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.2); z-index: 10; }
            #my-id { font-size: 0.8rem; font-weight: normal; display: block; opacity: 0.9; }

            /* Messages Area */
            #messages { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 8px; background-image: url('https://user-images.githubusercontent.com/15075759/28719144-86dc0f70-73b1-11e7-911d-60d70fcded21.png'); }
            
            /* Bubble Styles */
            .msg { padding: 8px 12px; border-radius: 8px; max-width: 85%; font-size: 15px; line-height: 1.4; position: relative; box-shadow: 0 1px 1px rgba(0,0,0,0.1); }
            .received { align-self: flex-start; background: white; border-top-left-radius: 0; }
            .self { align-self: flex-end; background: #dcf8c6; border-top-right-radius: 0; }
            .system { align-self: center; background: rgba(0,0,0,0.1); color: #555; font-size: 12px; border-radius: 5px; border: none; box-shadow: none; }
            .username { font-weight: bold; font-size: 11px; color: #27ae60; display: block; margin-bottom: 2px; }

            /* Input Area */
            .input-area { background: #f0f0f0; padding: 10px; display: flex; align-items: center; gap: 10px; border-top: 1px solid #ddd; }
            input { flex: 1; padding: 12px 15px; border: none; border-radius: 25px; outline: none; font-size: 16px; }
            button { background: #128c7e; color: white; border: none; width: 45px; height: 45px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header">
                Global Chat
                <span id="my-id"></span>
            </div>
            <div id="messages"></div>
            <form class="input-area" onsubmit="sendMessage(event)">
                <input type="text" id="messageText" placeholder="Type a message..." autocomplete="off"/>
                <button type="submit">></button>
            </form>
        </div>

        <script>
            let userTag = localStorage.getItem('chat_user_tag') || "User_" + Math.floor(Math.random() * 9000 + 1000);
            localStorage.setItem('chat_user_tag', userTag);
            document.getElementById('my-id').textContent = userTag;

            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const ws = new WebSocket(`${protocol}//${window.location.host}/ws/${userTag}`);
            
            ws.onmessage = function(event) {
                const [sender, ...textParts] = event.data.split(': ');
                const text = textParts.join(': ');
                const messages = document.getElementById('messages');
                const div = document.createElement('div');
                
                if (sender === "System") {
                    div.className = 'msg system';
                    div.textContent = text;
                } else {
                    const isSelf = sender === userTag;
                    div.className = 'msg ' + (isSelf ? 'self' : 'received');
                    div.innerHTML = `<span class="username">${isSelf ? 'You' : sender}</span>${text}`;
                }
                
                messages.appendChild(div);
                messages.scrollIntoView({ behavior: 'smooth', block: 'end' });
                messages.scrollTop = messages.scrollHeight;
            };

            function sendMessage(event) {
                const input = document.getElementById("messageText");
                if (input.value.trim()) {
                    ws.send(input.value);
                    input.value = '';
                }
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""

# --- THE BACKEND (Same logic, simple setup) ---

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    return HTMLResponse(HTML_TEMPLATE)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    await manager.broadcast(f"System: {user_id} joined")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        await manager.broadcast(f"System: {user_id} left")

if __name__ == "__main__":
    import uvicorn
    # 0.0.0.0 is crucial for mobile testing on your Wi-Fi
    uvicorn.run(app, host="0.0.0.0", port=8000)