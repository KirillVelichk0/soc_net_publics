from sqlalchemy.future import select
import models 
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.orm import sessionmaker
from DBMasterConfigure import db_engine
class DBMaster:
    def __init__(self):
        self.local_session = sessionmaker(expire_on_commit=False, bind=db_engine, class_= AsyncSession)
    
    def __del__(self):
        self.local_session.close_all()
        
    async def get_publics_limited(self, limit: int, user_id: int):
        session = self.local_session()
        query = select(models.Public.public_name, models.Public.p_id)\
            .join(models.PublicsSubscriber.public_id, models.Public.p_id == models.PublicsSubscriber.public_id)\
            .where(models.PublicsSubscriber.u_id == user_id)\
            .order_by(models.PublicsSubscriber.public_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return result.mappings()
    
    async def get_publics_limited_before(self, before_id: int, limit: int, user_id:int):
        session = self.local_session()
        query = select(models.Public.public_name, models.Public.p_id)\
            .join(models.PublicsSubscriber.public_id, models.Public.p_id == models.PublicsSubscriber.public_id)\
            .where(models.PublicsSubscriber.u_id == user_id and models.PublicsSubscriber.public_id < before_id)\
            .order_by(models.PublicsSubscriber.public_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return result.mappings()
        
    
    async def get_publics_limited_from_name(self, public_name: str, limit: int):
        session = self.local_session()
        query = select(models.Public).where(models.Public.public_name == public_name)\
            .order_by(models.Public.p_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return result.scalars().all()
    
    async def get_publics_limited_before_from_name(self, public_name: str, limit: int, before_id: int):
        session = self.local_session()
        query = select(models.Public)\
            .where(models.Public.public_name == public_name and before_id > models.Public.p_id)\
            .order_by(models.Public.p_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return result.scalars().all()
  
  
db_master_instance = DBMaster()  