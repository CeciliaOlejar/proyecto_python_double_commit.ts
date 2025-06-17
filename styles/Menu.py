from colorama import init, Style, Fore
from models.Herramienta import Herramienta
from utils.efecto import consola
import getpass, os

init()
class Menu:
    @staticmethod
    def principal():
        text = f"""
        {Fore.GREEN}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                   Bienvenido a Construrent                  ║
        ║                  Alquiler de Herramientas 🔧               ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Iniciar sesión                                         ║
        ║  2. Registrarse                                            ║
        ║  3. Explorar herramientas disponibles                      ║
        ║  4. Preguntar a RentaBot (asistente IA)                    ║
        ║  5. Salir                                                  ║
        ╚════════════════════════════════════════════════════════════╝
        """
        consola(text)
    
    @staticmethod
    def opcion() -> int:
        opcion = input(f"{Fore.YELLOW}Selecciona una opción (1-5): {Style.RESET_ALL}")
        return int(opcion)
    
    @staticmethod
    def registro():
        text = f"""
        {Fore.BLUE}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                    Registro de usuario                     ║
        ╠════════════════════════════════════════════════════════════╣
        {Style.RESET_ALL}"""
        consola(text)
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Usuario: {Style.RESET_ALL}""", end="")
        username = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Email: {Style.RESET_ALL}""", end="")
        email = input()
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Contraseña: {Style.RESET_ALL}""", end="")
        password = getpass.getpass("")
        print(f"""{Fore.BLUE}        ╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}
        """)
        registro = { username, password, email, password }
        return registro

    @staticmethod
    def login():
        text = f"""
        {Fore.BLUE}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                    Ingreso a la cuenta                     ║
        ╠════════════════════════════════════════════════════════════╣
        ║ {Fore.CYAN}Usuario:                                                 ║
        ║ {Fore.CYAN}Contraseña:                                                ║
        ╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}
        """
        consola(text)
    
    def asistente(username):
        text = f"""{Fore.GREEN}
        ╔══════════════════════════════════════════════════════╗
        ║                                                      ║
        ║   👋 ¡Hola, {username}!                                   ║
        ║                                                      ║
        ║   💬 Puedes preguntarme lo que quieras               ║
        ║   💡 Estoy aquí para ayudarte                        ║
        ║   🚪 Escribe 'salir' para terminar                   ║
        ║                                                      ║
        ╚══════════════════════════════════════════════════════╝
        {Style.RESET_ALL}"""
        consola(text)
    
    @staticmethod
    def mostrar_herramientas(herramientas: list):
        try:
            ancho_consola = os.get_terminal_size().columns
            titulo = "Herramientas Disponibles"
            separador = "═" * (ancho_consola - 2)
            espacio_titulo = (ancho_consola - len(titulo) - 2) // 2

            text = f"""
    {Fore.GREEN}{Style.BRIGHT}╔{separador}╗
    ║{' ' * espacio_titulo}{titulo}{' ' * (ancho_consola - len(titulo) - 2 - espacio_titulo)}║
    ╠{separador}╣
    """

            for idx, herramienta in enumerate(herramientas, 1):
                id_, nombre, tipo, descripcion, marca, modelo, *_ = herramienta
                resumen = f"{idx}. {nombre} ({tipo}) - {marca}, Modelo {modelo}"
                espacio = ancho_consola - len(resumen) - 4
                espacio = max(0, espacio)
                text += f"║ {Fore.CYAN}{resumen}{' ' * espacio}{Fore.GREEN}║\n"

            text += f"""╚{separador}╝
    {Fore.YELLOW}Selecciona una herramienta por número o presiona Enter para volver.{Style.RESET_ALL}
    """
            consola(text)
        except Exception as e:
            print(f"Ocurrió un error: {e}")

