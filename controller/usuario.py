from controller.herramienta import Herramienta_DAO
from db.conexion import Conexion
from models.Usuario import Usuario
from styles.Menu import Menu
from colorama import Fore, Style
from utils.ubicacion import obtener_ubicacion


class Usuario_DAO:
    _usuario_actual = None 
    _SELECCIONAR_USUARIO = "SELECT * FROM usuario ORDER BY id_usuario"
    _INSERTAR_USUARIO = """
    INSERT INTO usuario(nombre, apellido, email, contrasenia)
    VALUES (%s, %s, %s, %s)
    """
    _VERIFICAR_USUARIO = (
        "SELECT email, contrasenia FROM usuario WHERE email=%s AND contrasenia=%s"
    )
    _ACTUALIZAR_USUARIO = """
    UPDATE usuario
    SET nombre=%s, apellido=%s, email=%s, contrasenia=%s
    WHERE id_usuario=%s
    """
    _ELIMINAR_USUARIO = "DELETE FROM usuario WHERE id_usuario=%s"

    @classmethod
    def crear_usuario(cls, usuario: Usuario):
        """Inserta un nuevo usuario en la base de datos."""
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    cls._INSERTAR_USUARIO,
                    (
                        usuario.nombre,
                        usuario.apellido,
                        usuario.email,
                        usuario.contrasenia,
                    ),
                )
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}Usuario creado exitosamente.{Style.RESET_ALL}"
                )
                print(f"{Fore.BLUE}{Style.BRIGHT}{usuario}{Style.RESET_ALL}")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            
    @classmethod
    def set_usuario_actual(cls, usuario: Usuario):
        cls._usuario_actual = usuario

    @classmethod
    def obtener_usuario_actual(cls):
        return cls._usuario_actual

# ...existing code...
    @classmethod
    def ingresar(cls, usuario: Usuario, Chat: object):
        try:
            while True:
                with Conexion.obtener_conexion():
                    with Conexion.obtener_cursor() as cursor:
                        cursor.execute(
                            cls._VERIFICAR_USUARIO,
                            (
                                usuario.email,
                                usuario.contrasenia,
                            ),
                        )
                        usuarios_existentes = cursor.fetchall()
                        if not usuarios_existentes:
                            print(
                                f"{Fore.YELLOW}{Style.BRIGHT}Datos incorrectos. ¿Desea intentar de nuevo? (s/n){Style.RESET_ALL}"
                            )
                            opcion = input().lower()
                            if opcion in ["Si", "s", "si"]:
                                usuario = Menu.login()  # Vuelve a pedir los datos
                                continue
                            else:
                                print(f"{Fore.YELLOW}Volviendo al menú principal...{Style.RESET_ALL}")
                                return
                        print(
                            f"{Fore.YELLOW}{Style.BRIGHT}Has ingresado a ConstruRent como: {usuario.nombre}{Style.RESET_ALL}"
                        )
                        cls.set_usuario_actual(usuario)
                        catalogo = Herramienta_DAO.listar_herramientas()
                        ciudad, pais = obtener_ubicacion()
                        Chat.iniciar(usuario.nombre, catalogo, ciudad, pais)
                        break
        except Exception as e:
            print(f"Ocurrió un error al ingresar a la app: {e}")
            
    @classmethod
    def leer_usuarios(cls):
        """Obtiene todos los usuarios de la base de datos."""
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(cls._SELECCIONAR_USUARIO)
                usuarios = cursor.fetchall()
                return usuarios
        except Exception as e:
            print(f"Error al leer usuarios: {e}")
            return []

    @classmethod
    def actualizar_usuario(cls, usuario: Usuario):
        """Actualiza los datos de un usuario existente."""
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    cursor.execute(
                        cls._ACTUALIZAR_USUARIO,
                        (
                            usuario.nombre,
                            usuario.apellido,
                            usuario.email,
                            usuario.contrasenia,
                            usuario.id_usuario,
                        ),
                    )
                    print("Usuario actualizado exitosamente.")
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        """Elimina un usuario de la base de datos por su ID."""
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT nombre FROM usuario WHERE id_usuario=%s", (str(id_usuario),)
                )
                usuario = cursor.fetchone()
                if not usuario:
                    print(f"Usuario inexistente: {usuario}")
                    return
                print(usuario)
                cursor.execute(cls._ELIMINAR_USUARIO, (id_usuario,))
                print(f"El usuario: {usuario}, se ha eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")

