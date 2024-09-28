📸 Fotogram — Платформа для создания и обмена постами с изображениями
Fotogram — это современная и мощная платформа для обмена изображениями, общения и взаимодействия. Создайте свой пост с текстом и фото, поделитесь им с друзьями и общайтесь в режиме реального времени! В основе системы лежат FastAPI для разработки бэкенда и JavaScript для управления интерактивным фронтендом.

🌟 Основные возможности
🔐 Аутентификация пользователей: Полная поддержка системы регистрации и входа с безопасным управлением токенами.
🖼️ Создание и публикация постов: Публикуйте посты с заголовками, текстом и загружайте изображения.
🖼️ Управление медиафайлами: Поддержка загрузки и хранения нескольких изображений для каждого поста.
💬 Чат в реальном времени: Общайтесь с друзьями и другими пользователями через встроенный чат, сохраняя всю историю сообщений.
🔍 Поиск по контенту: Удобный поиск по постам и сообщениям для быстрого нахождения нужной информации.
🌐 RESTful API: Интуитивно понятный и легко расширяемый API для интеграции и взаимодействия с другими сервисами.
⚡ Документация API: Встроенная документация на базе Swagger, доступная по адресу /docs.
🛠️ Установка и настройка
Клонирование репозитория

Начните с клонирования проекта из GitHub:

bash
Копировать код
git clone https://github.com/stegruslan/fotogram.git
Настройка виртуального окружения

Перейдите в директорию проекта и создайте виртуальное окружение для изоляции зависимостей:

bash
Копировать код
cd fotogram
python -m venv venv
Активируйте виртуальное окружение:

На macOS/Linux:
bash
Копировать код
source venv/bin/activate
На Windows:
bash
Копировать код
venv\Scripts\activate
Установка зависимостей

Установите все необходимые зависимости для запуска бэкенда:

bash
Копировать код
pip install -r requirements.txt
Настройка переменных окружения

Создайте файл .env в корне проекта и добавьте туда следующие параметры:

makefile
Копировать код
SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=ваша_база_данных
SECRET_KEY — это секретный ключ для шифрования JWT токенов.
DATABASE_URL — это путь к базе данных, например, PostgreSQL или SQLite.
Запуск приложения

Запустите сервер FastAPI с автоперезагрузкой для разработки:

bash
Копировать код
uvicorn main:app --reload
Настройка фронтенда

Для отображения статических файлов и HTML страниц перейдите в директорию front:

bash
Копировать код
cd front
Вы можете использовать любой статический сервер, например Nginx, или запускать локальный сервер.

Для разработки:

bash
Копировать код
python -m http.server
Откройте браузер и перейдите по адресу http://localhost:8000, чтобы увидеть фронтенд в действии.

🚀 Использование
После того как вы настроите сервер и фронтенд, вы сможете получить доступ к платформе по адресу http://localhost.

🔑 Аутентификация
Чтобы использовать все функции платформы, пользователь должен зарегистрироваться или войти в систему. Это можно сделать через API или через интерфейс на сайте.

📋 API Эндпоинты
Регистрация пользователя: POST /api/v1/auth/register/
Вход в систему: POST /api/v1/auth/login/
Создание поста: POST /api/v1/posts/create/
Просмотр всех постов: GET /api/v1/posts/
Чат с пользователями: GET /api/v1/chats/
📂 Структура проекта
Проект разделён на два основных компонента: бэкенд и фронтенд. Вот подробное описание структуры директорий:

bash
Копировать код
fotogram/
│
├── backend/
│   ├── app/                # Основная логика приложения FastAPI
│   ├── api/                # Определение маршрутов API и моделей
│   ├── auth/               # Модули аутентификации и управления пользователями
│   ├── media/              # Логика работы с медиафайлами
│   ├── database/           # Модели базы данных и миграции
│   └── main.py             # Точка входа в приложение FastAPI
│
├── front/
│   ├── index.html          # Главная страница сайта
│   ├── chat.html           # Страница чата
│   ├── user.html           # Профиль пользователя и посты
│   ├── style.css           # Стили для всех страниц
│   └── scripts/            # Логика на JavaScript
│
└── media_files/            # Каталог для хранения загруженных изображений
💻 Вклад
Мы приветствуем любой вклад в развитие проекта! Если у вас есть идеи или предложения по улучшению, не стесняйтесь создавать pull requests или оставлять issues в репозитории.