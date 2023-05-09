from pathlib import Path
import sys, os
lib_path = os.path.abspath(os.path.join(__file__, '..', 'proto_gen'))
sys.path.append(lib_path)
import proto_gen.AuthServ_pb2_grpc as AuthServ_ipb2_grpc
import proto_gen.AuthServ_pb2 as AuthServ_ipb2
import grpc
from pathlib import Path
import json

import asyncio

class AuthServCaller:
    def __init__(self) -> None:
        self.channel_data = 'localhost:8091'
        base_dir = Path(__file__).parent.parent.resolve()
        cur_path = base_dir.joinpath('configs', 'db_auth_config.json')
        with open(cur_path) as json_config:
            path_to_cred_json = json.load(json_config)
        path_to_cred = path_to_cred_json['PathToCreds']
        #key = path_to_cred_json['Key']
        print("config parsed")
        pem_cert = open(path_to_cred, 'rb').read()
        #key_cert = open(key, 'rb').read()
        self.credential = grpc.ssl_channel_credentials(root_certificates=pem_cert)
        print("creds getted")

    def GetSecureChannel(self):
        return grpc.aio.secure_channel(self.channel_data, self.credential)
        
    def GetInsecure(self):
        return grpc.aio.insecure_channel(self.channel_data)
    
    
    async def TryRegistr(self, email: str, password: str):
        print("Start sendind")
        async with self.GetSecureChannel() as async_channel:
            print("Channel opened")
            stub = AuthServ_ipb2_grpc.AuthAndRegistServiceStub(async_channel)
            print('stub getted')
            input_data = AuthServ_ipb2.RegistrationInput(email= email, password= password)
            print('input data created')
            result = await stub.TryRegistr(input_data)
            print("Data getted")
            return (result.answer, result.isOk)
        
    async def TryVerifyRegistr(self, rand_token: str):
        async with self.GetSecureChannel() as async_channel:
            stub = AuthServ_ipb2_grpc.AuthAndRegistServiceStub(async_channel)
            input_data = AuthServ_ipb2.RegistrationVerificationInput(randomDataToken=rand_token)
            result = await stub.TryVerifRegistr(input_data)
            return result.response_message
        
    async def LoginWithPassword(self, email: str, password: str):
        async with self.GetSecureChannel() as async_channel:
            stub = AuthServ_ipb2_grpc.AuthAndRegistServiceStub(async_channel)
            input_data = AuthServ_ipb2.PasswordAuthInput(email=email, password=password)
            result = await stub.AuthFromPassword(input_data)
            return (result.jwtToken, result.user_id)
        
    async def LoginWithJWT(self, jwt:str):
        async with self.GetSecureChannel() as async_channel:
            stub = AuthServ_ipb2_grpc.AuthAndRegistServiceStub(async_channel)
            input_data = AuthServ_ipb2.AuthInput(jwtToken=jwt)
            result = await stub.Authenticate(input_data)
            return (result.userId, result.nextToken)
        



def IsDebug():
    base_dir = Path(__file__).parent.parent.resolve()
    cur_path = base_dir.joinpath('configs', 'db_auth_config.json')
    with open(cur_path) as file_config:
        json_config = json.loads(file_config.read())
    return json_config['Mode']== 'Debug'


is_debug = IsDebug()
if not is_debug:
    print("Creating grpc client")
    grpc_client = AuthServCaller() 


async def some_mock(jwt:str):
    return (13, 'Use_Old')


async def auth(jwt:str):
    if is_debug:
        return await some_mock(jwt)
    else:
        return await grpc_client.LoginWithJWT(jwt)