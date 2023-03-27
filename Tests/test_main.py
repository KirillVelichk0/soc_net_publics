import sys, os
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

@pytest.mark.anyio    
async def test_get_publics_for_name(client: AsyncClient):
    response = await client.post("/publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'public_name': 'Юморески',
                        'before': None,
                        'limit':20}
        )
    assert response.status_code == 200
    print(response.json())
    
    response = await client.post("/publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'public_name': 'НЕ_Юморески',
                        'before': None,
                        'limit':20}
        )
    assert response.status_code == 204


@pytest.mark.anyio        
async def test_get_publics_for_name_with_before(client: AsyncClient):
    response = await client.post("/publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'public_name': 'Юморески',
                        'before': 20,
                        'limit':20}
        )
    assert response.status_code == 200
    print(response.json())
    
    response = await client.post("/publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'public_name': 'НЕ_Юморески',
                        'before': 10,
                        'limit':20}
        )
    assert response.status_code == 204
    
    response = await client.post("/publics",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'public_name': 'Юморески',
                        'before': 1,
                        'limit':20}
        )
    assert response.status_code == 204
    
@pytest.mark.anyio   
async def test_sub_unsub(client: AsyncClient):
    response = await client.post("/publics/sub_des",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'jwt': 'qwr',
                        'public_id': 2,
                        'sub':True}
        )
    assert response.status_code == 200
    
    response = await client.post("/publics/sub_des",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'jwt': 'qwr',
                        'public_id': 2,
                        'sub':True}
        )
    assert response.status_code == 405
    
    response = await client.post("/publics/sub_des",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'jwt': 'qwr',
                        'public_id': 2,
                        'sub':False}
        )
    assert response.status_code == 200
    
    response = await client.post("/publics/sub_des",\
        headers= { "Accept": "application/json", "Content-Type": "application/json" },\
        json= {'jwt': 'qwr',
                        'public_id': 2,
                        'sub':False}
        )
    assert response.status_code == 405
    