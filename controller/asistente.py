from colorama import init, Fore, Style
from utils.cohere_config import response_config
from utils.resaltar import color_codigo
import re
from playwright.sync_api import sync_playwright
from styles.Menu import Menu
from controller.herramienta import Herramienta_DAO
from controller.usuario import Usuario_DAO
from utils.ubicacion import obtener_ubicacion

init()

class Chat:
    @staticmethod
    def iniciar(nombre_usuario: str, catalogo: list, ciudad: str, pais: str):
        try:
            historial = [
                {
                    "role": "system",
                    "content": f"""
                    Eres RentaBot, un asistente IA amigable, confiable y profesional. Aunque trabajas para ConstruRent 
                    (una app de alquiler de herramientas), eres un asistente completo que puede ayudar con cualquier tema.
                    
                    El nombre del usuario es {nombre_usuario}, dirígite a él por su nombre cuando sea apropiado.
                    
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
                    
                    EJEMPLOS DE CUÁNDO BUSCAR:
                    - "¿Qué pasó en las elecciones de [país] en 2025?"
                    - "¿Cuál es el precio actual del dólar?"
                    - "¿Qué nuevas películas salieron este año?"
                    - "¿Cómo está el clima hoy en {ciudad}?"
                    - "¿Cuáles son las noticias más importantes de esta semana?"
                    
                    Sé natural y útil. Si el usuario pregunta sobre herramientas, usa el catálogo. 
                    Si pregunta sobre otros temas, ayúdalo igual. Si no sabes algo reciente, busca en web.
                    """,
                }
            ]

            print(
                f"{Fore.CYAN}{Style.BRIGHT}Pregunta lo que quieras...{Style.RESET_ALL}"
            )
            while True:
                consulta = input(
                    f"🔹 {Fore.BLUE}{Style.BRIGHT}{nombre_usuario}{Style.RESET_ALL}: "
                ).strip()
                if consulta.lower() in ["salir", "exit", "quit"]:
                    print("🔚 Sesión de chat finalizada.\n")
                    break

                historial.append({"role": "user", "content": consulta})
                response = response_config(historial)
                full_response = "".join(
                    [chunk.text for chunk in response.message.content if chunk]
                )

                websearch_match = re.search(r"<<websearch:(.+?)>>", full_response)
                if websearch_match:
                    consulta_web = websearch_match.group(1).strip()
                    print(
                        f"\n🔎 {Fore.YELLOW}RentaBot está buscando en la web sobre: {consulta_web}{Style.RESET_ALL}"
                    )
                    resultado_web = Chat.playwright_sync(query=consulta_web)
                    print(
                        f"{Fore.GREEN}📄 Resultado web: {Style.RESET_ALL}{resultado_web}"
                    )
                    # Se agrega esto al historial también spara que la IA continúe desde ahí
                    historial.append(
                        {
                            "role": "assistant",
                            "content": f"Busqué esto: {resultado_web}",
                        }
                    )

                # Dividir la respuesta en bloques de código y texto normal
                bloques = re.split(r"(```[^`]+```)", full_response)
                color_codigo(bloques)
                print(f"\n{Fore.BLUE}🤖 RentaBot: {Style.RESET_ALL}", end="")

                print("\n")

                historial.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(e)

    @staticmethod
    def asistente_bienvenida():
        try:
            while True:
                historial = [
                    {
                        "role": "system",
                        "content": """Tu nombre es RentaBot, un asistente virtual de la aplicación ConstruRent, especializada en el alquiler de herramientas.
                        Tus objetivos al iniciar la aplicación son:
                        1. Dar una cálida bienvenida al usuario.
                        2. Explicar claramente las opciones disponibles en el menú principal:
                        - Iniciar sesión si ya tiene una cuenta (opción 1).
                        - Crear una nueva cuenta (opción 2).
                        - Explorar las herramientas disponibles para alquiler (opción 3).
                        - Preguntar a RentaBot asistente IA (opción 4).
                        - Salir de la aplicación (opción 5).
                        3. Responder de manera eficiente y amigable cualquier consulta que el usuario tenga.
                        Recuerda ser profesional, accesible y mantener un tono amigable en todo momento.
                        
                        - CAPACIDADES
                        El usuario puede que te escriba algunas de las opciones mencionadas en el menú, si esto sucede
                        usa <<opción: [número de la opción]>>, por ejemplo: si dice "Iniciar Sesión" o "opción 1" responde con <<opción: 1>>.
                        """,
                    }
                ]

                # Mensaje inicial del bot
                historial.append({"role": "user", "content": "Hola!"})
                response = response_config(historial)
                full_response = "".join(
                    [chunk.text for chunk in response.message.content if chunk]
                )

                # Mostrar respuesta del bot
                bloques = re.split(r"(```[^`]+```)", full_response)
                color_codigo(bloques)
                print("\n")
                historial.append({"role": "assistant", "content": full_response})

                # Obtener opción del usuario
                opcion_usuario = input("¿Qué opción eliges? ").strip()
                historial.append({"role": "user", "content": opcion_usuario})

                # Procesar respuesta del bot para extraer la opción
                response = response_config(historial)
                bot_response = "".join(
                    [chunk.text for chunk in response.message.content if chunk]
                )

                # Mostrar respuesta del bot
                bloques = re.split(r"(```[^`]+```)", bot_response)
                color_codigo(bloques)
                print("\n")

                # Buscar la opción en la respuesta del bot
                opciones_match = re.search(r"<<opción:\s*(\d+)\s*>>", bot_response)

                if opciones_match:
                    opcion_numero = opciones_match.group(1).strip()
                    print(f"Opción detectada: {opcion_numero}")

                    # Ejecutar la acción correspondiente
                    if opcion_numero == "1":
                        print("Ejecutando: Iniciar Sesión")
                        Menu.login()
                        break
                    elif opcion_numero == "2":
                        print("Ejecutando: Crear nueva cuenta")
                        usuario = Menu.registro()
                        Usuario_DAO.crear_usuario(usuario)
                        break
                    elif opcion_numero == "3":
                        print("Ejecutando: Explorar herramientas")
                        print(f"{Fore.WHITE}{Style.BRIGHT}Explorando herramientas disponibles...{Style.RESET_ALL}")
                        herramientas = Herramienta_DAO.listar_herramientas()
                        for herramienta in herramientas:
                            print(herramienta)
                            break
                    elif opcion_numero == "4":
                        print("Continuando conversación con RentaBot, puedes hacer que busque información actual en la web...")
                        nombre = input(
                        f"{Fore.GREEN}{Style.BRIGHT}A continuación escribe tu nombre, luego si deseas terminar el chat escibe <salir>: {Style.RESET_ALL}"
                        )
                        catalogo = Herramienta_DAO.listar_herramientas()
                        ciudad, pais = obtener_ubicacion()
                        Chat.iniciar(nombre, catalogo, ciudad, pais)
                    elif opcion_numero == "5":
                        print(f"{Fore.YELLOW}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}")
                        break
                    else:
                        print(f"{Fore.YELLOW}Opción: {opcion_numero} no válida. Intenta de nuevo.{Style.RESET_ALL}")
                        continue
                else:
                    # Si no se detecta una opción específica, continúa la conversación
                    print(
                        "No se detectó una opción específica, continuando conversación..."
                    )
                    historial.append({"role": "assistant", "content": bot_response})

                    # Verificar si el usuario quiere salir manualmente
                    if any(
                        palabra in opcion_usuario.lower()
                        for palabra in ["salir", "exit", "quit", "adiós"]
                    ):
                        print("Saliendo de la aplicación...")
                        break
        except Exception as e:
            print(e)

    @staticmethod
    def playwright_sync(query: str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
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
                print(e)
            finally:
                browser.close()
