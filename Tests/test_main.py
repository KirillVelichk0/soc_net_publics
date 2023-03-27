import sys, os
from fastapi.testclient import TestClient
lib_path = os.path.abspath(os.path.join(__file__, '..', '..', 'src'))
sys.path.append(lib_path)
import pytest
from httpx import AsyncClient




    
    
@pytest.mark.anyio
async def test_get_user_publics_with_before(client: AsyncClient):
    response = await client.post("/user_publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'jwt': 'jwt',\
                    'before': 100,\
                    'limit':20}) 
    assert response.status_code == 200
    print(response.json())

@pytest.mark.anyio
async def test_get_user_publics_without_before(client: AsyncClient):
    response1 = await client.post("/user_publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'jwt': 'jwt',\
                    'before': None,\
                    'limit':20}) 
    assert response1.status_code == 200
    print(response1.json())
    ...