FROM python:3.10

# Робоча директорія всередині контейнера
WORKDIR /app

# Копіюємо файли
COPY . /app

# Встановлюємо залежності
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Збираємо статику
RUN python manage.py collectstatic --noinput

# Порт для запуску (Django через gunicorn)
EXPOSE 8000

# Запуск сервера
CMD ["gunicorn", "restaurant.wsgi:application", "--bind", "0.0.0.0:8000"]