from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from env import DB_USERNAME, DB_PASS, DB_ADRESS, DB_NAME

DATABASE_URL = f"postgresql+asyncpg://{
    DB_USERNAME}:{DB_PASS}@{DB_ADRESS}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
