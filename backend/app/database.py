import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
SQLALCHEMY_DATABASE_URL = os.getenv("postgresql://gaah_bookkeeping_db_user:tnpETXEeKhDJ7tbeP7nuHE2uAxsqTlZi@dpg-d461tushg0os73e9g1h0-a/gaah_bookkeeping_db").replace("postgres://", "postgresql://", 1)
=======
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./medical.db')
>>>>>>> 1c071df926c702b72a64ef539685c19e319a01de
connect_args = {}
if DATABASE_URL.startswith('sqlite:///'):
    connect_args = {'check_same_thread': False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
