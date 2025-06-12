from colorama import init, Style, Fore
import sys
import time
import getpass

init()


class Menu:
    @staticmethod
    def maquina_de_escribir(text, delay=0.006):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)

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
        ║  3. Salir                                                  ║
        ╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Selecciona una opción (1-3): {Style.RESET_ALL}
        """
        Menu.maquina_de_escribir(text)
        
    @staticmethod
    def registro():
        text = f"""
        {Fore.BLUE}{Style.BRIGHT}
        ╔════════════════════════════════════════════════════════════╗
        ║                    Registro de usuario                     ║
        ╠════════════════════════════════════════════════════════════╣
        {Style.RESET_ALL}"""
        Menu.maquina_de_escribir(text)
        print(f"""{Fore.BLUE}║ {Fore.CYAN}Usuario: {Style.RESET_ALL}""", end="")
        username = input()
        print(f"""{Fore.BLUE}        ║ {Fore.CYAN}Contraseña: {Style.RESET_ALL}""", end="")
        password = getpass.getpass("")
        print(f"""{Fore.BLUE}        ╚════════════════════════════════════════════════════════════╝
        {Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}
        """)

        return username, password

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
        Menu.maquina_de_escribir(text)
    
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
        Menu.maquina_de_escribir(text)
