import uvicorn
from pathlib import Path
import json

if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent.resolve()
    cur_path = base_dir.joinpath('configs', 'db_auth_config.json')
    src_dir = base_dir.joinpath('src')
    with open(cur_path) as json_config:
        path_to_cred_json = json.load(json_config)
    crt_path = path_to_cred_json['PEM_crt']
    key_path = path_to_cred_json['PEM_key']

    uvicorn.run("main:app",
                host="0.0.0.0",
                port=8007,
                reload=True,
                ssl_keyfile=key_path,
                ssl_certfile=crt_path
                )