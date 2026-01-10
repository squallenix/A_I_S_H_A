import mysql.connector
from mysql.connector import pooling
from dbconfig import DB_CONFIG

class DatabaseConnection:
    _pool=None
    @classmethod
    def init_pool(cls):
        if cls._pool is None:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                **DB_CONFIG
            )
    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.init_pool()
        return cls._pool.get_connection()