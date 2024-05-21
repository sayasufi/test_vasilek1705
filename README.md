<!DOCTYPE html>
<html lang="ru">
<body>
    <div class="container">
        <h1>Задание 1. Документация по FastAPI-Redis сервису</h1>
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
<h1>Задание 2. Решение задачи по переносу данных в СУБД Postgres</h1>
    <p>У нас есть две таблицы в базе данных Postgres:</p>
    <ul>
        <li><strong>short_names</strong> с 700,000 записями, содержащая имена файлов без расширений и их статус.</li>
        <li><strong>full_names</strong> с 500,000 записями, содержащая имена файлов с расширениями.</li>
    </ul>
    <p>Необходимо перенести статус файлов из таблицы <strong>short_names</strong> в таблицу <strong>full_names</strong> с минимальным количеством запросов и за максимально короткое время. Рассмотрим два варианта решения задачи.</p>
    <h2>Вариант 1: Использование UPDATE с подзапросом</h2>
    <pre><code>
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE full_names.name LIKE short_names.name || '%';
    </code></pre>
    <p><strong>Объяснение:</strong></p>
    <ul>
        <li>Запрос обновляет таблицу <code>full_names</code>.</li>
        <li>Используется <code>SET status = short_names.status</code> для установки нового значения столбца <code>status</code>.</li>
        <li><code>FROM short_names</code> подключает таблицу <code>short_names</code>.</li>
        <li>Условие <code>WHERE full_names.name LIKE short_names.name || '%'</code> проверяет, что имена файлов совпадают, игнорируя расширения.</li>
    </ul>
    <h2>Вариант 2: Использование временной таблицы</h2>
    <pre><code>
-- Создание временной таблицы с данными о статусе
CREATE TEMP TABLE temp_full_names AS
SELECT f.name, f.status AS full_status, s.status AS short_status
FROM full_names f
JOIN short_names s ON f.name LIKE s.name || '%';

-- Обновление статусов в основной таблице
UPDATE full_names
SET status = temp_full_names.short_status
FROM temp_full_names
WHERE full_names.name = temp_full_names.name;
    </code></pre>
    <p><strong>Объяснение:</strong></p>
    <ul>
        <li><strong>Создание временной таблицы:</strong></li>
        <ul>
            <li>Временная таблица <code>temp_full_names</code> создается на основе объединения данных из <code>full_names</code> и <code>short_names</code>.</li>
            <li><code>JOIN</code> используется для объединения строк, где <code>full_names.name</code> начинается с <code>short_names.name</code>.</li>
        </ul>
        <li><strong>Обновление основной таблицы:</strong></li>
        <ul>
            <li>В этом запросе используется временная таблица для обновления статусов в основной таблице <code>full_names</code>.</li>
            <li><code>SET status = temp_full_names.short_status</code> обновляет столбец <code>status</code> в <code>full_names</code>.</li>
        </ul>
    </ul>
    <h2>Заключение</h2>
    <p>Оба варианта имеют свои преимущества. Первый вариант прост и эффективен, так как использует всего один запрос, но может занять больше времени на выполнение. Второй вариант более сложен, так как требует создания временной таблицы, но может быть более эффективным с точки зрения производительности, особенно если временная таблица индексирована.</p>
    <p>Оба варианта должны быть протестированы и оптимизированы для конкретной базы данных и окружения, чтобы выбрать наиболее эффективный подход.</p>
</body>
</html>
