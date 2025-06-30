from db.conexion import Conexion
from models.Herramienta import Herramienta
from colorama import Fore, Style


class Herramienta_DAO:
    _SELECCIONAR_HERRAMIENTAS = "SELECT * FROM herramienta ORDER BY id_herramienta"
    _INSERTAR_HERRAMIENTA = "INSERT INTO herramienta(nombre, tipo, descripcion, marca, modelo, fecha_adquisicion, ubicacion, precio_por_dia, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    _ACTUALIZAR_HERRAMIENTA = """
    UPDATE herramienta
    SET nombre=%s,
        tipo=%s,
        descripcion=%s,
        marca=%s,
        modelo=%s,
        fecha_adquisicion=%s,
        ubicacion=%s,
        precio_por_dia=%s,
        estado=%s
    WHERE id_herramienta=%s
    """
    _ELIMINAR_HERRAMIENTA = "DELETE FROM herramienta WHERE id_herramienta=%s"

    @classmethod
    def listar_herramientas(cls) -> list:
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(cls._SELECCIONAR_HERRAMIENTAS)
                registros = cursor.fetchall()
                herramientas = []
                for registro in registros:
                    herramienta = Herramienta(
                        registro[1],
                        registro[2],
                        registro[3],
                        registro[4],
                        registro[5],
                        registro[6],
                        registro[7],
                        registro[8],
                        registro[9],
                        registro[0],
                    )
                    herramientas.append(herramienta)
                return herramientas
        except Exception as e:
            print(
                f"{Fore.RED}{Style.BRIGHT}Error al listar herramientas: {e}{Style.RESET_ALL}"
            )
            return []

    @classmethod
    def agregar_herramienta(cls, herramienta: Herramienta) -> int:
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT * FROM herramienta WHERE modelo=%s",
                    (herramienta.modelo,),
                )
                if cursor.fetchone() is not None:
                    print(
                        f"La herramienta con el siguiente '{herramienta.modelo}' ya existe."
                    )
                    return
                if (
                    not herramienta.nombre
                    or herramienta.precio_por_dia <= 0
                    or not herramienta.marca
                ):
                    print("Datos inválidos para agregar herramienta.")
                    return
                cursor.execute(
                    cls._INSERTAR_HERRAMIENTA,
                    (
                        herramienta.nombre,
                        herramienta.tipo,
                        herramienta.descripcion,
                        herramienta.marca,
                        herramienta.modelo,
                        herramienta.fecha_adquisicion,
                        herramienta.ubicacion,
                        herramienta.precio_por_dia,
                        herramienta.estado,
                    ),
                )
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}Se ha agregado la siguiente herramienta:{Style.RESET_ALL}"
                )
                print(
                    f"{Fore.WHITE}{Style.BRIGHT}{herramienta}{Style.RESET_ALL}"
                )
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar herramienta: {e}")

    @classmethod
    def actualizar_herramienta(cls, herramienta: Herramienta):
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    cls._ACTUALIZAR_HERRAMIENTA,
                    (
                        herramienta.nombre,
                        herramienta.tipo,
                        herramienta.descripcion,
                        herramienta.marca,
                        herramienta.modelo,
                        herramienta.fecha_adquisicion,
                        herramienta.ubicacion,
                        herramienta.precio_por_dia,
                        herramienta.estado,
                        herramienta.id_herramienta,
                    ),
                )
                conexion.commit()
                print(f"{Fore.GREEN}{Style.BRIGHT}Herramienta actualizada correctamente.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}Ocurrió un error {e}{Style.RESET_ALL}")

    @classmethod
    def eliminar(cls, id_herramienta):
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT nombre FROM herramienta WHERE id_herramienta=%s",
                    (id_herramienta,),
                )
                id, nombre = cursor.fetchone()
                if not id:
                    print(
                        f"{Fore.YELLOW}{Style.BRIGHT}ID de herramienta inexistente {id_herramienta}{Style.RESET_ALL}"
                    )
                    return
                cursor.execute(cls._ELIMINAR_HERRAMIENTA, (id_herramienta,))
                return cursor.rowcount, nombre
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}Ocurrió un error {e}{Style.RESET_ALL}")

    @classmethod
    def buscar_por_nombre(cls, nombre: str) -> list:
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                consulta = "SELECT * FROM herramienta WHERE LOWER(nombre) LIKE %s"
                cursor.execute(consulta, (f"%{nombre.lower()}%",))
                registros = cursor.fetchall()
                herramientas = []
                for registro in registros:
                    herramienta = Herramienta(
                        registro[0],
                        registro[1],
                        registro[2],
                        registro[3],
                        registro[4],
                        registro[5],
                        registro[6],
                        registro[7],
                        registro[8],
                        registro[9],
                    )
                    herramientas.append(herramienta)
                return herramientas
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}Error al buscar herramienta: {e}{Style.RESET_ALL}")
            return []
