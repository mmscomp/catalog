#import sys,psycopg2
#from psycopg2 import postgressql
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from  datetime import datetime as Date

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Sports(Base):
    __tablename__ = 'sports'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(300), nullable=True)
    favorite = Column(String(300), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""

        return {

            'name': self.name,
            'id': self.id,
            'description': self.description,
            'favorite': self.favorite,

        }

class Entertainment(Base):
    __tablename__ = 'entertainment'

    name  = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(230), nullable=True)
    favorite = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        """Return object data in easily serializeable format"""

        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'favorite': self.favorite,
        }

class Education(Base):
    __tablename__ = 'education'

    name  = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(230), nullable=True)
    favorite = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        """Return object data in easily serializeable format"""

        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'favorite': self.favorite,
        }

class Business(Base):
    __tablename__ = 'business'

    name  = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(230), nullable=True)
    favorite = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        """Return object data in easily serializeable format"""

        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'favorite': self.favorite,
        }

class Read(Base):
    __tablename__ = 'books'

    name  = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(230), nullable=True)
    favorite = Column(String(200), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        """Return object data in easily serializeable format"""

        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'favorite': self.favorite,
        }

class Diary(Base):
    __tablename__ = 'diary'

    name  = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable =True)
    description = Column(String(230), nullable=True)
    date = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        """Return object data in easily serializeable format"""

        return {
            'name': self.name,
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
        }

url = 'postgresql://{}:{}@{}:{}/{}'
#url = url.format('postgres','grespost','localhost',5432,'catalogdb')
url = url.format('matt','jonam','localhost',5432,'catalogdb')
engine = create_engine('sqlite:///app1withusers.db')
#connection = psycopg2.connect(url)

Base.metadata.create_all(engine)
