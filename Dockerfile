FROM python:3.13-slim

# Устанавливаем переменные среды
ENV HOST=0.0.0.0
ENV PORT=8888

# Устанавливаем рабочую директорию
WORKDIR /ais

# Скопируем файл зависимостей и установим их
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем весь исходный код в контейнер
COPY . /ais

# Открываем порт для приложения
EXPOSE $PORT

# Запускаем приложение
CMD ["sh", "-c", "uvicorn --host $HOST --port $PORT main:app"]