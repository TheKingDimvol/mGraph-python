from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

from controllers.desk import DeskController
from controllers.node import NodeController
from controllers.relationship import RelationshipController
from controllers.type import TypeController
from controllers.typology import TypologyController


class ConnectionManager:
    def __init__(self):
        # {"<UUID доски>": {"<UUID пользователя>": websocket}}
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, desk_uuid: str, user_uuid: str):
        await websocket.accept()

        if desk_uuid not in self.active_connections:
            self.active_connections[desk_uuid] = {}
        self.active_connections[desk_uuid][user_uuid] = websocket

        # При первом подключении будет приходить весь граф на текущий момент

        desk = DeskController.read(desk_uuid)

        nodes = NodeController.read_all(desk_uuid)

        edges = RelationshipController.read(uuid='all', desk=desk_uuid)

        typology_uuid = desk.get('typologyUuid')

        typology = TypologyController.read(typology_uuid)

        types = TypeController.read_all(typology_uuid)

        typology_edges = RelationshipController.read(uuid='all', typology=typology_uuid)

        await websocket.send_json({
            'Desk': desk,
            'Nodes': nodes,
            'Edges': edges,
            'Typology': typology,
            'Types': types,
            'TypeEdges': typology_edges
        })

    def disconnect(self, desk_uuid: str, user_uuid: str):
        users = self.active_connections[desk_uuid]
        del users[user_uuid]
        print(self.active_connections)

    async def graph_changed(self, desk_uuid, new_nodes=None, new_edges=None, deleted_nodes=None, deleted_edges=None):
        if desk_uuid not in self.active_connections:
            return
        for user_uuid, user_ws in self.active_connections[desk_uuid].items():
            await user_ws.send_json({
                'NewNodes': new_nodes,
                'NewEdges': new_edges,
                'DeletedNodes': deleted_nodes,
                'DeletedEdges': deleted_edges
            })


manager = ConnectionManager()
