from aiohttp import web
import asyncio
from db import init_db
from routes import task_routes
from aiohttp_swagger3 import SwaggerDocs, SwaggerUiSettings

app = web.Application()
app.add_routes(task_routes)

# Инициализация Swagger документации
swagger = SwaggerDocs(
    app,
    title="Task API",
    version="1.0.0",
    description="API для управления задачами",
    swagger_ui_settings=SwaggerUiSettings(path="/docs")  # путь к Swagger UI
)
swagger.add_routes(task_routes)


async def startup_db_init(app):
    await init_db()

app.on_startup.append(startup_db_init)

if __name__ == '__main__':
    web.run_app(app, port=9000)
