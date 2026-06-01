import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from database import Base
from employees import employee_services as employee_service


@pytest.mark.anyio
async def test_create_employee_persists_the_record():

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as db:
        # body = EmployeeCreate(
        #     name="Ada",
        #     email="ada@example.com",
        #     password="secret123"
        # )

        employee = await employee_service.create(
            name="Ada", email="ada@example.com", age=23, password="secret123", db=db
        )

        assert employee.id is not None
        assert employee.name == "Ada"
        assert employee.email == "ada@example.com"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
