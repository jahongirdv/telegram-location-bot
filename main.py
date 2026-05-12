import asyncio
import os
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import AuthBytesInvalid
from pyrogram.session import StringSession

# Получаем настройки из переменных окружения
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
CHAT_ID = int(os.getenv("CHAT_ID"))
LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))

async def send_location():
    """Отправляет геолокацию с использованием String Session"""
    async with Client(StringSession(STRING_SESSION), API_ID, API_HASH) as app:
        try:
            # Знакомство с чатом — обязательно для работы с группами
            chat = await app.get_chat(CHAT_ID)
            print(f"[{datetime.now()}] Подключены к чату: {chat.title}")

            # Отправляем геолокацию
            await app.send_location(CHAT_ID, LATITUDE, LONGITUDE)
            print(f"[{datetime.now()}] ✅ Геолокация отправлена!")

        except AuthBytesInvalid:
            print(f"[{datetime.now()}] ❌ Ошибка авторизации. Проверьте STRING_SESSION.")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Ошибка: {e}")

async def main():
    print("Бот запущен и ожидает расписания...")
    # Запускаем бесконечный цикл, который будет проверять время каждую минуту
    while True:
        now = datetime.now()
        # Если текущее время совпадает с заданным (13:04), а секунды не превышают 1, отправляем
        if now.hour == 13 and now.minute == 4 and now.second < 1:
            await send_location()
            # Ждём минуту, чтобы не отправить несколько раз за одну минуту
            await asyncio.sleep(60)
        else:
            # Проверяем каждые 30 секунд
            await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())