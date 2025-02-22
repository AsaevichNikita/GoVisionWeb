from fastapi import FastAPI, WebSocket  # Импортируем FastAPI для создания сервера и WebSocket для работы с веб-сокетами
from fastapi.responses import HTMLResponse  # Импортируем HTMLResponse для отправки HTML-страницы
from typing import List  # Импортируем List для работы со списком подключенных клиентов
import uvicorn  # Импортируем uvicorn для запуска сервера

# Создаем приложение FastAPI
app = FastAPI()

# HTML-код для отображения веб-страницы с чатом
html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
</head>
<body>
    <h2>WebSocket Chat</h2>
    <input id="messageInput" type="text" placeholder="Enter message..."/>
    <button onclick="sendMessage()">Send</button>
    <ul id="messages"></ul>
    <script>
        // Устанавливаем соединение WebSocket с сервером
        let ws = new WebSocket("ws://localhost:8000/ws");

        
        // Обработчик получения сообщений
        ws.onmessage = function(event) {
            let li = document.createElement("li");
            li.textContent = event.data;
            document.getElementById("messages").appendChild(li);
        };
        
        // Функция отправки сообщения через WebSocket
        function sendMessage() {
            let input = document.getElementById("messageInput");
            ws.send(input.value);
            input.value = "";
        }
    </script>
</body>
</html>
"""

# Эндпоинт для главной страницы, возвращающий HTML-код
@app.get("/")
async def get():
    return HTMLResponse(html)  # Возвращаем HTML-код клиенту

# Список подключенных клиентов
connected_clients: List[WebSocket] = []

# WebSocket-эндпоинт, который управляет подключением клиентов
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Принимаем WebSocket-подключение
    connected_clients.append(websocket)  # Добавляем клиента в список
    try:
        while True:
            data = await websocket.receive_text()  # Получаем сообщение от клиента
            for client in connected_clients:
                await client.send_text(data)  # Отправляем сообщение всем клиентам
    except:
        connected_clients.remove(websocket)  # Удаляем клиента при разрыве соединения

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Запускаем сервер с uvicorn