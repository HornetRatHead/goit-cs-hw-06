# Використовуємо Python 3.9 як базовий образ
FROM python:3.9-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл залежностей (requirements.txt)
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли сокет-сервера до контейнера
COPY . .

# Відкриваємо порт 5000 для сокет-сервера
EXPOSE 5000

# Запуск веб-сервера з uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
