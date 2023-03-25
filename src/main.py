from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from application import app
from DBMaster import db_master_instance


        
@app.get("/")
async def read_root():
    html_content = "<h2>Hello somebody!</h2>"
    return HTMLResponse(content=html_content)

@app.get("/1")
async def get_test_1():
    result = await db_master_instance.get_publics_limited(20, 13)
    return JSONResponse({"message":[public_name for public_name in result]})