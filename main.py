# main.py
from aiohttp import web
import asyncio
from aiohttp.web_request import Request
from db import init_db
# Импортируем модель, чтобы она регистрировалась в метаданных базы данных
from routes import task_routes
from models import Task

app = web.Application()
app.add_routes(task_routes)

if __name__ == '__main__':
    asyncio.run(init_db())
    web.run_app(app, port=9000)
