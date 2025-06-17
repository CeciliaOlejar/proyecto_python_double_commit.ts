from styles.Menu import Menu
from controller.asistente import Chat
from controller.usuario import Usuario_DAO
from models.Herramienta import Herramienta
from colorama import Fore, Style

if __name__ == "__main__":
    try:
        Menu.principal()
        Chat.asistente_bienvenida()
        while True:
            try:
                opcion = Menu.opcion()
                if opcion == 1:
                    Menu.login()
                elif opcion == 2:
                    id = int(input("Ingrese el id del usuario para eliminar: "))
                    Usuario_DAO.eliminar_usuario(id)
                elif opcion == 3:
                    print("Explorando herramientas disponibles...")
                    herramientas = Herramienta.listar_herramientas()
                    for index, herramienta in herramientas:
                        print(f"{Fore.LIGHTBLACK_EX}{index}. {herramienta}{Style.RESET_ALL}")
                elif opcion == 4:
                    nombre = input(
                        f"{Fore.GREEN}{Style.BRIGHT}A continuación escribe tu nombre, luego si deseas terminar el chat escibe <salir>: {Style.RESET_ALL}"
                    )
                    catalogo = Herramienta.listar_herramientas()
                    Chat.iniciar(nombre, catalogo)
                elif opcion == 5:
                    print(f"{Fore.CYAN}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.YELLOW}Opción: {opcion} no válida. Intenta de nuevo.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}Ocurrió un error: {e}{Style.RESET_ALL}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
