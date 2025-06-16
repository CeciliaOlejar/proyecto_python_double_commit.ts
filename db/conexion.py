import psycopg2 as bd
import sys


class Conexion:
    _DATABASE = "contrurent"
    _USERNAME = "postgres"
    _PASSWORD = "32088028..mGc"
    _PORT = "5432"
    _HOST = "127.0.0.1"
    _conexion = None
    _cursor = None

    @classmethod
    def obtener_conexion(cls):
        if cls._conexion is None:
            try:
                cls._conexion = bd.connect(
                    host=cls._HOST,
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    port=cls._PORT,
                    database=cls._DATABASE,
                )
                return cls._conexion
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                sys.exit()
        else:
            return cls._conexion

    @classmethod
    def obtener_cursor(cls):
        if cls._cursor is None:
            try:
                cls._cursor = cls.obtener_conexion().cursor()
                return cls._cursor
            except Exception as e:
                print(f"Ocurrió un error: {e}")
                sys.exit()
        else:
            return cls._cursor