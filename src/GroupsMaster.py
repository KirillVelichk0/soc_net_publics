from DBMaster import db_master_instance, RowExistingProblem
from GRPCClient import auth
from pydantic import BaseModel
class UserGroupsRequest(BaseModel):
    jwt: str
    limit: int
    before: int | None = None

    async def get_groups_from_self(self):
        id, new_jwt = await auth(self.jwt)
        if self.before is None:
            pre_res = await db_master_instance.get_publics_limited(self.limit, id)
        else:
            pre_res = await db_master_instance.get_publics_limited_before(self.before, self.limit, id)
        return (pre_res, new_jwt)
       

class GroupsRequestFromName(BaseModel):
    limit: int
    before: int | None = None
    public_name: str  
    
    async def get_groups_from_self(self):
        if self.before is None:
            result = await db_master_instance.get_publics_limited_from_name(self.public_name, self.limit)
        else:
            result = await db_master_instance.get_publics_limited_before_from_name(self.public_name\
                , self.limit, self.before)
        return result
    
    
class TrySub_Unsub(BaseModel):
    jwt: str
    public_id: int
    sub: bool
    
    
    async def try_sub_unsub_from_self(self):
        id, new_jwt = await auth(self.jwt)
        try:
            if self.sub:
                await db_master_instance.subsribe_to_public(self.public_id, id)
            else:
                await db_master_instance.describe_from_public(self.public_id, id)
        except RowExistingProblem as ex:
            raise ex
        except Exception as ex:
            raise ex
        return new_jwt


class GetAuthoredGroupsRequest(BaseModel):
    jwt: str
    
    async def get_authored_from_self(self):
        id, new_jwt = await auth(self.jwt)
        pre_res = await db_master_instance.get_my_authored_publics(id)
        return (pre_res, new_jwt)


class DeletePublicRequest(BaseModel):
    jwt: str
    public_id: int
    
    
    async def delete_public_from_self(self):
        id, new_jwt = auth(self.jwt)
        try:
            await db_master_instance.delete_public(id, self.public_id)
            return new_jwt
        except Exception as ex:
            raise ex
    
    
class GetPublicRequest(BaseModel):
     public_id: int
     
     async def get_public_from_self(self):
         return await db_master_instance.get_public_from_id(self.public_id)


class RedactPublicHeadRequest(BaseModel):
    jwt : str
    public_id: int
    new_name: str
    new_readme: str
    
    async def redact_from_self(self):
        id, new_jwt = auth(self.jwt)
        try:
            await db_master_instance.redact_public_head(self.public_id, self.new_name,\
                self.new_readme, id)
            return new_jwt
        except Exception as ex:
            raise ex


class SendPostRequest(BaseModel):
    jwt: str
    public_id: int
    text: str
    
    async def send_post_from_self(self):
        id, new_jwt = auth(self.jwt)
        try:
            await db_master_instance.send_post(self.public_id, id, self.text)
            return new_jwt
        except Exception as ex:
            raise ex
    
    
class GetPostsRequest(BaseModel):
    public_id: int
    limit: int
    before: int | None = None
    
    
    async def get_posts_from_self(self):
        if self.before is None:
            result = await db_master_instance.get_last_posts(self.public_id, self.limit)
        else:
            result = await db_master_instance.get_last_posts_before(self.public_id,\
                self.limit, self.before)
        return result
        
    
class CreatePublicRequest(BaseModel):
    jwt: str
    public_name: str
    public_readme: str
    
    async def try_create_from_self(self):
        id, new_jwt = await auth(self.jwt)
        await db_master_instance.create_public(id, self.public_name, self.public_readme)
        return new_jwt
    