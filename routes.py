import datetime
from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
from models import Task

task_routes = web.RouteTableDef()


@task_routes.get('/task/{id}')
async def get_task_by_id(request):
    """
    ---
    description: Получить задачу по ID
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        description: ID задачи
        required: true
        schema:
          type: integer
    responses:
      "200":
        description: Успешное получение задачи
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                text:
                  type: string
                status:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "404":
        description: Задача не найдена
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
    """
    task_id = request.match_info['id']
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Task).where(Task.id == int(task_id)))
            task = result.scalars().first()

        if task is None:
            return web.json_response({"error": "Task not found"}, status=404)

        task_data = {
            "id": task.id,
            "text": task.text,
            "status": task.status,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None
        }

        return web.json_response(task_data)


@task_routes.post('/task')
async def create_task(request):
    """
    ---
    description: Создать новую задачу
    tags:
      - Tasks
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              text:
                type: string
                description: Текст задачи
              status:
                type: boolean
                description: Статус задачи (например, "в работе" или "завершена")
            required:
              - text
              - status
    responses:
      "201":
        description: Задача успешно создана
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                text:
                  type: string
                status:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
    """
    data = await request.json()

    async with async_session() as session:
        task_data = {
            "text": data.get('text'),
            "status": data.get('status'),
            "created_at": datetime.datetime.utcnow()
        }

        async with session.begin():
            new_task = Task(
                text=task_data["text"],
                status=task_data["status"],
                created_at=task_data["created_at"],
                updated_at=None
            )
            session.add(new_task)

        await session.commit()
        await session.refresh(new_task)
        task_data['created_at'] = task_data['created_at'].__str__()
        return web.json_response(task_data, status=201)
