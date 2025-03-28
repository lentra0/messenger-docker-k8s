from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis
import json

app = FastAPI()

# Подключение к Redis
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# SQLAlchemy модели
Base = declarative_base()
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user = Column(String)

# WebSocket соединения
active_connections = []

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = {"user": user_id, "text": data}
            # Сохраняем в Redis и PostgreSQL
            r.publish("chat_channel", json.dumps(message))
            for connection in active_connections:
                await connection.send_text(json.dumps(message))
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/messages")
async def get_messages():
    return {"messages": []}  # Заглушка