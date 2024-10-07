import socket
import json
from datetime import datetime
from pymongo import MongoClient

# Підключення до MongoDB
MONGO_URL = "mongodb://hw06_user:pass_hw06@mongo:27017/"
client = MongoClient(MONGO_URL)
db = client['message_db']
collection = db['messages']

def start_socket_server():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"Socket server started on {UDP_IP}:{UDP_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)  # Отримуємо повідомлення
        message = json.loads(data.decode())
        message['date'] = str(datetime.now())  # Додаємо час отримання повідомлення

        # Збереження повідомлення в MongoDB
        collection.insert_one(message)
        print(f"Message saved to MongoDB: {message}")

if __name__ == '__main__':
    start_socket_server()
