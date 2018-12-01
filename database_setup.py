from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    resource_link_id = Column(String(250), nullable=False)
    message_type = Column(String(250), nullable=False)
    lti_version = Column(String(250), nullable=False)



engine = create_engine('sqlite:///LTI_provider.db')


Base.metadata.create_all(engine)