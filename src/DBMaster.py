from sqlalchemy.future import select, insert
import models 
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.orm import sessionmaker
from DBMasterConfigure import db_engine
from sqlalchemy import and_, or_

parse_model_row = lambda row : {c.name: getattr(row, c.name) for c in row.__table__.columns}
class RowExistingProblem(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'Row existing problem!'
    
    
    def __str__(self):
        return f'RowExistingProblem exception raised. Message: {self.message}'
    
    
    
def get_parse_model_and_return(result):
    result = result.scalars().all()
    result = [parse_model_row(data_row) for data_row in result]
    return result


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
            .where(and_(models.PublicsSubscriber.u_id == user_id, models.PublicsSubscriber.public_id < before_id))\
            .order_by(models.PublicsSubscriber.public_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return result.mappings()
        
    
    async def get_publics_limited_from_name(self, public_name: str, limit: int):
        session = self.local_session()
        print("without before ")
        query = select(models.Public).where(models.Public.public_name == public_name)\
            .order_by(models.Public.p_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return get_parse_model_and_return(result)
    
    async def get_publics_limited_before_from_name(self, public_name: str, limit: int, before_id: int):
        session = self.local_session()
        print(f"with before {before_id}")
        query = select(models.Public)\
            .where(and_(models.Public.public_name == public_name, before_id > models.Public.p_id))\
            .order_by(models.Public.p_id.desc()).limit(limit)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return get_parse_model_and_return(result)
    
    async def subsribe_to_public(self, public_id_in: int, u_id_in: int):
        session = self.local_session()
        query = select(models.PublicsSubscriber.u_id).\
            where(and_(u_id_in == models.PublicsSubscriber.u_id, public_id_in == models.PublicsSubscriber.public_id))
        live_row = await session.execute(query)
        live_row = live_row.first()
        if live_row is None:
            query = models.PublicsSubscriber.insert().values(u_id = u_id_in, public_id = public_id_in)
            await session.execute(query)
            await session.commit()
            await session.close()
        else:
            raise RowExistingProblem('Пользователь уже подписан на эту группу')
        
    
    
    async def describe_from_public(self, public_id_in: int, u_id_in: int):
        session = self.local_session()
        query = select(models.PublicsSubscriber.u_id).\
            where(and_(u_id_in == models.PublicsSubscriber.u_id, public_id_in == models.PublicsSubscriber.public_id))
        live_row = await session.execute(query)
        live_row = live_row.first()
        if live_row is not None:
            query = models.PublicsSubscriber.delete().where(and_(u_id_in == models.PublicsSubscriber.u_id, public_id_in == models.PublicsSubscriber.public_id))
            await session.execute(query)
            await session.commit()
            await session.close()
        else:
            raise RowExistingProblem('Пользователь не подписан на эту группу')
        
db_master_instance = DBMaster()  