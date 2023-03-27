from sqlalchemy import BigInteger, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata


class Public(Base):
    __tablename__ = 'publics'

    p_id = Column(BigInteger, primary_key=True)
    author_id = Column(BigInteger, index=True)
    public_name = Column(String(20), index=True)
    public_readme = Column(String(200))


class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(BigInteger, primary_key=True)
    public_id = Column(ForeignKey('publics.p_id'), index=True)
    text_data = Column(Text)

    public = relationship('Public')


class PublicsSubscriber(Base):
    __tablename__ = 'publics_subscribers'

    public_id = Column(ForeignKey('publics.p_id'), primary_key=True, nullable=False, index=True)
    u_id = Column(BigInteger, primary_key=True, nullable=False, index=True)

    public = relationship('Public')

    