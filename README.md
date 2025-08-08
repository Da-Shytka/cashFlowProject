# CashFlow Project - Полное руководство по запуску

## Содержание
1. [Клонирование репозитория](#1-клонирование-репозитория)
2. [Настройка виртуального окружения](#2-настройка-виртуального-окружения)
3. [Установка зависимостей](#3-установка-зависимостей)
4. [Настройка базы данных](#4-настройка-базы-данных)
5. [Запуск backend](#5-запуск-backend)
6. [Запуск frontend](#6-запуск-frontend)
7. [Приложение](#7-приложение)

---

## 1. Клонирование репозитория
Получение исходного кода проекта на ваш компьютер:

```bash
git clone https://github.com/Da-Shytka/cashFlowProject.git
```
```bash
cd cashFlowProject
```

---
## 2. Настройка виртуального окружения
Создание изолированной среды для Python:
```bash
python -m venv venv
```
Активация:
```bash
.\venv\scripts\activate
```

---
## 3. Установка зависимостей
Установка всех необходимых библиотек:
```bash
pip install -r requirements.txt
```

---
## 4. Настройка базы данных
Я использовала PostgreSQL, для этого нужно зайти в pgAdmin4, создать базу данных cashFlowDb, затем нужно исправить поля подключение в cashFlowProject\backend\backend\settings.py, добавив свои данные DATABASES (USER, PASSWORD, HOST, PORT) и сделать миграцию с базой и приминить их для изменения (создания) базы данных
```bash
cd backend
```
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

---
## 5. Запуск backend
Из папки backend
```bash
cd backend
```
```bash
python manage.py runserver
```

---
## 6. Запуск frontend
Открыть второй терминал, из папки frontend
```bash
cd ..
```
```bash
cd frontend
```
```bash
python -m http.server 3000
```

---
## 7. Приложение
Сделан swagger
```bash
http://127.0.0.1:8000/api/docs/swagger/

```
А вот и само приложение
```bash
http://localhost:3000/

```