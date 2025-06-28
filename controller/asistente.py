from colorama import init, Fore, Style
from utils.cohere_config import response_config
from utils.resaltar import color_codigo
import re  # módulo para expresiones regulares
from playwright.sync_api import sync_playwright
from styles.Menu import Menu
from controller.herramienta import Herramienta_DAO
from controller.usuario import Usuario_DAO
from controller.ticket import Ticket_DAO
from utils.ubicacion import obtener_ubicacion
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

init()


# El decorador @dataclass en Python se utiliza para simplificar la creación de clases que son principalmente contenedores de datos
@dataclass
class ConfiguracionChat:
    """Configuración para diferentes tipos de chat"""

    mensaje_sistema: str
    mostrar_saludo: bool = False
    habilitar_busqueda_web: bool = False
    habilitar_detec_opciones: bool = False


class BuscadorWeb:
    """Maneja las búsquedas web de forma separada"""

    @staticmethod
    def buscar(query: str) -> str:
        """Realiza una búsqueda web usando Playwright (Web scrapping)"""
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113 Safari/537.36"
            )
            page = context.new_page()
            try:
                page.goto("https://duckduckgo.com")
                page.fill("input[name='q']", query)
                page.press("input[name='q']", "Enter")
                page.wait_for_selector("a.result__a")
                result = page.inner_text("body").strip()
                return result
            except Exception as e:
                print(
                    f"{Fore.RED}{Style.BRIGHT}❌ Error en búsqueda web: {e}{Style.RESET_ALL}"
                )
                return "No se pudo obtener información de la web."
            finally:
                browser.close()


class ProcesadorMensajes:
    """Procesa y formatea los mensajes del chat"""

    @staticmethod
    def formatear_y_mostrar(message: str, sender: str = "RentaBot") -> None:
        """Formatea y muestra un mensaje con colores"""
        bloques = re.split(r"(```[^`]+```)", message)
        color_codigo(bloques)
        if sender == "RentaBot":
            print(f"\n{Fore.BLUE}🤖 {sender}: {Style.RESET_ALL}", end="")
        print("\n")

    @staticmethod
    def extraer_busqueda_web(message: str) -> Optional[str]:
        """Extrae consulta de búsqueda web del mensaje"""
        emparejar = re.search(r"<<websearch:(.+?)>>", message)
        return emparejar.group(1).strip() if emparejar else None

    @staticmethod
    def extraer_opcion(message: str) -> Optional[str]:
        """Extrae número de opción del mensaje"""
        emparejar = re.search(r"<<opción:\s*(\d+)\s*>>", message)
        return emparejar.group(1).strip() if emparejar else None


