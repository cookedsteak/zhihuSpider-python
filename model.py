from sqlalchemy import Column, String, Integer, VARCHAR, Text
from sqlalchemy.ext.declarative import declarative_base


# orm基类
Base = declarative_base()


class Users(Base):
    """
    用户表映射
    """
    __tablename__ = 'zhihu_users'

    id = Column('id', Integer, primary_key=True)
    username = Column('username', VARCHAR(100))
    showname = Column('showname', VARCHAR(120))
    followers = Column('followers', Integer)
    followees = Column('followees', Integer)
    focus = Column('focus', VARCHAR(45))
    gender = Column('gender', Integer)
    sign = Column('sign', VARCHAR(255))


