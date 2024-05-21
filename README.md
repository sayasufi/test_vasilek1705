<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Документация по FastAPI-Redis сервису</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #000;
        }
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3, h4, p, code, pre {
            color: #000;
        }
        code {
            background: #eee;
            padding: 2px 5px;
            border-radius: 4px;
        }
        pre {
            background: #eee;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #000;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Документация по FastAPI-Redis сервису</h1>
        <p>Добро пожаловать в сервис FastAPI-Redis! Данный документ содержит полное руководство по использованию и функционалу приложения.</p>
        <h2>Запуск проекта</h2>
        <p>Для запуска проекта вам понадобятся Docker и Docker Compose. Выполните следующие шаги:</p>
        <pre><code>docker-compose up --build</code></pre>
        <p>Команда запустит оба сервиса (FastAPI и Redis) с помощью docker-compose.</p>
        <h2>Использование API</h2>
        <p>После запуска проекта, API будет доступен по адресу <code>http://localhost:8000</code>.</p>
        <h3>Эндпоинты</h3>
        <h4>Запись данных</h4>
        <p>Эндпоинт для записи или обновления номера телефона и адреса в Redis.</p>
        <p><strong>URL:</strong> <code>/write_data/</code></p>
        <p><strong>Метод:</strong> POST</p>
        <p><strong>Пример запроса:</strong></p>
        <pre><code>curl -X POST "http://localhost:8000/write_data/" -H "Content-Type: application/json" -d '{"phone":"89090000000", "address":"123 Main St, Anytown, USA"}'</code></pre>
        <p><strong>Ответ:</strong></p>
        <pre><code>{
    "message": "Данные успешно записаны"
}</code></pre>
        <h4>Получение данных</h4>
        <p>Эндпоинт для получения адреса по номеру телефона из Redis.</p>
        <p><strong>URL:</strong> <code>/check_data/</code></p>
        <p><strong>Метод:</strong> GET</p>
        <p><strong>Пример запроса:</strong></p>
        <pre><code>curl -X GET "http://localhost:8000/check_data/?phone=89090000000"</code></pre>
        <p><strong>Ответ:</strong></p>
        <pre><code>{
    "phone": "89090000000",
    "address": "123 Main St, Anytown, USA"
}</code></pre>
        <h4>Корневой эндпоинт</h4>
        <p>Эндпоинт для проверки работы API. Возвращает приветственное сообщение.</p>
        <p><strong>URL:</strong> <code>/</code></p>
        <p><strong>Метод:</strong> GET</p>
        <p><strong>Пример запроса:</strong></p>
        <pre><code>curl -X GET "http://localhost:8000/"</code></pre>
        <p><strong>Ответ:</strong></p>
        <pre><code>{
    "message": "Добро пожаловать в сервис FastAPI-Redis. Используйте /docs для документации API."
}</code></pre>
        <h2>Структура проекта</h2>
        <p>Структура проекта выглядит следующим образом:</p>
        <pre><code>
├── app/
│   ├── main.py
├── Dockerfile
├── requirements.txt
└── docker-compose.yml</code></pre>
    </div>
</body>
</html>
