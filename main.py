from styles.Menu import Menu
from controller.asistente import Chat
from colorama import Fore, Style


if __name__ == "__main__":
    try:
        Menu.principal()
        Chat.asistente_bienvenida()
    except Exception as e:
        print(f"{Fore.RED}{Style.BRIGHT}Ocurrió un error: {e}{Style.RESET_ALL}")