class ManejadorDeOpciones:
    """Maneja las opciones del menú principal"""

    @staticmethod
    def ejecutar_opcion(option: str) -> bool:
        """Ejecuta una opción y retorna True si debe continuar el bucle"""
        if option == "1":
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Iniciar Sesión{Style.RESET_ALL}"
            )
            usuario = Menu.login()
            Usuario_DAO.ingresar(usuario, Chat)
            return True
        elif option == "2":
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Crear nueva cuenta{Style.RESET_ALL}"
            )
            usuario = Menu.registro()
            Usuario_DAO.crear_usuario(usuario)
            return True
        elif option == "3":
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
                        if reservar == "s":
                            id_herramienta = input(
                                f"{Fore.YELLOW}Ingrese el ID de la herramienta a reservar: {Style.RESET_ALL}"
                            )
                            usuario_actual = Usuario_DAO.obtener_usuario_actual()
                            if not usuario_actual:
                                print(
                                    f"{Fore.RED}Debe iniciar sesión para reservar herramientas.{Style.RESET_ALL}"
                                )
                                salir_menu_explorar = True
                                break
                            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
                            fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
                            from models.Ticket import Ticket
                            from datetime import datetime

                            herramienta = next((h for h in herramientas if str(h.id_herramienta) == id_herramienta),None,)
                            if herramienta:
                                ticket = Ticket(
                                    herramienta.id_herramienta,
                                    herramienta.nombre,
                                    herramienta.tipo,
                                    herramienta.descripcion,
                                    herramienta.marca,
                                    herramienta.modelo,
                                    herramienta.fecha_adquisicion,
                                    herramienta.ubicacion,
                                    herramienta.precio_por_dia,
                                    herramienta.estado,
                                    cliente=usuario_actual,
                                    fecha_inicio=datetime.strptime(
                                        fecha_inicio, "%Y-%m-%d"
                                    ),
                                    fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d"),
                                )
                                print(
                                    f"{Fore.GREEN}¡Reserva realizada! Aquí está tu ticket:{Style.RESET_ALL}"
                                )
                                print(ticket)
                                from controller.ticket import Ticket_DAO
                                Ticket_DAO.crear_ticket(ticket)
                            else:
                                print(
                                    f"{Fore.RED}ID de herramienta no válido.{Style.RESET_ALL}"
                                )
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
                    elif subopcion == 2:
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
                        if reservar == "s":
                            id_herramienta = input(
                                f"{Fore.YELLOW}Ingrese el ID de la herramienta a reservar: {Style.RESET_ALL}"
                            )
                            usuario_actual = Usuario_DAO.obtener_usuario_actual()
                            if not usuario_actual:
                                print(
                                    f"{Fore.RED}Debe iniciar sesión para reservar herramientas.{Style.RESET_ALL}"
                                )
                                salir_menu_explorar = True
                                break
                            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ")
                            fecha_fin = input("Fecha de fin (YYYY-MM-DD): ")
                            from models.Ticket import Ticket
                            from datetime import datetime

                            herramienta = next((h for h in herramientas if str(h.id_herramienta) == id_herramienta),None,)
                            if herramienta:
                                ticket = Ticket(
                                    herramienta.id_herramienta,
                                    herramienta.nombre,
                                    herramienta.tipo,
                                    herramienta.descripcion,
                                    herramienta.marca,
                                    herramienta.modelo,
                                    herramienta.fecha_adquisicion,
                                    herramienta.ubicacion,
                                    herramienta.precio_por_dia,
                                    herramienta.estado,
                                    cliente=usuario_actual,
                                    fecha_inicio=datetime.strptime(
                                        fecha_inicio, "%Y-%m-%d"
                                    ),
                                    fecha_fin=datetime.strptime(fecha_fin, "%Y-%m-%d"),
                                )
                                print(
                                    f"{Fore.GREEN}¡Reserva realizada! Aquí está tu ticket:{Style.RESET_ALL}"
                                )
                                print(ticket)
                                from controller.ticket import Ticket_DAO
                                Ticket_DAO.crear_ticket(ticket)
                            else:
                                print(
                                    f"{Fore.RED}ID de herramienta no válido.{Style.RESET_ALL}"
                                )
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

        elif option == "4":
            print(
                f"{Fore.CYAN}{Style.BRIGHT}Continuando conversación con RentaBot...{Style.RESET_ALL}"
            )
            nombre = input(
                f"{Fore.GREEN}{Style.BRIGHT}Escribe tu nombre: {Style.RESET_ALL}"
            )
            catalogo = Herramienta_DAO.listar_herramientas()
            ciudad, pais = obtener_ubicacion()
            Chat.chat_interactivo(nombre, catalogo, ciudad, pais)
            return True
        elif option == "5":
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
                            print(f"{Fore.YELLOW}No hay usuarios registrados.{Style.RESET_ALL}")
                        else:
                            for usuario in usuarios:
                                print(usuario)
                    elif subopcion == 2:
                        # Registrar usuario admin
                        print(f"{Fore.CYAN}Registrar nuevo usuario admin:{Style.RESET_ALL}")
                        nombre = input("Nombre: ")
                        apellido = input("Apellido: ")
                        email = input("Email: ")
                        contrasenia = input("Contraseña: ")
                        usuario_admin = usuario(nombre, apellido, email, contrasenia, 1)
                        Usuario_DAO.crear_usuario(usuario_admin)
                    elif subopcion == 3:
                        # Eliminar usuario
                        id_usuario = input("Ingrese el ID del usuario a eliminar: ")
                        Usuario_DAO.eliminar_usuario(id_usuario)
                    elif subopcion == 4:
                        # Modificar usuario
                        id_usuario = input("Ingrese el ID del usuario a modificar: ")
                        # Aquí puedes pedir los nuevos datos y llamar a Usuario_DAO.actualizar_usuario(...)
                        print("Funcionalidad de modificar usuario aún no implementada.")
                    elif subopcion == 5:
                        print(f"{Fore.YELLOW}Volviendo al menú de administración...{Style.RESET_ALL}")
                        break
                    else:
                        print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")
            elif opcion == 2:
                print(f"{Fore.CYAN}Gestión de herramientas{Style.RESET_ALL}")
                while True:
                    subopcion = Menu.menu_gestionar_herramientas()
                    if subopcion == 1:
                        # Listar herramientas
                        herramientas = Herramienta_DAO.listar_herramientas()
                        if not herramientas:
                            print(f"{Fore.YELLOW}No hay herramientas registradas.{Style.RESET_ALL}")
                        else:
                            for herramienta in herramientas:
                                print(herramienta)
                    elif subopcion == 2:
                        # Registrar herramienta
                        print(f"{Fore.CYAN}Registrar nueva herramienta:{Style.RESET_ALL}")
                        # Aquí puedes pedir los datos y llamar a Herramienta_DAO.crear_herramienta(...)
                        print("Funcionalidad de registrar herramienta aún no implementada.")
                    elif subopcion == 3:
                        # Eliminar herramienta
                        id_herramienta = input("Ingrese el ID de la herramienta a eliminar: ")
                        Herramienta_DAO.eliminar(id_herramienta)
                    elif subopcion == 4:
                        # Modificar herramienta
                        id_herramienta = input("Ingrese el ID de la herramienta a modificar: ")
                        # Aquí puedes pedir los nuevos datos y llamar a Herramienta_DAO.actualizar_herramienta(...)
                        print("Funcionalidad de modificar herramienta aún no implementada.")
                    elif subopcion == 5:
                        print(f"{Fore.YELLOW}Volviendo al menú de administración...{Style.RESET_ALL}")
                        break
                    else:
                        print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")
            elif opcion == 3:
                print(f"{Fore.MAGENTA}Gestión de tickets{Style.RESET_ALL}")
                while True:
                    subopcion = Menu.menu_gestionar_tickets()
                    if subopcion == 1:
                        # Listar tickets
                        tickets = Ticket_DAO.listar_tickets()
                        if not tickets:
                            print(f"{Fore.YELLOW}No hay tickets registrados.{Style.RESET_ALL}")
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
                            print(f"{Fore.YELLOW}No se encontró el ticket con ese ID.{Style.RESET_ALL}")
                    elif subopcion == 3:
                        # Eliminar ticket
                        id_ticket = input("Ingrese el ID del ticket a eliminar: ")
                        Ticket_DAO.eliminar_ticket(id_ticket)
                    elif subopcion == 4:
                        # Modificar ticket
                        id_ticket = input("Ingrese el ID del ticket a modificar: ")
                        # Aquí puedes pedir los nuevos datos y llamar a Ticket_DAO.actualizar_ticket(...)
                        print("Funcionalidad de modificar ticket aún no implementada.")
                    elif subopcion == 5:
                        print(f"{Fore.YELLOW}Volviendo al menú de administración...{Style.RESET_ALL}")
                        break
                    else:
                        print(f"{Fore.RED}Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")
                


