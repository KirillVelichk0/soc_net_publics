from fastapi.responses import JSONResponse, FileResponse, Response
from application import app
from GroupsMaster import *
from DBMaster import RowExistingProblem
main_app = app       
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
    
@app.post('/publics')
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
    
@app.post('/publics/sub_des')
async def subscribe_describe(request: TrySub_Unsub):
    try:
        await request.try_sub_unsub_from_self()
        return Response(status_code=200)
    except RowExistingProblem:
        return Response(status_code= 405)
    except Exception:
        return Response(status_code=401)
    

@app.post('publics/authored_pubs')
async def get_my_authored_publics(request: GetAuthoredGroupsRequest):
    result = await request.get_authored_from_self()
    return JSONResponse({"message": result[0], "new_jwt": result[1]})

@app.post('publics/create')
async def create_public(request: CreatePublicRequest):
    result = await request.try_create_from_self()
    if result is not None:
        return JSONResponse({"message": result[0], "new_jwt": result[1]})
    else:
        return JSONResponse({"error": 'Uncorrect auth data'}, status_code=401)

    
@app.post('publics/delete')
async def delete_public(request: DeletePublicRequest):
    try:
        new_jwt = await request.delete_public_from_self()
        return JSONResponse({"message": 'Ok', "new_jwt": new_jwt})
    except Exception:
        return JSONResponse({"error": 'Uncorrect auth data'}, status_code=401)
    
    
@app.post('publics/from_id')
async def get_pub_from_id(request: GetPublicRequest):
    result = await request.get_public_from_self()
    return JSONResponse({"message": result})


@app.post('publics/redact')
async def redact_public_head(request: RedactPublicHeadRequest):
    try:
        new_jwt = await request.redact_from_self()
        return JSONResponse({"message": 'Ok', "new_jwt": new_jwt})
    except Exception:
        return JSONResponse({"error": 'Uncorrect auth data'}, status_code=401)
    

@app.post('publics/get_posts')
async def get_posts_request(request: GetPostsRequest):
    result = await request.get_posts_from_self()
    return JSONResponse({"message": result})


@app.post('publics/create_post')
async def create_post(request: SendPostRequest):
    try:
        new_jwt = await request.send_post_from_self()
        return JSONResponse({"message": 'Ok', "new_jwt": new_jwt})
    except Exception:
        return JSONResponse({"error": 'Uncorrect auth data'}, status_code=401)