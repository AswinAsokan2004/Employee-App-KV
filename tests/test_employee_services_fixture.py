# tests/test_employee_service.py

# `pytest_asyncio` provides the *async-aware* fixture decorator. Plain
# `@pytest.fixture` doesn't know how to drive an `async def` body — you
# have to use `@pytest_asyncio.fixture` whenever the fixture itself is
# async or yields an async resource.
import pytest
# Same async-flavoured SQLAlchemy imports as the previous slide.

from auth.utils import hash_password
from employees import employee_services as employee_service
from models.employee import Employee


# The fixture: a single function that owns the engine, the schema, and
# the session — and tears it all back down when the test finishes.


# The test is now pure "act + assert" — no engine, no create_all, no
# cleanup. Pytest sees the `db_session` parameter, runs the fixture
# above, and hands the yielded session in.
@pytest.mark.anyio
async def test_get_by_id_returns_seeded_employee(db_session):

    # Seed a row directly via the ORM. We construct Employee ourselves
    # (with a real `password_hash`) because service.create currently
    # drops the password field — bypassing it keeps this test focused.
    seeded = Employee(
        name="Ada", email="ada@example.com", password_hash=hash_password("secret123")
    )
    # `add()` is sync — it just stages the row in the session.
    db_session.add(seeded)
    # `commit()` is the IO step. Must be awaited.

    await db_session.commit()

    # `refresh()` re-reads the row so `seeded.id` is populated.

    await db_session.refresh(seeded)

    # Call the function under test — async, so we await.

    fetched = await employee_service.get_employee_by_id(
        db=db_session, employee_id=seeded.id
    )

    assert fetched.get("id") == seeded.id
    assert fetched.get("email") == "ada@example.com"