class Chat:
    """Clase principal para manejar diferentes tipos de chat"""

    @staticmethod
    def _crear_mensaje_sistema(tipo: str, **kwargs) -> str:
        """Crea mensajes del sistema según el tipo de chat"""
        if tipo == "bienvenida":
            ciudad = kwargs.get("ciudad", "Ciudad")
            pais = kwargs.get("pais", "País")
            return f"""Tu nombre es RentaBot, un asistente virtual de la aplicación ConstruRent, especializada en el alquiler de herramientas.
            - Ubicación del usuario: ({ciudad}, {pais}) para tener contexto.
            
            Tus objetivos al iniciar la aplicación son:
            1. Dar una cálida bienvenida al usuario de acuerdo a su ubicación por única vez
            2. Explicar claramente las opciones disponibles en el menú principal:
            - Iniciar sesión si ya tiene una cuenta (opción 1).
            - Crear una nueva cuenta (opción 2).
            - Explorar las herramientas disponibles para alquiler (opción 3).
            - Preguntar a RentaBot asistente IA (opción 4).
            - Salir de la aplicación (opción 5).
            3. Responder de manera eficiente y amigable cualquier consulta que el usuario tenga.
            
            CAPACIDADES:
            El usuario puede que te escriba algunas de las opciones mencionadas en el menú, si esto sucede
            usa <<opción: [número de la opción]>>, por ejemplo: si dice "Iniciar Sesión" o "opción 1" responde con <<opción: 1>>."""

        elif tipo == "interactivo":
            nombre_usuario = kwargs.get("nombre_usuario", "Usuario")
            catalogo = kwargs.get("catalogo", [])
            ciudad = kwargs.get("ciudad", "Ciudad")
            pais = kwargs.get("pais", "País")

            return f"""Eres RentaBot, un asistente IA amigable, confiable y profesional. Aunque trabajas para ConstruRent 
            (una app de alquiler de herramientas), eres un asistente completo que puede ayudar con cualquier tema.
            
            El nombre del usuario es {nombre_usuario}, dirígete a él por su nombre cuando sea apropiado.
            
            INFORMACIÓN IMPORTANTE:
            - Fecha actual: Estamos en 2025
            - Tu conocimiento base llega hasta 2024, por lo que para información reciente (2025) debes buscar en web
            - Puedes ayudar con CUALQUIER tema, no solo herramientas
            - Ubicación del usuario: ({ciudad}, {pais}) para tener contexto.
            
            CATÁLOGO DE HERRAMIENTAS CONSTRURENT:
            {catalogo}
            
            CAPACIDAD DE BÚSQUEDA WEB:
            Cuando necesites información que no tienes, especialmente:
            - Noticias actuales de 2025
            - Eventos recientes
            - Precios actualizados
            - Información técnica específica
            - Cualquier dato que no conozcas con certeza
            
            Usa: <<websearch: tu consulta en español>>
            
            Sé natural y útil. Si el usuario pregunta sobre herramientas, usa el catálogo. 
            Si pregunta sobre otros temas, ayúdalo igual. Si no sabes algo reciente, busca en web."""

        return ""

    @staticmethod
    def _procesar_respuesta_chat(
        historial: List[Dict[str, str]],
        habilitar_busqueda_web: bool = False,
        habilitar_detec_opciones: bool = False,
    ) -> Tuple[str, Optional[str]]:
        """Procesa una respuesta del chat y maneja búsquedas web y opciones"""
        response = response_config(historial)
        full_response = "".join(
            [chunk.text for chunk in response.message.content if chunk]
        )

        # Manejar búsqueda web
        if habilitar_busqueda_web:
            consulta_web = ProcesadorMensajes.extraer_busqueda_web(full_response)
            if consulta_web:
                print(
                    f"\n🔎 {Fore.YELLOW}{Style.BRIGHT}RentaBot está buscando en la web sobre: {consulta_web}{Style.RESET_ALL}"
                )
                resultado_web = BuscadorWeb.buscar(consulta_web)
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}📄 Resultado web: {Style.RESET_ALL}{resultado_web}"
                )
                historial.append(
                    {
                        "role": "assistant",
                        "content": f"Busqué esto: {resultado_web}",
                    }
                )

        # Extraer opción si está habilitado
        option = None
        if habilitar_detec_opciones:
            option = ProcesadorMensajes.extraer_opcion(full_response)

        return full_response, option

    @staticmethod
    def chat_base(config: ConfiguracionChat, **kwargs) -> None:
        """Método base para manejar chats con diferentes configuraciones"""
        try:
            historial = [{"role": "system", "content": config.mensaje_sistema}]

            # Mostrar saludo inicial si está configurado
            if config.mostrar_saludo:
                historial.append({"role": "user", "content": "Hola!"})
                response, _ = Chat._procesar_respuesta_chat(historial)
                ProcesadorMensajes.formatear_y_mostrar(response)
                historial.append({"role": "assistant", "content": response})

            # Bucle principal de chat
            while True:
                # Obtener entrada del usuario
                if config.habilitar_detec_opciones:
                    user_input = input(
                        f"{Fore.GREEN}{Style.BRIGHT}¿Qué opción eliges?\n"
                    ).strip()
                    Style.RESET_ALL
                else:
                    nombre_usuario = kwargs.get("nombre_usuario", "Usuario")
                    user_input = input(
                        f"🔹 {Fore.BLUE}{Style.BRIGHT}{nombre_usuario}{Style.RESET_ALL}: "
                    ).strip()

                # Verificar condiciones de salida
                if user_input.lower() in ["salir", "exit", "quit", "adiós"]:
                    if config.habilitar_detec_opciones:
                        print(
                            f"{Fore.YELLOW}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}"
                        )
                    else:
                        print(
                            f"{Fore.YELLOW}{Style.BRIGHT}🔚 Sesión de chat finalizada.{Style.RESET_ALL}\n"
                        )
                    break

                historial.append({"role": "user", "content": user_input})

                # Procesar respuesta
                bot_response, detected_option = Chat._procesar_respuesta_chat(
                    historial,
                    config.habilitar_busqueda_web,
                    config.habilitar_detec_opciones,
                )

                # Mostrar respuesta
                ProcesadorMensajes.formatear_y_mostrar(bot_response)
                historial.append({"role": "assistant", "content": bot_response})

                # Manejar opciones si están habilitadas
                if config.habilitar_detec_opciones and detected_option:
                    print(
                        f"{Fore.MAGENTA}{Style.BRIGHT}🎯 Opción detectada: {detected_option}{Style.RESET_ALL}"
                    )
                    should_continue = ManejadorDeOpciones.ejecutar_opcion(
                        detected_option
                    )
                    if not should_continue:
                        break
                elif config.habilitar_detec_opciones and not detected_option:
                    print(
                        f"{Fore.YELLOW}{Style.BRIGHT}💬 No se detectó una opción específica, continuando conversación...{Style.RESET_ALL}"
                    )

        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}❌ Error en chat: {e}{Style.RESET_ALL}")

    @staticmethod
    def asistente_bienvenida() -> None:
        """Inicia el asistente de bienvenida"""
        ciudad, pais = obtener_ubicacion()
        config = ConfiguracionChat(
            mensaje_sistema=Chat._crear_mensaje_sistema(
                "bienvenida", ciudad=ciudad, pais=pais
            ),
            mostrar_saludo=True,
            habilitar_detec_opciones=True,
        )
        Chat.chat_base(config)

    @staticmethod
    def chat_interactivo(
        nombre_usuario: str, catalogo: list, ciudad: str, pais: str
    ) -> None:
        """Inicia el chat interactivo con búsqueda web"""
        print(
            f"{Fore.CYAN}{Style.BRIGHT}💬 Pregunta lo que quieras...{Style.RESET_ALL}"
        )

        config = ConfiguracionChat(
            mensaje_sistema=Chat._crear_mensaje_sistema(
                "interactivo",
                nombre_usuario=nombre_usuario,
                catalogo=catalogo,
                ciudad=ciudad,
                pais=pais,
            ),
            habilitar_busqueda_web=True,
        )
        Chat.chat_base(config, nombre_usuario=nombre_usuario)

    # Mantener compatibilidad con el método anterior
    @staticmethod
    def iniciar(nombre_usuario: str, catalogo: list, ciudad: str, pais: str) -> None:
        """Método de compatibilidad - usa chat_interactivo"""
        print(
            f"{Fore.BLUE}{Style.BRIGHT}🔄 Iniciando chat con compatibilidad...{Style.RESET_ALL}"
        )
        Chat.chat_interactivo(nombre_usuario, catalogo, ciudad, pais)
