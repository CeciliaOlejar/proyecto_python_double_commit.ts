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
        registro = Usuario(nombre, apellido, email, contrasenia)
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
        ingreso_usuario = Usuario(nombre, apellido, email, contrasenia)
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
