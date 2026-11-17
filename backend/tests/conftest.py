import pytest


# Testcontainers PostgreSQL will be wired here in Stage 1.
# For now the fixtures are stubs so the test suite can run without a live DB.


@pytest.fixture(scope="session")
def engine() -> None:  # type: ignore[return]
    # TODO Stage 1: replace with Testcontainers postgres
    return None


@pytest.fixture
def db(engine: None) -> None:  # type: ignore[return]
    return None
