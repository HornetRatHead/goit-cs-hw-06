import os
from pathlib import Path
import json
import uvicorn
from datetime import datetime
import docker
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from socket_server import start_socket_server
from init_mongo import initialize_mongo
from run_docker import start_docker_compose

app = FastAPI()

# Встановлюємо шлях до директорії front-init для HTML-шаблонів
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "front-init")

# Шлях до файлу data.json у теці storage
DATA_FILE = BASE_DIR / "front-init/storage/data.json"

# Функція для відправки даних на Socket-сервер (UDP)
def send_to_socket_server(data):
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(data).encode(), (UDP_IP, UDP_PORT))

# Маршрут для головної сторінки index.html
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Маршрут для сторінки message.html
@app.get("/message.html", response_class=HTMLResponse)
async def message_html(request: Request):
    return templates.TemplateResponse("message.html", {"request": request})

# Обробка POST-запиту з форми message.html
@app.post("/message")
async def handle_message(username: str = Form(...), message: str = Form(...)):
    data = {
        "username": username,
        "message": message,
        "date": str(datetime.now())  # Додаємо час отримання повідомлення
    }

    # Відправка даних через сокет
    try:
        send_to_socket_server(data)  # Виклик функції для відправки даних
        return {"status": "Message sent to socket server"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send message to socket server")

# Обробка файлу logo.png 
@app.get("/logo.png")
async def serve_logo():
    logo_path = BASE_DIR / "front-init" / "logo.png"
    return FileResponse(logo_path)

# Обробка файлу style.css 
@app.get("/style.css")
async def serve_style():
    style_path = BASE_DIR / "front-init" / "style.css"
    return FileResponse(style_path)

# Читання даних з файлу data.json
@app.get("/data")
async def get_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
        return {"data": data}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON data")

# Обробка помилки 404, повернення сторінки error.html
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("error.html", {"request": request}, status_code=404)
    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)

if __name__ == "__main__":
    
    container_name = "web_socket_container"  # Назва контейнера

    # Поточна директорія проекту
    cwd = BASE_DIR  
    
    start_docker_compose(container_name, cwd=BASE_DIR)

    initialize_mongo()
    
    # Запускаємо Socket-сервер
    start_socket_server()

    # Запускаємо FastAPI-додаток
    uvicorn.run(app, host="0.0.0.0", port=3000)
