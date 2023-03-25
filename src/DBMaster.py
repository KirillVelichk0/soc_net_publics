from sqlalchemy.future import select
import models 
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.orm import sessionmaker
from DBMasterConfigure import db_engine
class DBMaster:
    def __init__(self):
        self.local_session = sessionmaker(expire_on_commit=False, bind=db_engine, class_= AsyncSession)
    
        
        
    async def get_publics_limited(self, limit: int, user_id: int):
        session = self.local_session()
        query = select(models.Public.public_name)\
            .join(models.PublicsSubscriber.public_id, models.Public.p_id == models.PublicsSubscriber.public_id)\
            .where(models.PublicsSubscriber.u_id == user_id)\
            .order_by(models.PublicsSubscriber.public_id.desc()).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
        
  
  
  
db_master_instance = DBMaster()  