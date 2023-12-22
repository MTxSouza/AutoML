"""
Database configuration script to initialize 
and set up the local database using SQLAlquemy 
library.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# taking absolute path
path = os.path.dirname(p=os.path.abspath(path=__file__))

# creating database engine
ENGINE = create_engine(url=f"sqlite+pysqlite:///{path}/db.sqlite3", echo=False)
Base = declarative_base()

# creating session
Session = sessionmaker(bind=ENGINE)
