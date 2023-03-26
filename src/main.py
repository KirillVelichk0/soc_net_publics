from fastapi.responses import JSONResponse, FileResponse
from application import app
from GroupsMaster import UserGroupsRequest, GroupsRequestFromName

parse_model_row = lambda row : {c.name: getattr(row, c.name) for c in row.__table__.columns}
        
@app.get("/")
async def root():
    return FileResponse('public/test.html')

@app.post("/user_publics")
async def get_user_publics(request: UserGroupsRequest):
    try:
        result = await request.get_groups_from_self()
        return JSONResponse({"message":[str(public) for public in result[0]], "new_jwt": result[1]})
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=401)
    
@app.post('/publics')
async def get_publics_from_name(request: GroupsRequestFromName):
    try:
        result = await request.get_groups_from_self()
        return JSONResponse({"message": [str(parse_model_row(data_row)) for data_row in result]})
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=404)