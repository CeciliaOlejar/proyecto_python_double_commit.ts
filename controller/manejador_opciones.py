from colorama import Fore, Style
from models.Usuario import Usuario
from models.Herramienta import Herramienta
from styles.Menu import Menu
from controller.usuario import Usuario_DAO
from controller.herramienta import Herramienta_DAO
from controller.ticket import Ticket_DAO
from utils.ubicacion import obtener_ubicacion
import asyncio

class ManejadorDeOpciones:
    """Maneja las opciones del menú principal"""

    @staticmethod
    def ejecutar_opcion(option: str | int, Chat) -> bool:
        """Ejecuta una opción y retorna True si debe continuar el bucle"""
        if option == "1" or option.startswith("<<opción: 1>>"):
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Iniciar Sesión{Style.RESET_ALL}"
            )
            usuario = Menu.login()
            _, rol = Usuario_DAO.ingresar(usuario)
            if rol == 1:
                while True:
                    ManejadorDeOpciones.menu_admin()
                    break
            else:
                catalogo = Herramienta_DAO.listar_herramientas()
                ciudad, pais = asyncio.run(obtener_ubicacion())
                Chat.iniciar(usuario.nombre, catalogo, ciudad, pais)
            return True
        elif option == "2" or option.startswith("<<opción: 2>>"):
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Crear nueva cuenta{Style.RESET_ALL}"
            )
            usuario = Menu.registro()
            Usuario_DAO.crear_usuario(usuario)
            catalogo = Herramienta_DAO.listar_herramientas()
            ciudad, pais = asyncio.run(obtener_ubicacion())
            Menu.menu_usuario(usuario)
            Chat.chat_interactivo(
                usuario.nombre, catalogo=catalogo, ciudad=ciudad, pais=pais
            )
            Menu.menu_usuario(usuario)
            return True
        elif option == "3" or option.startswith("<<opción: 3>>"):
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Explorar herramientas{Style.RESET_ALL}"
            )
            while True:
                subopcion = Menu.explorar_herramientas()
                # listado de herramientas
                if subopcion == 1:
                    salir_menu_explorar = False
                    while True:
                        herramientas = Herramienta_DAO.listar_herramientas()
                        if not herramientas:
                            print(
                                f"{Fore.YELLOW}No hay herramientas registradas.{Style.RESET_ALL}"
                            )
                            continue
                        print(
                            f"{Fore.WHITE}{Style.BRIGHT}Listado de herramientas:{Style.RESET_ALL}"
                        )
                        for herramienta in herramientas:
                            print(herramienta)
                        reservar = input(
                            f"{Fore.GREEN}¿Desea reservar alguna herramienta? (s/n): {Style.RESET_ALL}"
                        ).lower()
                        if reservar is None or reservar == "":
                            print(
                                f"{Fore.RED}Por favor, ingrese una opción válida.{Style.RESET_ALL}"
                            )
                            continue
                        if reservar in ["s", "si", "yes", "y"]:
                            print(
                                f"{Fore.RED}Estamos desarrollando esta mejora.{Style.RESET_ALL}"
                            )
                            break
                        # id_herramienta = input(
                        #     f"{Fore.YELLOW}Ingrese el ID de la herramienta a reservar: {Style.RESET_ALL}"
                        # )
                        # usuario_actual = Usuario_DAO.obtener_usuario_actual()
                        # if not usuario_actual:
                        #     print(
                        #         f"{Fore.RED}Debe iniciar sesión para reservar herramientas.{Style.RESET_ALL}"
                        #     )
                        #     salir_menu_explorar = True
                        #     Menu.principal()
                        #     break
                        # fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
                        # fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
                        # from models.Ticket import Ticket
                        # from datetime import datetime

                        # herramienta = next(
                        #     (
                        #         h
                        #         for h in herramientas
                        #         if str(h.id_herramienta) == id_herramienta
                        #     ),
                        #     None,
                        # )
                        # if herramienta:
                        #     ticket = Ticket(
                        #         herramienta.id_herramienta,
                        #         herramienta.nombre,
                        #         herramienta.tipo,
                        #         herramienta.descripcion,
                        #         herramienta.marca,
                        #         herramienta.modelo,
                        #         herramienta.fecha_adquisicion,
                        #         herramienta.ubicacion,
                        #         herramienta.precio_por_dia,
                        #         herramienta.estado,
                        #         cliente=usuario_actual,
                        #         fecha_inicio=datetime.strptime(
                        #             fecha_inicio, "%Y-%m-%d"
                        #         ),
                        #         fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d"),
                        #     )
                        #     print(
                        #         f"{Fore.GREEN}¡Reserva realizada! Aquí está tu ticket:{Style.RESET_ALL}"
                        #     )
                        #     print(ticket)
                        #     from controller.ticket import Ticket_DAO

                        #     Ticket_DAO.crear_ticket(ticket)
                        # else:
                        #     print(
                        #         f"{Fore.RED}ID de herramienta no válido.{Style.RESET_ALL}"
                        #     )
                        elif reservar == "n":
                            print(
                                f"{Fore.YELLOW}Volviendo al menú de herramientas...{Style.RESET_ALL}"
                            )
                            break
                        break
                    if salir_menu_explorar:
                        print(
                            f"{Fore.YELLOW}Volviendo al menú principal...{Style.RESET_ALL}"
                        )
                        break
                    # buscar herramientas por nombre
                    elif subopcion == 2 or "2":
                        salir_menu_explorar = False
                        nombre = input(
                            f"{Fore.YELLOW}{Style.BRIGHT}Ingrese el nombre de la herramienta: {Style.RESET_ALL}"
                        )
                        resultados = Herramienta_DAO.buscar_por_nombre(nombre)
                        if not resultados:
                            print(
                                f"{Fore.YELLOW}{Style.BRIGHT}No se encontraron herramientas con ese nombre.{Style.RESET_ALL}"
                            )
                            continue
                        print(
                            f"{Fore.WHITE}{Style.BRIGHT}Resultados de búsqueda:{Style.RESET_ALL}"
                        )
                        for herramienta in resultados:
                            print(herramienta)
                            reservar = input(
                                f"{Fore.GREEN}¿Desea reservar alguna herramienta? (s/n): {Style.RESET_ALL}"
                            ).lower()
                        if reservar in ["s", "si", "yes", "y"]:
                            print(
                                f"{Fore.RED}Estamos desarrollando esta mejora.{Style.RESET_ALL}"
                            )
                            break
                            # id_herramienta = input(
                            #     f"{Fore.YELLOW}Ingrese el ID de la herramienta a reservar: {Style.RESET_ALL}"
                            # )
                            # usuario_actual = Usuario_DAO.obtener_usuario_actual()
                            # if not usuario_actual:
                            #     print(
                            #         f"{Fore.RED}Debe iniciar sesión para reservar herramientas.{Style.RESET_ALL}"
                            #     )
                            #     salir_menu_explorar = True
                            #     break
                            # fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
                            # fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
                            # from models.Ticket import Ticket
                            # from datetime import datetime

                            # herramienta = next(
                            #     (
                            #         h
                            #         for h in herramientas
                            #         if str(h.id_herramienta) == id_herramienta
                            #     ),
                            #     None,
                            # )
                            # if herramienta:
                            #     ticket = Ticket(
                            #         herramienta.id_herramienta,
                            #         herramienta.nombre,
                            #         herramienta.tipo,
                            #         herramienta.descripcion,
                            #         herramienta.marca,
                            #         herramienta.modelo,
                            #         herramienta.fecha_adquisicion,
                            #         herramienta.ubicacion,
                            #         herramienta.precio_por_dia,
                            #         herramienta.estado,
                            #         cliente=usuario_actual,
                            #         fecha_inicio=datetime.strptime(
                            #             fecha_inicio, "%Y-%m-%d"
                            #         ),
                            #         fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d"),
                            #     )
                            #     print(
                            #         f"{Fore.GREEN}¡Reserva realizada! Aquí está tu ticket:{Style.RESET_ALL}"
                            #     )
                            #     print(ticket)
                            #     from controller.ticket import Ticket_DAO

                            #     Ticket_DAO.crear_ticket(ticket)
                            # else:
                            #     print(
                            #         f"{Fore.RED}ID de herramienta no válido.{Style.RESET_ALL}"
                            #     )
                        elif reservar in ["n", "no", "nope", "nada"]:
                            print(
                                f"{Fore.YELLOW}Volviendo al menú de herramientas...{Style.RESET_ALL}"
                            )
                            break
                        break
                    if salir_menu_explorar:
                        print(
                            f"{Fore.YELLOW}Volviendo al menú principal...{Style.RESET_ALL}"
                        )
                        break

                    # volver al menú principal
                    elif subopcion == 3:
                        print(
                            f"{Fore.YELLOW}{Style.BRIGHT}Volviendo al menú principal...{Style.RESET_ALL}"
                        )
                        break
                    else:
                        print(
                            f"{Fore.RED}{Style.BRIGHT}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}"
                        )
                return True

        elif option == "4" or option.startswith("<<opción: 4>>"):
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Continuando conversación con RentaBot...{Style.RESET_ALL}"
            )
            nombre = input(
                f"{Fore.GREEN}{Style.BRIGHT}Escribe tu nombre: {Style.RESET_ALL}"
            )
            catalogo = Herramienta_DAO.listar_herramientas()
            ciudad, pais = asyncio.run(obtener_ubicacion())
            Chat.chat_interactivo(nombre, catalogo, ciudad, pais)
            return True
        elif option == "5" or 5:
            print(
                f"{Fore.YELLOW}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}"
            )
            return False
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}⚠️ Opción: {option} no válida. Intenta de nuevo.{Style.RESET_ALL}"
            )
            return True

    @staticmethod
    def menu_admin():
        while True:
            opcion = Menu.menu_admin()
            if opcion == 1:
                while True:
                    subopcion = Menu.menu_gestionar_usuarios()
                    if subopcion == 1:
                        # Listar usuarios
                        print(f"{Fore.CYAN}Gestión de Usuarios{Style.RESET_ALL}")
                        usuarios = Usuario_DAO.leer_usuarios()
                        if not usuarios:
                            print(
                                f"{Fore.YELLOW}No hay usuarios registrados.{Style.RESET_ALL}"
                            )
                        else:
                            for usuario in usuarios:
                                print(f"\n{Fore.WHITE}{Style.BRIGHT}{usuario}{Style.RESET_ALL}")
                    elif subopcion == 2:
                        # Registrar usuario admin
                        print(
                            f"{Fore.CYAN}Registrar nuevo usuario admin:{Style.RESET_ALL}"
                        )
                        nombre = input("Nombre: ").strip()
                        apellido = input("Apellido: ").strip()
                        email = input("Email: ").strip()
                        contrasenia = input("Contraseña: ").strip()
                        usuario_admin = Usuario(nombre, apellido, email, contrasenia, 1)
                        Usuario_DAO.crear_usuario(usuario_admin)
                    elif subopcion == 3:
                        # Eliminar usuario
                        id_usuario = input(f"{Fore.YELLOW}Ingrese el ID del usuario a eliminar: {Style.RESET_ALL}")
                        Usuario_DAO.eliminar_usuario(id_usuario)
                    elif subopcion == 4:
                        # Modificar usuario
                        id_usuario = input(f"{Fore.YELLOW}Ingrese el ID del usuario a modificar: {Style.RESET_ALL}")
                        nombre = input("Nuevo nombre: ").strip()
                        apellido = input("Nuevo apellido: ").strip()
                        email = input("Nuevo email: ").strip()
                        contrasenia = input("Nueva contraseña: ").strip()
                        rol = int(input("Nuevo rol (1=admin, 2=usuario): ").strip())
                        usuario_modificado = Usuario(nombre, apellido, email, contrasenia, rol, id_usuario)
                        Usuario_DAO.actualizar_usuario(usuario_modificado)
                    elif subopcion == 5:
                        print(
                            f"{Fore.YELLOW}Volviendo al menú de administración...{Style.RESET_ALL}"
                        )
                        break
                    else:
                        print(
                            f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}"
                        )
                        continue
            elif opcion == 2:
                print(f"{Fore.CYAN}Gestión de herramientas{Style.RESET_ALL}")
                while True:
                    subopcion = Menu.menu_gestionar_herramientas()
                    if subopcion == 1:
                        # Listar herramientas
                        herramientas = Herramienta_DAO.listar_herramientas()
                        if not herramientas:
                            print(
                                f"{Fore.YELLOW}No hay herramientas registradas.{Style.RESET_ALL}"
                            )
                        else:
                            for herramienta in herramientas:
                                print(herramienta)
                    elif subopcion == 2:
                        # Registrar herramienta
                        print(
                            f"{Fore.CYAN}Registrar nueva herramienta:{Style.RESET_ALL}"
                        )
                        nombre = input("Nombre: ").strip()
                        tipo = input("Tipo: ").strip()
                        descripcion = input("Descripción: ").strip()
                        marca = input("Marca: ").strip()
                        modelo = input("Modelo: ").strip()
                        fecha_adquisicion = input("Fecha de adquisición (YYYY-MM-DD): ").strip()
                        ubicacion = input("Ubicación: ").strip()
                        precio_por_dia = float(input("Precio por día: ").strip())
                        estado = input("Estado (disponible, en uso, etc): ").strip()

                        from models.Herramienta import Herramienta
                        herramienta = Herramienta(
                            nombre=nombre,
                            tipo=tipo,
                            descripcion=descripcion,
                            marca=marca,
                            modelo=modelo,
                            fecha_adquisicion=fecha_adquisicion,
                            ubicacion=ubicacion,
                            precio_por_dia=precio_por_dia,
                            estado=estado
                        )
                        Herramienta_DAO.agregar_herramienta(herramienta)
                    elif subopcion == 3:
                        # Eliminar herramienta
                        id_herramienta = int(input(
                            "Ingrese el ID de la herramienta a eliminar: "
                        ))
                        resultado = Herramienta_DAO.eliminar(id_herramienta)
                        if resultado:
                            rowcount, nombre = resultado
                            if nombre is None:
                                print(f"{Fore.YELLOW}{Style.BRIGHT}ID de herramienta inexistente {id_herramienta}{Style.RESET_ALL}")
                            elif rowcount > 0:
                                print(f"{Fore.GREEN}{Style.BRIGHT}Herramienta '{nombre}' eliminada correctamente.{Style.RESET_ALL}")
                            else:
                                print(f"{Fore.YELLOW}{Style.BRIGHT}No se eliminó ninguna herramienta.{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}{Style.BRIGHT}Ocurrió un error inesperado.{Style.RESET_ALL}")
                    elif subopcion == 4:
                        # Modificar herramienta
                        id_herramienta = int(input("Ingrese el ID de la herramienta a modificar: ").strip())
                        nombre = input("Nuevo nombre: ").strip()
                        tipo = input("Nuevo tipo: ").strip()
                        descripcion = input("Nueva descripción: ").strip()
                        marca = input("Nueva marca: ").strip()
                        modelo = input("Nuevo modelo: ").strip()
                        fecha_adquisicion = input("Nueva fecha de adquisición (YYYY-MM-DD): ").strip()
                        ubicacion = input("Nueva ubicación: ").strip()
                        precio_por_dia = float(input("Nuevo precio por día: ").strip())
                        estado = input("Nuevo estado (disponible, en uso, etc): ").strip()

                        from models.Herramienta import Herramienta
                        herramienta_modificada = Herramienta(
                            nombre=nombre,
                            tipo=tipo,
                            descripcion=descripcion,
                            marca=marca,
                            modelo=modelo,
                            fecha_adquisicion=fecha_adquisicion,
                            ubicacion=ubicacion,
                            precio_por_dia=precio_por_dia,
                            estado=estado,
                            id_herramienta=id_herramienta
                        )
                        Herramienta_DAO.actualizar_herramienta(herramienta_modificada)
                    elif subopcion == 5:
                        print(
                            f"{Fore.YELLOW}Volviendo al menú de administración...{Style.RESET_ALL}"
                        )
                        break
                    else:
                        print(
                            f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}"
                        )
            elif opcion == 3:
                print(f"{Fore.MAGENTA}Gestión de tickets{Style.RESET_ALL}")
                while True:
                    subopcion = Menu.menu_gestionar_tickets()
                    if subopcion == 1:
                        # Listar tickets
                        tickets = Ticket_DAO.listar_tickets()
                        if not tickets:
                            print(
                                f"{Fore.YELLOW}No hay tickets registrados.{Style.RESET_ALL}"
                            )
                        else:
                            for ticket in tickets:
                                print(ticket)
                    elif subopcion == 2:
                        # Buscar ticket por ID
                        id_ticket = input("Ingrese el ID del ticket a buscar: ")
                        ticket = Ticket_DAO.buscar_por_id(id_ticket)
                        if ticket:
                            print(ticket)
                        else:
                            print(
                                f"{Fore.YELLOW}No se encontró el ticket con ese ID.{Style.RESET_ALL}"
                            )
                    elif subopcion == 3:
                        # Eliminar ticket
                        id_ticket = input("Ingrese el ID del ticket a eliminar: ")
                        Ticket_DAO.eliminar_ticket(id_ticket)
                    elif subopcion == 4:
                        # Modificar ticket
                        id_ticket = input("Ingrese el ID del ticket a modificar: ")
                        print("Funcionalidad de modificar ticket aún no implementada.")
                    elif subopcion == 5:
                        print(
                            f"{Fore.YELLOW}Volviendo al menú de administración...{Style.RESET_ALL}"
                        )
                        break
                    else:
                        print(
                            f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}"
                        )
            else:
                print(f"{Fore.YELLOW}Volviendo al menú de principal{Style.RESET_ALL}")
                Menu.principal()
                break
