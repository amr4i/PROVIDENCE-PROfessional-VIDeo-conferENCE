import os
import sys

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *

Base = declarative_base()

class UserBase(Base):
    __tablename__ = 'users'

    username = Column(String(128), primary_key=True)
    password = Column(String(128))


    def __init__(self, username, password):
        self.username = username
        self.password = password


def db_setup():
    dbdir = 'db'
    if os.path.exists(dbdir) == False:
        os.makedirs(dbdir)

    dbfile = os.path.join(dbdir, 'user_data.db')

    db_engine = create_engine('sqlite:///%s' % dbfile)
    Base.metadata.create_all(db_engine)


def db_session():
    dbfile = os.path.join('db', 'user_data.db')
    db_engine = create_engine('sqlite:///%s' % dbfile)
    session = sessionmaker(bind=db_engine)
    return session()


if __name__ == '__main__':
    if sys.argv[1] == 'init-db':
        db_setup()
    else:
        raise Exception("unknown command %s" % cmd)
