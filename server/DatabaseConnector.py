import os
import psycopg2
from sqlalchemy import create_engine, func, and_, MetaData
from geoalchemy2 import Geometry
from sqlalchemy.orm import sessionmaker
from models import Base

POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS", "postgres")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    POSTGRES_USER,
    POSTGRES_PASS,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

class DatabaseConnector:
        class ___PrivateConnection:
            def __init__(self):
                self.engine = self.__create_engine()
                self.session = self.__create_session()

            def __create_engine(self):
                return create_engine(SQLALCHEMY_DATABASE_URI, echo=False)

            def __create_session(self):
                Base.metadata.create_all(self.engine)
                Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
                conn = self.engine.connect()
                session = Session(bind=conn)
                return session

        singleton_session = None
        def __init__(self, debug=False):
            if DatabaseConnector.singleton_session is None:
                DatabaseConnector.singleton_session = DatabaseConnector.___PrivateConnection()
            self.debug = debug

        def make_tables(self):
            Base.metadata.create_all(self.singleton_session.engine)
        # Format string for timestamps in retrieved data.

        def __initialize_session_if_closed(self):
            if DatabaseConnector.singleton_session is None:
                DatabaseConnector.singleton_session = DatabaseConnector.___PrivateConnection()


        def try_add_and_commit(self, model_to_add):
            self.__initialize_session_if_closed()
            # with self.lock:
            try:
                DatabaseConnector.singleton_session.session.add(model_to_add)
                DatabaseConnector.singleton_session.session.commit()
                print('DatabaseConnector.try_add_and_commit: Added model '+str(model_to_add)+'to db')
                return model_to_add
            except psycopg2.IntegrityError as e:
                print(e)
                print('DatabaseConnector.try_add_and_commit: Failed to add model '+str(model_to_add)+'to db')
                DatabaseConnector.singleton_session.session.rollback()
                return None

        def try_add_and_flush(self, model_to_add):
            self.__initialize_session_if_closed()
            # with self.lock:
            try:
                DatabaseConnector.singleton_session.session.add(model_to_add)
                DatabaseConnector.singleton_session.session.flush()
                print('DatabaseConnector.try_add_and_commit: Added model '+str(model_to_add)+'to session')
                return True
            except psycopg2.IntegrityError as e:
                print(e)
                print('DatabaseConnector.try_add_and_commit: Failed to add model '+str(model_to_add)+'to session')
                DatabaseConnector.singleton_session.session.rollback()
                return False

        def commit(self):
            self.__initialize_session_if_closed()
            try:
                DatabaseConnector.singleton_session.session.commit()
                print("Succesfully committed.")
                return True
            except psycopg2.IntegrityError as e:
                print(e)
                print("DatabaseConnector.commit(): failed to commit. Rolling back...")
                DatabaseConnector.singleton_session.session.rollback()
                return False

        def get_session(self):
            return self.singleton_session.session

        def get_engine(self):
            return self.singleton_session.engine