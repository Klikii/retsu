from sqlalchemy import BigInteger, Boolean, DateTime, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime

engine = create_async_engine(url='postgresql+asyncpg://postgres:Qwsxzectgb54321@localhost/dbname')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    payment_status: Mapped[bool] = mapped_column(Boolean, default=False)
    payment_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=True)

async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)    
        
async def set_user_paid(user_id: int, username: str):
    async with async_session() as session:
        # Check we have that user or not
        user = await session.get(User, user_id)
        
        if user:
            user.payment_status = True
            user.username = username
            user.payment_date = datetime.now()
        else:
            new_user = User(
                user_id=user_id,
                username=username,
                payment_status=True,
                payment_date=datetime.now()
            )
            session.add(new_user)
            
        await session.commit()