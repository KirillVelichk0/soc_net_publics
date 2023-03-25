from fastapi.responses import JSONResponse, FileResponse
from application import app
from GroupsMaster import GroupsRequest
from fastapi import Request

        
@app.get("/")
async def root():
    return FileResponse("public/test.html")

@app.post("/groups")
async def get_groups(request: GroupsRequest):
    try:
        result = await request.get_groups_from_self()
        return JSONResponse({"message":[public_name for public_name in result[0]], "new_jwt": result[1]})
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=401)