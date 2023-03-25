async def some_mock(jwt:str):
    return (13, 'Use_Old')


async def auth(jwt:str):
    return await some_mock(jwt)