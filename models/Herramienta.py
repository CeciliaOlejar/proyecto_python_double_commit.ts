from db.Conexion import Conexion
from logger.logger_base import log

class Herramineta():
    
    _SELECCIONAR_HERRAMIENTAS = "SELECT * FROM herramienta ORDER BY id_herramienta"
    
    def __init__(self, nombre, descripcion, precio_por_dia, disponible=True):
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio_por_dia = precio_por_dia
        self._disponible = disponible
        
    def __str__(self):
        return f'''
        Herramienta: {self._nombre} - ${self._precio_por_dia}/día
        Descripción: {self._descripcion}
        Estado: {self._disponible}
        '''
    
    @classmethod
    def listar_herramienta(cls):
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    registros = cursor.execute(cls._SELECCIONAR_HERRAMIENTAS)
                    return registros.fetchall()
        except Exception as e:
            log.error(f"Error al listar herramientas: {e}")
            return []
