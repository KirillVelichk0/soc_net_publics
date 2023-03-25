import json
from pathlib import Path
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
        raise ValueError('Uncorrect config')