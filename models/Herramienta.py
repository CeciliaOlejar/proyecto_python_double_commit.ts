from db.Conexion import Conexion
from logger.logger_base import log


class Herramineta:

    _SELECCIONAR_HERRAMIENTAS = "SELECT * FROM herramienta ORDER BY id_herramienta"
    _INSERTAR_HERRAMIENTA = "INSERT INTO herramienta(nombre, descripcion, precio_por_dia, disponible) VALUES (%s,%s,%s,%s)"
    _ACTUALIZAR_HERRAMIENTA = "UPDATE herramienta SET nombre=%s descripcion=%s precio_por_dia=%s disponible=%s"
    _ELIMINAR_HERRAMINETA = "DELETE FROM herramienta WHERE id_herramienta=%s"

    def __init__(self, nombre, descripcion, precio_por_dia, disponible=True):
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio_por_dia = precio_por_dia
        self._disponible = disponible

    def __str__(self):
        return f"""
        Herramienta: {self._nombre} - ${self._precio_por_dia}/día
        Descripción: {self._descripcion}
        Estado: {self._disponible}
        """

    @classmethod
    def listar_herramientas(cls) -> list:
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    # Seleccionamos las herramientas de la base de datos
                    cursor.execute(cls._SELECCIONAR_HERRAMIENTAS)
                    registros = cursor.fetchall()
                    herramientas = []
                    for registro in registros:
                        herramientas.append(registro)
                    return herramientas
        except Exception as e:
            log.error(f"Error al listar herramientas: {e}")
            return []

    @classmethod
    def agregar_herramienta(cls, nombre, descripcion, precio_por_dia, disponible=True) -> int:
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    # Verificar si la herramienta ya existe
                    cursor.execute("SELECT * FROM herramienta WHERE nombre=%s", (nombre,))
                    if cursor.fetchone() is not None:
                        log.error(f"La herramienta '{nombre}' ya existe.")
                        return
                    # Insertar nueva herramienta
                    log.info(f"Agregando herramienta: {nombre}")
                    if not nombre or precio_por_dia <= 0:
                        log.error("Datos inválidos para agregar herramienta.")
                        return
                    cursor.execute(cls._INSERTAR_HERRAMIENTA, (nombre, descripcion, precio_por_dia, disponible))
                    return cursor.lastrowid
        except Exception as e:
            log.error(f"Error al agregar herramienta: {e}")