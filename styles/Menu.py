from colorama import Style, Fore

class Menu:
    def __init__(self):
        pass
    
    @staticmethod
    def menu_ingreso():
        return f'''
        {Style.BRIGHT}{Fore.GREEN}Bienvenido a la App de Alquiler de Herramientas{Style.RESET_ALL}
        Por favor, elige una opción:
        1. Iniciar sesión
        2. Registrarse
        3. Salir
        {Style.BRIGHT}{Fore.YELLOW}Selecciona una opción (1-3): {Style.RESET_ALL}
        '''

    @staticmethod
    def menu_login():
        return f'''
        {Style.BRIGHT}{Fore.BLUE}Ingreso a la cuenta{Style.RESET_ALL}
        Por favor, introduce tus credenciales:
        {Style.BRIGHT}{Fore.CYAN}Usuario: {Style.RESET_ALL}
        {Style.BRIGHT}{Fore.CYAN}Contraseña: {Style.RESET_ALL}
        {Style.BRIGHT}{Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}
        '''