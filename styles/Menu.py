from colorama import init, Style, Fore
from utils.efecto import consola
import getpass

init()

class Menu:
    @staticmethod
    def principal():
        text = f"""
        {Fore.GREEN}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                   Bienvenido a Contrurent                  ║
        ║                  Alquiler de Herramientas 🔧               ║
        ╠════════════════════════════════════════════════════════════╣
        ║  1. Iniciar sesión                                         ║
        ║  2. Registrarse                                            ║
        ║  3. Explorar herramientas disponibles                      ║
        ║  4. Preguntar a Kai (asistente IA)                         ║
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
        text = f"""{Fore.YELLOW}
        ╔══════════════════════════════════════════════════════╗
        ║                                                      ║
        ║   🌟 ¡BIENVENIDO A TU ASISTENTE VIRTUAL! 🌟          ║
        ║                                                      ║
        ╠══════════════════════════════════════════════════════╣
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
    def mostrar_herramientas(herramientas):
        text = f"""
        {Fore.MAGENTA}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║               Herramientas Disponibles                    ║
        ╠════════════════════════════════════════════════════════════╣
        """
        for idx, herramienta in enumerate(herramientas, 1):
            text += f"{Fore.CYAN}║  {idx}. {herramienta:<55}{Fore.MAGENTA}║\n"
        text += f"""╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Selecciona una herramienta por número o presiona Enter para volver.{Style.RESET_ALL}
        """
        consola(text)
