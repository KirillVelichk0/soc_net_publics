from DBMaster import db_master_instance
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
    