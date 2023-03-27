from fastapi.responses import JSONResponse, FileResponse, Response
from application import app
from GroupsMaster import UserGroupsRequest, GroupsRequestFromName

        
@app.get("/")
async def root():
    return FileResponse('public/test.html')

@app.post("/user_publics", response_class=JSONResponse)
async def get_user_publics(request: UserGroupsRequest):
    try:
        result = await request.get_groups_from_self()
        rows_res = [str(public) for public in result[0]]
        if len(rows_res) > 0:
            return JSONResponse({"message": rows_res, "new_jwt": result[1]})
        else:
            return Response(status_code=204)
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=401)
    
@app.post('/publics', response_class=JSONResponse)
async def get_publics_from_name(request: GroupsRequestFromName):
    try:
        result = await request.get_groups_from_self()
        rows_res = [str(data_row) for data_row in result]
        if len(rows_res) > 0:
            return JSONResponse({"message": rows_res})
        else:
            return Response(status_code=204)
    except Exception as ex:
        return JSONResponse({"error": str(ex)}, status_code=404)