from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, default='')
    url_link = Column(String(32))
    ingredients = Column(String(32))
    instructions = Column(String(32))

engine = create_engine('sqlite:///recipes.db')
 

Base.metadata.create_all(engine)
    
