import json
from sqlalchemy.future import select
import databases
from application import app
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine
def cofigure_from_json(base_dir: Path) -> tuple:
    cur_path = base_dir.joinpath('configs', 'db_auth_config.json')
    try:
        with open(cur_path) as file_config:
            json_aut = json.loads(file_config.read())
            db_name = json_aut['DB_NAME']
            user_name = json_aut['USER']
            host = json_aut['HOST']
            port = json_aut['PORT']
            path_to_pass = json_aut['PATH_TO_PASSWORD']
            with open(path_to_pass) as pass_file:
                json_password = json.loads(pass_file.read())
                password = json_password['password']
            return (db_name, user_name, password, host, port)
    except:
        raise ValueError(f'Uncorrect config. Base path {base_dir}')
    
def create_db_url():
      db_data = cofigure_from_json(Path(__file__).parent.parent.resolve()) 
      return f"mysql+aiomysql://{db_data[1]}:{db_data[2]}@{db_data[3]}:{db_data[4]}/{db_data[0]}" 
db_url = create_db_url()
db_engine = create_async_engine(db_url, echo=True)
db_instanse = databases.Database(db_url)

#до лучших времен
"""@app.on_event("startup")
async def startup():
    await db_instanse.connect()


@app.on_event("shutdown")
async def shutdown():
    await db_instanse.disconnect()"""

        
        


