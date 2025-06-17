from db.conexion import Conexion


class Herramienta:

    _SELECCIONAR_HERRAMIENTAS = "SELECT * FROM herramienta ORDER BY id_herramienta"
    _INSERTAR_HERRAMIENTA = "INSERT INTO herramienta(nombre, descripcion, precio_por_dia, disponible) VALUES (%s,%s,%s,%s)"
    _ACTUALIZAR_HERRAMIENTA = "UPDATE herramienta SET nombre=%s descripcion=%s precio_por_dia=%s disponible=%s"
    _ELIMINAR_HERRAMIENTA = "DELETE FROM herramienta WHERE id_herramienta=%s"

    def _init_(self, nombre, tipo, descripcion, marca, modelo, fecha_adquisicion, ubicacion, precio_por_dia, estado=True):
        self._nombre = nombre
        self._tipo = tipo
        self._descripcion = descripcion
        self._marca = marca
        self._modelo = modelo
        self._fecha_adquisicion = fecha_adquisicion
        self._ubicacion = ubicacion
        self._precio_por_dia = precio_por_dia
        self._estado = estado

    def _str_(self):
        return f"""
        Herramienta: {self._nombre} - ${self._precio_por_dia}/día
        Tipo: {self._tipo}
        Descripción: {self._descripcion}
        Marca: {self._descripcion}
        Modelo: {self._modelo}
        Fecha Adquisición: {self._fecha_adquisicion}
        Ubicación: {self._ubicacion}
        Estado: {self._estado}
        """

    @classmethod
    def listar_herramientas(cls) -> list:
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    cursor.execute(cls._SELECCIONAR_HERRAMIENTAS)
                    registros = cursor.fetchall()
                    return registros
        except Exception as e:
            print(f"Error al listar herramientas: {e}")
            return []

    @classmethod
    def agregar_herramienta(
        cls, nombre, descripcion, precio_por_dia, disponible=True
    ) -> int:
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    # Verificar si la herramienta ya existe
                    cursor.execute(
                        "SELECT * FROM herramienta WHERE nombre=%s", (nombre,)
                    )
                    if cursor.fetchone() is not None:
                        print(f"La herramienta '{nombre}' ya existe.")
                        return
                    # Insertar nueva herramienta
                    print(f"Agregando herramienta: {nombre}")
                    if not nombre or precio_por_dia <= 0:
                        print("Datos inválidos para agregar herramienta.")
                        return
                    cursor.execute(
                        cls._INSERTAR_HERRAMIENTA,
                        (nombre, descripcion, precio_por_dia, disponible),
                    )
                    return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar herramienta: {e}")
            
    @classmethod
    def eliminar(cls, id_herramienta):
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    cursor.execute("SELECT nombre FROM herramienta WHERE id_herramienta=%s", (id_herramienta,))
                    id, nombre = cursor.fetchone()
                    if not id:
                        print(f"ID de herramienta inexistente {id_herramienta}")
                        return
                    cursor.execute(cls._ELIMINAR_HERRAMIENTA, (id_herramienta,))
                    return cursor.rowcount, nombre
        except Exception as e:
            print(f"Ocurrió un error {e}")
