import pytest
import sys, os
lib_path = os.path.abspath(os.path.join(__file__, '..', '..', 'src'))
sys.path.append(lib_path)
from main import main_app
from httpx import AsyncClient


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=main_app, base_url="http://test") as client:
        print("Client is ready")
        yield client