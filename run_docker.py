import os
import subprocess
from socket_server import start_socket_server
from init_mongo import initialize_mongo

# Явно вказуємо імена контейнерів
WEB_CONTAINER_NAME = "computer-systems-hw06-web"
SOCKET_SERVER_CONTAINER_NAME = "computer-systems-hw06-socket-server"
MONGO_CONTAINER_NAME = "computer-systems-hw06-mongo"

# Встановлюємо робочу директорію проекту (де розміщений docker-compose.yml)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Отримуємо директорію, де знаходиться цей файл

# Функція для зупинки та видалення всіх контейнерів і обсягів
def remove_all_containers_and_volumes():
    try:
        # Зупинка всіх контейнерів
        subprocess.run(["docker", "stop", WEB_CONTAINER_NAME, SOCKET_SERVER_CONTAINER_NAME, MONGO_CONTAINER_NAME], check=True)
        print("Всі контейнери зупинені.")

        # Видалення всіх контейнерів
        subprocess.run(["docker", "rm", WEB_CONTAINER_NAME, SOCKET_SERVER_CONTAINER_NAME, MONGO_CONTAINER_NAME], check=True)
        print("Всі контейнери видалені.")

        # Видалення всіх обсягів
        subprocess.run(["docker", "volume", "rm", "$(docker", "volume", "ls", "-q)"], shell=True, check=True)
        print("Всі обсяги видалені.")
    
    except Exception as e:
        print(f"Error removing containers and volumes: {e}")

# Функція для запуску Docker Compose
def start_docker_compose(cwd):
    print("Запускаємо docker-compose...")
    subprocess.Popen(["docker-compose", "up", "--build"], cwd=cwd)

# Функція для запуску всіх трьох контейнерів
def run_3_docker():
    # Видалення старих контейнерів та обсягів
    remove_all_containers_and_volumes()

    # Запуск Docker Compose для створення всіх контейнерів
    start_docker_compose(cwd=BASE_DIR)

    # Додаткова логіка для ініціалізації MongoDB
    initialize_mongo()

    # Запуск Socket-сервера
    start_socket_server()

if __name__ == "__main__":
    # Запуск всіх трьох контейнерів
    run_3_docker()

