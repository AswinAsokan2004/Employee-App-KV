# Async-flavoured SQLAlchemy: async engine factory + async session factory.
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# `hash_password` — service.create() drops the password field today, so we
# bypass it and seed the row directly with a valid bcrypt hash ourselves.
from auth.utils import hash_password

# `Base` carries the metadata for every ORM-mapped class — used by
# `create_all` / `drop_all` to build and wipe the schema.
from database import Base

# The service under test.
from employees import employee_services as employee_service

# The ORM model we'll instantiate to seed a row.
from models.employee import Employee
import pytest


# `async def` because the body uses `await`. `pytest-asyncio` (mode=auto in
# pyproject.toml) runs this on an event loop for us — no decorator needed.
@pytest.mark.anyio
async def test_get_by_id_returns_seeded_employee():

    # ── SETUP ─────────────────────────────────────────────

    # 1. Build an async engine pointed at an in-memory SQLite database.

    #    The `+aiosqlite` suffix selects the async driver — without it,

    #    SQLAlchemy would pick the default sync driver and refuse to mix.

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    # 2. Materialise every ORM table on the empty in-memory DB.

    #    `engine.begin()` is an async context manager that opens a

    #    transactional connection. `create_all` is a *sync* SQLAlchemy

    #    call, so we hand it to `conn.run_sync(...)`, which runs it on a

    #    worker thread (via greenlet) and awaits the result.

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 3. Build the session factory and immediately open one session.

    #    `expire_on_commit=False` keeps loaded attributes usable after

    #    `commit()` — the recommended setting for async SQLAlchemy.

    db = async_sessionmaker(engine, expire_on_commit=False)()

    # ── ACT ───────────────────────────────────────────────
    # Build an Employee directly (bypassing the service) so we control
    # every field — including `password_hash`, which the service drops.
    seeded = Employee(
        name="Ad43424a",
        email="ada42342424@example.com",
        password_hash=hash_password("secret123"),
    )
    # `add()` is sync — it just stages the row in the session's identity map.
    db.add(seeded)
    # `commit()` is the IO step — flush + COMMIT to SQLite. Must be awaited.

    await db.commit()

    # `refresh()` re-reads the row so `seeded.id` is populated from the DB.

    await db.refresh(seeded)

    # Call the function under test — it itself is `async def`, so we await.

    fetched = await employee_service.get_employee_by_id(db=db, employee_id=seeded.id)

    # ── ASSERT ────────────────────────────────────────────
    # Same id we seeded — proves the lookup returned the right row.
    assert fetched.get("id") == seeded.id
    # Email round-trips through SQLAlchemy unchanged.
    assert fetched.get("email") == "ada42342424@example.com"

    # ── TEARDOWN ──────────────────────────────────────────

    # Close the session — releases the connection back to the pool.

    await db.close()

    # Drop every table so the next test starts clean. (We could also let the

    # engine fall out of scope, but explicit cleanup is the lesson here.)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # Dispose the engine — closes the underlying connection pool.

    await engine.dispose()
