from colorama import init, Style, Fore
from models.Usuario import Usuario
from utils.efecto import consola
import getpass, textwrap

init()
class Menu:
    @staticmethod
    def principal():
        text = textwrap.dedent(f"""
        {Fore.GREEN}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                   Bienvenido a Construrent                 ║
        ║                  Alquiler de Herramientas 🔧               ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Iniciar sesión                                         ║
        ║  2. Registrarse                                            ║
        ║  3. Explorar herramientas disponibles                      ║
        ║  4. Preguntar a RentaBot (asistente IA)                    ║
        ║  5. Salir                                                  ║
        ╚════════════════════════════════════════════════════════════╝
        """)
        consola(text)

    @staticmethod
    def opcion() -> int:
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-5): {Style.RESET_ALL}")
        return int(opcion)

    @staticmethod
    def registro():
        text = textwrap.dedent(f"""
        {Fore.BLUE}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                    Registro de usuario                     ║
        ╠════════════════════════════════════════════════════════════╣
        {Style.RESET_ALL}""")
        consola(text)
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Usuario: {Style.RESET_ALL}""", end="")
        nombre = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Apellido: {Style.RESET_ALL}""", end="")
        apellido = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Email: {Style.RESET_ALL}""", end="")
        email = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Contraseña: {Style.RESET_ALL}""", end="")
        contrasenia = getpass.getpass("") # Esta función es para ocultar la contraseña
        print(textwrap.dedent(f"""{Fore.BLUE}╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}
        """))
        registro = Usuario(nombre, apellido, email, contrasenia, 2)  # Rol por defecto es 2 (usuario normal)
        return registro

    @staticmethod
    def login():
        text = textwrap.dedent(f"""
        {Fore.BLUE}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                     Ingreso de usuario                     ║
        ╠════════════════════════════════════════════════════════════╣
        {Style.RESET_ALL}""")
        consola(text)
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Usuario: {Style.RESET_ALL}""", end="")
        nombre = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Apellido: {Style.RESET_ALL}""", end="")
        apellido = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Email: {Style.RESET_ALL}""", end="")
        email = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Contraseña: {Style.RESET_ALL}""", end="")
        contrasenia = getpass.getpass("") # Esta función es para ocultar la contraseña
        print(textwrap.dedent(f"""{Fore.BLUE}╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}
        """))
        ingreso_usuario = Usuario(nombre.strip(), apellido.strip(), email.strip(), contrasenia.strip())
        return ingreso_usuario

    @staticmethod
    def explorar_herramientas():
        text = textwrap.dedent(f"""
        {Fore.MAGENTA}{Style.BRIGHT}
        
        ╔════════════════════════════════════════════════════════════╗
        ║               Explorar Herramientas Disponibles            ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Listar todas las herramientas                          ║
        ║  2. Buscar por nombre                                      ║
        ║  3. Volver al menú principal                               ║
        ╚════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}""")
        consola(text)
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-4): {Style.RESET_ALL}")
        return int(opcion)

    @staticmethod
    def menu_admin():
        text = textwrap.dedent(
            f"""
        {Fore.RED}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                  Panel de Administración                   ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Gestionar usuarios                                     ║
        ║  2. Gestionar herramientas                                 ║
        ║  3. Gestionar Tickets                                      ║
        ║  4. Volver al menú principal                               ║
        ╚════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}"""
        )
        consola(text)
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-4): {Style.RESET_ALL}")
        return int(opcion)

    @staticmethod
    def menu_gestionar_usuarios():
        text = textwrap.dedent(f"""
        {Fore.CYAN}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                   Gestión de Usuarios                      ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Listar usuarios                                        ║
        ║  2. Registrar usuario admin                                ║
        ║  3. Eliminar usuario                                       ║
        ║  4. Modificar usuario                                      ║ 
        ║  5. Volver al menú anterior                                ║
        ╚════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}""")
        consola(text)
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-5): {Style.RESET_ALL}")
        return int(opcion)

    @staticmethod
    def menu_gestionar_herramientas():
        text = textwrap.dedent(f"""
        {Fore.YELLOW}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                Gestión de Herramientas                     ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Listar herramientas                                    ║
        ║  2. Registrar herramienta                                  ║
        ║  3. Eliminar herramienta                                   ║
        ║  4. Modificar herramienta                                  ║
        ║  5. Volver al menú anterior                                ║
        ╚════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}""")
        consola(text)
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-5): {Style.RESET_ALL}")
        return int(opcion)

    @staticmethod
    def menu_gestionar_tickets():
        text = textwrap.dedent(f"""
        {Fore.MAGENTA}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                   Gestión de Tickets                       ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Listar tickets                                         ║
        ║  2. Buscar ticket por ID                                   ║
        ║  3. Eliminar ticket                                        ║
        ║  4. Modificar ticket                                       ║
        ║  5. Volver al menú anterior                                ║
        ╚════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}""")
        consola(text)
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-5): {Style.RESET_ALL}")
        return int(opcion)
    
    @staticmethod
    def menu_usuario(usuario: Usuario):
        text = textwrap.dedent(f"""
        {Fore.GREEN}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                  Dashboard {usuario.nombre}                        
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Listar herramientas                                    ║
        ║  2. Salir                                                  ║
        ╚════════════════════════════════════════════════════════════╝
        {Style.RESET_ALL}""")
        consola(text)
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-2): {Style.RESET_ALL}")
        return int(opcion)