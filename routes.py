import datetime
from aiohttp import web
from sqlalchemy.future import select
from db import async_session
from models import Task
from datetime import datetime

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
        required: true
        schema:
          type: integer
        description: ID задачи
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
                is_done:
                  type: boolean
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
                deadline:
                  type: string
                  format: date-time
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
        result = await session.execute(select(Task).where(Task.id == int(task_id)))
        task = result.scalars().first()

        if task is None:
            return web.json_response({"error": "Task not found"}, status=404)

        task_data = {
            "id": task.id,
            "text": task.text,
            "is_done": task.is_done,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "deadline": task.deadline.isoformat() if task.deadline else None
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
              is_done:
                type: boolean
                description: Статус задачи (выполнена или нет)
              deadline:
                type: string
                format: date-time
                description: Дедлайн на выполнение задачи
            required:
              - text
              - is_done
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
                is_done:
                  type: boolean
                deadline:
                  type: string
                  format: date-time
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
    """
    data = await request.json()

    async with async_session() as session:
        task_data = {
            "text": data.get('text'),
            "is_done": data.get('is_done'),
            "deadline": data.get('deadline', None)
        }

        new_task = Task(
            text=task_data["text"],
            is_done=task_data["is_done"],
            deadline=datetime.fromisoformat(
                task_data['deadline'].replace("Z", "+00:00"))
        )
        session.add(new_task)

        await session.commit()

        created_task_data = {
            "id": new_task.id,
            "text": new_task.text,
            "is_done": new_task.is_done,
            "deadline": new_task.deadline.isoformat() if new_task.deadline else None,
            "created_at": new_task.created_at.isoformat(),
            "updated_at": new_task.updated_at.isoformat() if new_task.updated_at else None
        }

        return web.json_response(created_task_data, status=201)


@task_routes.patch('/task/{id}/done')
async def change_task_state(request):
    """
    ---
    description: Изменить статус задачи на выполнена
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID задачи
    responses:
      "200":
        description: Успешное обновление статуса задачи
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
        result = await session.execute(select(Task).where(Task.id == int(task_id)))
        task = result.scalars().first()

        if task is None:
            return web.json_response({"error": "Task not found"}, status=404)

        task.is_done = True
        session.add(task)
        await session.commit()

        return web.Response(status=200)


@task_routes.delete('/task/{id}/delete')
async def delete_task(request):
    """
    ---
    description: Удалить задачу
    tags:
      - Tasks
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: ID задачи
    responses:
      "200":
        description: Успешное удаление задачи
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
        result = await session.execute(select(Task).where(Task.id == int(task_id)))
        task = result.scalars().first()

        if task is None:
            return web.json_response({"error": "Task not found"}, status=404)

        await session.delete(task)
        await session.commit()

        return web.Response(status=200)
