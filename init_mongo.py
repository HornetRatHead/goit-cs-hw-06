import os
import time
from pymongo import MongoClient
from datetime import datetime

def initialize_mongo():
    # Підключення до MongoDB із використанням облікових даних
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://hw06_user:pass_hw06@mongo:27017/")
    client = MongoClient(MONGO_URL)

    # Затримка перед підключенням
    time.sleep(10)  # Додаємо затримку на 10 секунд
    
    # Перевірка підключення до MongoDB з повторними спробами
    for attempt in range(5):  # Зробити до 5 спроб підключення
        try:
            client = MongoClient(MONGO_URL)
            # Спробуємо отримати список баз даних
            if 'message_db' in client.list_database_names():
                print("База даних 'message_db' успішно створена або вже існує.")
                break  # Якщо успішно, виходимо з циклу
            else:
                print("База даних 'message_db' не існує. Створюємо нову.")
                break  # Якщо бази даних ще не існує, продовжимо
        except Exception as e:
            print(f"Не вдалося підключитися до MongoDB (спроба {attempt + 1}): {e}. Спробуйте ще раз.")
            time.sleep(5)  # Затримка перед наступною спробою
    else:
        print("Не вдалося підключитися до MongoDB після кількох спроб.")
        exit(1)  # Завершити програму, якщо підключення не вдалося

    # Створення бази даних
    db = client['message_db']
    
    # Створення колекції
    collection = db['messages']
    
    # Перевірка, чи колекція вже існує
    if 'messages' in db.list_collection_names():
        print("Колекція 'messages' успішно створена або вже існує.")
    else:
        # Додавання прикладних даних
        sample_data = [
            {"date": str(datetime.now()), "username": "krabaton", "message": "First message"},
            {"date": str(datetime.now()), "username": "Krabat", "message": "Second message"}
        ]
        
        # Вставка прикладних даних
        collection.insert_many(sample_data)
        print("Прикладні дані успішно додані.")

if __name__ == '__main__':
    initialize_mongo()
