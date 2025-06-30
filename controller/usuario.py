import textwrap
from db.conexion import Conexion
from models.Usuario import Usuario
from styles.Menu import Menu
from colorama import Fore, Style
from utils.ubicacion import obtener_ubicacion


class Usuario_DAO:
    _usuario_actual = None
    _SELECCIONAR_USUARIO = "SELECT * FROM usuario ORDER BY id_usuario"
    _INSERTAR_USUARIO = """
    INSERT INTO usuario(nombre, apellido, email, contrasenia, rol)
    VALUES (%s, %s, %s, %s, %s)
    """
    _VERIFICAR_USUARIO = "SELECT id_usuario, nombre, apellido, email, contrasenia, rol FROM usuario WHERE email=%s AND contrasenia=%s"

    _ACTUALIZAR_USUARIO = """
    UPDATE usuario
    SET nombre=%s, apellido=%s, email=%s, contrasenia=%s, rol=%s,
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
                        usuario.rol,
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

    @classmethod
    def ingresar(cls, usuario: Usuario):
        try:
            while True:
                with Conexion.obtener_conexion() as conexion:
                    cursor = conexion.cursor()

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
                            print(
                                f"{Fore.YELLOW}Volviendo al menú principal...{Style.RESET_ALL}"
                            )
                            return
                    usuario_db = usuarios_existentes[0]
                    usuario.id_usuario = usuario_db[0]
                    usuario.nombre = usuario_db[1]
                    usuario.apellido = usuario_db[2]
                    usuario.email = usuario_db[3]
                    usuario.contrasenia = usuario_db[4]
                    usuario.rol = usuario_db[5]
                    print(
                        textwrap.dedent(f"{Fore.YELLOW}{Style.BRIGHT}Has ingresado a ConstruRent como: {usuario}{Style.RESET_ALL}"
                    ))
                    print("")
                    cls.set_usuario_actual(usuario)
                    return usuario, usuario.rol # Salir del bucle si el usuario es válido
        except Exception as e:
            print(f"Ocurrió un error al ingresar a la app: {e}")
            return

    @classmethod
    def leer_usuarios(cls):
        """Obtiene todos los usuarios de la base de datos."""
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(cls._SELECCIONAR_USUARIO)
                registros = []
                usuarios = cursor.fetchall()
                if usuarios:
                    for usuario in usuarios:
                        id_usuario, nombre, apellido, email, contrasenia, rol = usuario
                        registro = Usuario(
                            nombre=nombre,
                            apellido=apellido,
                            email=email,
                            contrasenia=contrasenia,
                            rol=rol,
                            id_usuario=id_usuario,
                        )
                        registros.append(registro)
                return registros
        except Exception as e:
            print(f"Error al leer usuarios: {e}")
            return []

    @classmethod
    def actualizar_usuario(cls, usuario: Usuario):
        """Actualiza los datos de un usuario existente."""
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                registros_existentes = cursor.fetchall()
                if not registros_existentes:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}No hay usuarios")
                    return
                for registro in registros_existentes:
                    registro = Usuario(nombre=registro[1], apellido=registro[2], email=registro[3], contrasenia=registro[4], rol=registro[5])
                    if registro:
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
                        print(f" {Fore.GREEN}{Style.BRIGHT}Usuario actualizado exitosamente: {usuario}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}{Style.BRIGHT}No existe el usuario a actualizar.{Style.RESET_ALL}")
                        continue
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")

    @classmethod
    def eliminar_usuario(cls, id_usuario: int):
        """Elimina un usuario de la base de datos por su ID."""
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "SELECT * FROM usuario WHERE id_usuario=%s", (str(id_usuario),)
                )
                usuario = cursor.fetchone()
                if not usuario:
                    print(f"Usuario inexistente: {usuario}")
                    return
                usuario_eliminado = Usuario(usuario[1], usuario[2], usuario[3], "•••••••", usuario[5], usuario[0])
                print(f"{Fore.GREEN}{Style.BRIGHT}\nEl usuario: {usuario_eliminado}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{Style.BRIGHT}Se ha eliminado {cursor.rowcount} registro/s exitosamente")
                cursor.execute(cls._ELIMINAR_USUARIO, (id_usuario,))
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
