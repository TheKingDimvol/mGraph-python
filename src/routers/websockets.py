from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

from controllers.websocket import ConnectionManager, manager
from src.controllers.auth import AuthController


router = APIRouter(prefix='/ws', tags=['WebSockets'])


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/93abd379-b260-4325-be2c-8384a0b3aaf9?user=1");
            ws.onmessage = function(event) {
                console.log(JSON.parse(event.data))
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
def get():
    return HTMLResponse(html)


@router.websocket("/{desk_uuid}")
async def websocket_endpoint(websocket: WebSocket, desk_uuid: str, user: str = None):
    try:
        print(f'User "{user}" has connected!')
    except Exception as e:
        print(str(e))
        await websocket.accept()
        await websocket.send_json({'error': 'Could not validate token!'})
        await websocket.close()
        return

    await manager.connect(websocket, desk_uuid, user)
    try:
        while True:
            data = await websocket.receive_json()
    except WebSocketDisconnect:
        manager.disconnect(desk_uuid, user)
        print(f"User #{user} closed graph.")
