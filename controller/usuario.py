from db.conexion import Conexion
from models.Usuario import Usuario
from colorama import Fore, Style

class Usuario_DAO:
    _SELECCIONAR_USUARIO = "SELECT * FROM usuario ORDER BY id_usuario"
    _INSERTAR_USUARIO = """
    INSERT INTO usuario(nombre, apellido, email, contrasena)
    VALUES (%s, %s, %s, %s)
    """
    _ACTUALIZAR_USUARIO = """
    UPDATE usuario
    SET nombre=%s, apellido=%s, email=%s, contrasena=%s
    WHERE id_usuario=%s
    """
    _ELIMINAR_USUARIO = "DELETE FROM usuario WHERE id_usuario=%s"

    @classmethod
    def crear_usuario(cls, usuario: Usuario):
        """Inserta un nuevo usuario en la base de datos."""
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    cursor.execute(cls._INSERTAR_USUARIO, (usuario.nombre, usuario.apellido, usuario.email, usuario.contrasena))
                    print(f"{Fore.GREEN}{Style.BRIGHT}Usuario creado exitosamente.{Style.RESET_ALL}")
        except Exception as e:
            print(f"Error al crear usuario: {e}")

    @classmethod
    def leer_usuarios(cls):
        """Obtiene todos los usuarios de la base de datos."""
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
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
                    cursor.execute(cls._ACTUALIZAR_USUARIO, (usuario.nombre, usuario.apellido, usuario.email, usuario.contrasena, usuario.id_usuario))
                    print("Usuario actualizado exitosamente.")
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        """Elimina un usuario de la base de datos por su ID."""
        try:
            with Conexion.obtener_conexion():
                with Conexion.obtener_cursor() as cursor:
                    cursor.execute("SELECT nombre FROM usuario WHERE id_usuario=%s", (str(id_usuario),))
                    usuario = cursor.fetchone()
                    if not usuario:
                        print(f"Usuario inexistente: {usuario}")
                        return
                    print(usuario)
                    cursor.execute(cls._ELIMINAR_USUARIO, (id_usuario,))
                    print(f"El usuario: {usuario}, se ha eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")