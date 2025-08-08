# 1. Нужно создать и активировать виртуальное окружение, в терминале в папке cashFlowProject нужно выполнить:
python -m venv venv
.\venv\scripts\activate

# 2. Нужно установить зависимости из requirements.txt
pip install -r requirements.txt

# 3. База данных
# Я использовала PostgreSQL, для этого нужно зайти в pgAdmin4, создать базу данных cashFlowDb,
# затем нужно исправить поля подключение в cashFlowProject\backend\backend\settings.py, добавив свои данные DATABASES (USER, PASSWORD, HOST, PORT) и сделать миграцию с базой и приминить их для изменения (создания) базы данных
cd backend
python manage.py makemigrations
python manage.py migrate

# 4. Запуск бэкенда
python manage.py runserver

# 5. Запуск фронтенда
python -m http.server 3000

# 6. Откройте 
http://localhost:3000/