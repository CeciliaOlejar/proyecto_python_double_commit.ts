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
                    Menu.mostrar_herramientas(herramientas)
                elif opcion == 4:
                    nombre = input(
                        "A continucación escribe tu nombre, luego si deseas terminar el chat escibe <salir>: "
                    )
                    Chat.iniciar(nombre)
                elif opcion == 5:
                    print(f"{Fore.RED}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}")
                    break
                else:
                    print(f"Opción: {opcion} no válida. Intenta de nuevo.")
            except Exception as e:
                print(f"Error en el ingreso de opción.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
