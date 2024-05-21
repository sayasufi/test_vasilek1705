import os

import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Получение настроек из переменных окружения
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))

# Подключение к Redis
try:
    r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    r.ping()  # Проверка соединения с Redis
except redis.ConnectionError as e:
    raise Exception("Не удалось подключиться к Redis. Пожалуйста, проверьте ваш сервер Redis.") from e


class WriteData(BaseModel):
    phone: str = Field(..., title="Номер телефона", regex="^\\d{11}$", example="89090000000")
    address: str = Field(..., title="Адрес", max_length=255, example="123 Main St, Anytown, USA")


class CheckData(BaseModel):
    phone: str = Field(..., title="Номер телефона", regex="^\\d{11}$", example="89090000000")


@app.post("/write_data/", response_model=dict)
def write_data(data: WriteData):
    """
    Запись или обновление номера телефона и адреса в Redis.

    Args:
        data (WriteData): Номер телефона и адрес для сохранения.

    Returns:
        dict: Подтверждающее сообщение.
    """
    try:
        r.set(data.phone, data.address)
        return {"message": "Данные успешно записаны"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from e


@app.get("/check_data/", response_model=dict)
def check_data(phone: str):
    """
    Получение адреса по номеру телефона из Redis.

    Args:
        phone (str): Номер телефона для поиска.

    Returns:
        dict: Номер телефона и соответствующий адрес.
    """
    try:
        address = r.get(phone)
        if address is None:
            raise HTTPException(status_code=404, detail="Номер телефона не найден")
        return {"phone": phone, "address": address}
    except HTTPException as e:
        raise e  # Повторное поднятие HTTP исключений, чтобы сохранить статус код и сообщение
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера") from e


# Дополнительная ручка для обработки корневого URL
@app.get("/")
def read_root():
    """
    Корневой эндпоинт для проверки работы API.

    Returns:
        dict: Приветственное сообщение.
    """
    return {"message": "Добро пожаловать в сервис FastAPI-Redis. Используйте /docs для документации API."}
