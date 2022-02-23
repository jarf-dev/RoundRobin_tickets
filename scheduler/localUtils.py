import pymysql
from sqlalchemy.sql import select, insert, update, delete
from sqlalchemy import create_engine, select, MetaData, Table
import configparser
import os

from dotenv import load_dotenv
load_dotenv()

config = configparser.ConfigParser()
config.read('conf.cfg')

dbType = config['database-settings']['DBTYPE']

def dbConnection():
    if dbType == 'sqlite':
        DB_PATH = os.getenv("SQLITE_DB_PATH")
        return create_engine(f'sqlite:///{DB_PATH}', echo=False)
    if dbType == 'postgres':
        USER = os.getenv("POST_DB_USER")
        PASS = os.getenv("POST_DB_PASS")
        SERVER = os.getenv("POST_DB_SERVER")
        PORT = os.getenv("POST_DB_PORT")
        SCHEMA = os.getenv("POST_DB_SCHEMA")
        return create_engine(f'postgresql://{USER}:{PASS}@{SERVER}:{PORT}/{SCHEMA}', echo=False)
    if dbType == 'mysql':
        USER = os.getenv("MYSQL_DB_USER")
        PASS = os.getenv("MYSQL_DB_PASS")
        SERVER = os.getenv("MYSQL_DB_SERVER")
        PORT = os.getenv("MYSQL_DB_PORT")
        SCHEMA = os.getenv("MYSQL_DB_SCHEMA")
        return create_engine(f'mysql+pymysql://{USER}:{PASS}@{SERVER}:{PORT}/{SCHEMA}', echo=False)


def selectRecordTable(table, id=None, idRutina=None):
    # load work database
    engine = dbConnection()
    meta = MetaData()
    meta.reflect(bind=engine)
    table = Table(table, meta, autoload=True, autoload_with=engine)

    if id:
        stmt = select(table).where(table.columns.id == id)
    elif idRutina:
        stmt = select(table).where(table.columns.idRutina == idRutina)
    else:
        stmt = select(table)

    conn = engine.connect()
    results = conn.execute(stmt).fetchall()
    conn.close()

    results = [dict(r) for r in results]

    return results


def insertRecordTable(table, **kwargs):
    # load work database
    engine = dbConnection()
    meta = MetaData()
    meta.reflect(bind=engine)
    table = Table(table, meta, autoload=True, autoload_with=engine)

    stmt = (insert(table)
            .values(kwargs))
    conn = engine.connect()
    result = conn.execute(stmt)
    new_id = result.inserted_primary_key[0]
    conn.close()
    return new_id


def updateRecordTable(table, id, **kwargs):
    # load work database
    engine = dbConnection()
    meta = MetaData()
    meta.reflect(bind=engine)
    table = Table(table, meta, autoload=True, autoload_with=engine)

    stmt = (update(table).
            where(table.columns.id == id).
            values(kwargs)
            )

    conn = engine.connect()
    conn.execute(stmt)
    conn.close()


def deleteRecordTable(table, id, all=None):
    # load work database
    engine = dbConnection()
    meta = MetaData()
    meta.reflect(bind=engine)
    table = Table(table, meta, autoload=True, autoload_with=engine)

    if all:
        stmt = (
            delete(table).
            where(table.columns.idRutina == id)
        )
    else:
        stmt = (
            delete(table).
            where(table.columns.id == id)
        )

    conn = engine.connect()
    conn.execute(stmt)
    conn.close()

if __name__=="__main__":
    pass