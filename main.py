from styles.Menu import Menu
from controller.asistente import Chat
from controller.usuario import Usuario_DAO
from controller.herramienta import Herramienta_DAO
from colorama import Fore, Style
from models.Ticket import Ticket
from models.Usuario import Usuario
from datetime import date

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
                    usuario = Menu.registro()
                    Usuario_DAO.crear_usuario(usuario)
                elif opcion == 3:
                    print(f"{Fore.WHITE}{Style.BRIGHT}Explorando herramientas disponibles...{Style.RESET_ALL}")
                    herramientas = Herramienta_DAO.listar_herramientas()
                    for herramienta in herramientas:
                        print(herramienta)
                elif opcion == 4:
                    nombre = input(
                        f"{Fore.GREEN}{Style.BRIGHT}A continuación escribe tu nombre, luego si deseas terminar el chat escibe <salir>: {Style.RESET_ALL}"
                    )
                    catalogo = Herramienta_DAO.listar_herramientas()
                    Chat.iniciar(nombre, catalogo)
                elif opcion == 5:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}")
                    break
                elif opcion == 6:
                    # Esto es una Prueba de clase Ticket (No va esta opción...)
                    usuario = Usuario("Juan", "Pérez", "juan@example.com", "secreta123")
    
                    ticket = Ticket(
                        id_herramienta=1,
                        nombre="Taladro",
                        tipo="Eléctrica",
                        descripcion="Taladro inalámbrico de 18V",
                        marca="DeWalt",
                        modelo="DCD791D2",
                        fecha_adquisicion=date(2023, 1, 15),
                        ubicacion="Almacén 1",
                        precio_por_dia=1000,
                        estado="Disponible",
                        cliente=usuario,
                        fecha_inicio=date(2025, 6, 10),
                        fecha_fin=date(2025, 6, 12),
                    )

                    print(ticket)
                else:
                    print(f"{Fore.YELLOW}Opción: {opcion} no válida. Intenta de nuevo.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}{Style.BRIGHT}Ocurrió un error: {e}{Style.RESET_ALL}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
