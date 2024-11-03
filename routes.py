# routest.py
from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import async_session
from models import Task

task_routes = web.RouteTableDef()


@task_routes.get('/task/{id}')
async def get_task_by_id(request):
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
