from sqlalchemy.future import select
import models 
from sqlalchemy.ext.asyncio import  AsyncSession
import asyncio
from sqlalchemy.orm import sessionmaker
from DBMasterConfigure import db_engine, db_instanse
from sqlalchemy import and_, or_, insert, delete, update

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
        print("sub executed")
        if len(live_row.scalars().all()) == 0:
            new_sub = models.PublicsSubscriber(u_id= u_id_in, public_id=public_id_in)
            print('query created')
            session.add(new_sub)
            print('query added')
            await session.flush()
            print('query flushed')
            await session.commit()
            print('query commited')
            await session.close()
            print('query closed')
        else:
            await session.close()
            print("exception raised")
            raise RowExistingProblem('Пользователь уже подписан на эту группу')
        
    
    
    async def describe_from_public(self, public_id_in: int, u_id_in: int):
        session = self.local_session()
        query = select(models.PublicsSubscriber.u_id).\
            where(and_(u_id_in == models.PublicsSubscriber.u_id, public_id_in == models.PublicsSubscriber.public_id))
        live_row = await session.execute(query)
        print("sub executed")
        if len(live_row.scalars().all()) != 0:
            query = delete(models.PublicsSubscriber).where(and_(models.PublicsSubscriber.u_id == u_id_in,\
                models.PublicsSubscriber.public_id == public_id_in))
            await session.execute(query)
            await session.commit()
            await session.close()
        else:
            await session.close()
            raise RowExistingProblem('Пользователь не подписан на эту группу')
        
     #Все, что ниже, пока не протестировано   
    async def get_my_authored_publics(self, author_id: int):
        session = self.local_session()
        query = select(models.Public).where(models.Public.author_id == author_id)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return get_parse_model_and_return(result)
    
    
    async def create_public(self, author_id_in: int, public_name_in: str, public_readme_in: str):
        session = self.local_session()
        new_pub = models.Public(p_id = None, author_id= author_id_in, \
            public_name = public_name_in, public_readme = public_readme_in)
        session.add(new_pub)
        await session.flush()
        await session.commit()
        await session.close()
        
    async def delete_public(self, author_id_in, public_id_in):
        session = self.local_session()
        query = select(models.Public.p_id).\
            where(and_(models.Public.p_id == author_id_in, models.Public.author_id == public_id_in))
        live_row = await session.execute(query)
        if len(live_row.scalars().all()) != 0:
            query = delete(models.PublicsSubscriber).\
                where(models.PublicsSubscriber.public_id == public_id_in)
            await session.execute(query)
            query = delete(models.Public).\
                where(models.Public.p_id == public_id_in)
            await session.execute(query)
            await session.commit()
            await session.close()
        else:
           raise RowExistingProblem('Uncorrect public data') 
        
        
    async def get_public_from_id(self, public_id_in: int):
        session = self.local_session()
        query = select(models.Public).where(models.Public.p_id == public_id_in)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return get_parse_model_and_return(result)
    
    
    async def redact_public_head(self, public_id_in:int, public_name_in: str,
                                 public_readme_in: str, author_id_in: int):
        session = self.local_session()
        query = select(models.Public.p_id).\
            where(and_(models.Public.p_id == author_id_in, models.Public.author_id == public_id_in))
        live_row = await session.execute(query)
        if len(live_row.scalars().all()) != 0:
            query = update(models.Public).\
            where(models.Public.id == public_id_in).\
            values(public_name= public_name_in, public_readme = public_readme_in)
            await session.execute(query)
            await session.commit()
            await session.close()
            ...
        else:
             raise RowExistingProblem('Uncorrect public data') 
         
    async def get_last_posts(self, public_id_in: int, limit_in: int):
        session = self.local_session()
        query = select(models.Post).where(models.Post.public_id == public_id_in).\
            order_by(models.Post.post_id.desc()).limit(limit_in)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return get_parse_model_and_return(result)
    
    
    async def get_last_posts_before(self, public_id_in: int, limit_in: int, before_in : int):
        session = self.local_session()
        query = select(models.Post).\
            where(and_(models.Post.public_id == public_id_in, models.Post.post_id < before_in)).\
            order_by(models.Post.post_id.desc()).limit(limit_in)
        result = await session.execute(query)
        await session.commit()
        await session.close()
        return get_parse_model_and_return(result)
    
    async def send_post(self, public_id_in: int, author_id_in: int, text_data_in: str):
        session = self.local_session()
        query = select(models.Public.p_id).\
            where(and_(models.Public.author_id == author_id_in, models.Public.p_id == public_id_in))
        live_row = session.execute(query)
        if len(live_row.scalars().all()) != 0:
            new_post = models.Post(post_id = None, public_id = public_id_in, text_data = text_data_in)
            session.add(new_post)
            await session.flush()
            await session.commit()
            await session.close()
        else:
            await session.close()
            raise RowExistingProblem('Вы не являетесь автором этой группы')
        
        
db_master_instance = DBMaster() 