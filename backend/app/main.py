from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
from typing import Dict, List
import json
import asyncio

app = FastAPI()

# Хранилище в памяти
active_connections = []
message_history = []
MAX_HISTORY = 100  # Лимит сообщений

class ConnectionManager:
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        active_connections.append(websocket)
        await self.send_history(websocket)

    async def send_history(self, websocket: WebSocket):
        """Отправляем последние сообщения новому пользователю"""
        if message_history:
            await websocket.send_text(json.dumps({
                "type": "history",
                "data": message_history[-MAX_HISTORY:]
            }))

    async def broadcast(self, message: Dict):
        """Рассылаем сообщение всем"""
        message_str = json.dumps(message)
        for connection in active_connections:
            await connection.send_text(message_str)

    def disconnect(self, websocket: WebSocket):
        if websocket in active_connections:
            active_connections.remove(websocket)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_handler(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    try:
        while True:
            message_text = await websocket.receive_text()

            # Формируем сообщение
            message = {
                "text": message_text,
                "user": username,
                "time": datetime.now().isoformat()
            }

            # Сохраняем и рассылаем
            message_history.append(message)
            if len(message_history) > MAX_HISTORY:
                message_history.pop(0)

            await manager.broadcast({
                "type": "message",
                "data": message
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "user_left",
            "data": f"{username} покинул чат"
        })

@app.get("/health")
async def health_check():
    return {"status": "OK", "connections": len(active_connections)}

@app.get("/")
async def root():
    return {
        "message": "WebSocket Chat Backend",
        "endpoints": {
            "websocket": "/ws/{username}",
            "health_check": "/health"
        }
    }
