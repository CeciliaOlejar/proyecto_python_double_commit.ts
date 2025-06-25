from colorama import init, Fore, Style
from utils.cohere_config import response_config
from utils.resaltar import color_codigo
import re
from playwright.sync_api import sync_playwright
from styles.Menu import Menu
from controller.herramienta import Herramienta_DAO
from controller.usuario import Usuario_DAO
from utils.ubicacion import obtener_ubicacion
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

init()

@dataclass
class ChatConfig:
    """Configuración para diferentes tipos de chat"""
    system_message: str
    show_greeting: bool = False
    enable_web_search: bool = False
    enable_option_detection: bool = False

class WebSearcher:
    """Maneja las búsquedas web de forma separada"""
    
    @staticmethod
    def search(query: str) -> str:
        """Realiza una búsqueda web usando Playwright"""
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
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
                print(f"{Fore.RED}{Style.BRIGHT}❌ Error en búsqueda web: {e}{Style.RESET_ALL}")
                return "No se pudo obtener información de la web."
            finally:
                browser.close()

class MessageProcessor:
    """Procesa y formatea los mensajes del chat"""
    
    @staticmethod
    def format_and_display(message: str, sender: str = "RentaBot") -> None:
        """Formatea y muestra un mensaje con colores"""
        bloques = re.split(r"(```[^`]+```)", message)
        color_codigo(bloques)
        if sender == "RentaBot":
            print(f"\n{Fore.BLUE}🤖 {sender}: {Style.RESET_ALL}", end="")
        print("\n")
    
    @staticmethod
    def extract_web_search(message: str) -> Optional[str]:
        """Extrae consulta de búsqueda web del mensaje"""
        match = re.search(r"<<websearch:(.+?)>>", message)
        return match.group(1).strip() if match else None
    
    @staticmethod
    def extract_option(message: str) -> Optional[str]:
        """Extrae número de opción del mensaje"""
        match = re.search(r"<<opción:\s*(\d+)\s*>>", message)
        return match.group(1).strip() if match else None

class OptionHandler:
    """Maneja las opciones del menú principal"""
    
    @staticmethod
    def execute_option(option: str) -> bool:
        """Ejecuta una opción y retorna True si debe continuar el bucle"""
        if option == "1":
            print(f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Iniciar Sesión{Style.RESET_ALL}")
            usuario = Menu.login()
            Usuario_DAO.ingresar(usuario, Chat)
            return True
        elif option == "2":
            print(f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Crear nueva cuenta{Style.RESET_ALL}")
            usuario = Menu.registro()
            Usuario_DAO.crear_usuario(usuario)
            return True
        elif option == "3":
            print(f"{Fore.CYAN}{Style.BRIGHT}Ejecutando: Explorar herramientas{Style.RESET_ALL}")
            print(f"{Fore.WHITE}{Style.BRIGHT}Explorando herramientas disponibles...{Style.RESET_ALL}")
            herramientas = Herramienta_DAO.listar_herramientas()
            for herramienta in herramientas:
                print(herramienta)
            return True
        elif option == "4":
            print(f"{Fore.CYAN}{Style.BRIGHT}Continuando conversación con RentaBot...{Style.RESET_ALL}")
            nombre = input(f"{Fore.GREEN}{Style.BRIGHT}Escribe tu nombre: {Style.RESET_ALL}")
            catalogo = Herramienta_DAO.listar_herramientas()
            ciudad, pais = obtener_ubicacion()
            Chat.chat_interactivo(nombre, catalogo, ciudad, pais)
            return True
        elif option == "5":
            print(f"{Fore.YELLOW}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.RED}{Style.BRIGHT}⚠️ Opción: {option} no válida. Intenta de nuevo.{Style.RESET_ALL}")
            return True

class Chat:
    """Clase principal para manejar diferentes tipos de chat"""
    
    @staticmethod
    def _create_system_message(tipo: str, **kwargs) -> str:
        """Crea mensajes del sistema según el tipo de chat"""
        if tipo == "bienvenida":
            return """Tu nombre es RentaBot, un asistente virtual de la aplicación ConstruRent, especializada en el alquiler de herramientas.
            Tus objetivos al iniciar la aplicación son:
            1. Dar una cálida bienvenida al usuario por única vez.
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
            nombre_usuario = kwargs.get('nombre_usuario', 'Usuario')
            catalogo = kwargs.get('catalogo', [])
            ciudad = kwargs.get('ciudad', 'Ciudad')
            pais = kwargs.get('pais', 'País')
            
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
    def _process_chat_response(historial: List[Dict[str, str]], enable_web_search: bool = False, 
                              enable_option_detection: bool = False) -> Tuple[str, Optional[str]]:
        """Procesa una respuesta del chat y maneja búsquedas web y opciones"""
        response = response_config(historial)
        full_response = "".join([chunk.text for chunk in response.message.content if chunk])
        
        # Manejar búsqueda web
        if enable_web_search:
            web_query = MessageProcessor.extract_web_search(full_response)
            if web_query:
                print(f"\n🔎 {Fore.YELLOW}{Style.BRIGHT}RentaBot está buscando en la web sobre: {web_query}{Style.RESET_ALL}")
                resultado_web = WebSearcher.search(web_query)
                print(f"{Fore.GREEN}{Style.BRIGHT}📄 Resultado web: {Style.RESET_ALL}{resultado_web}")
                historial.append({
                    "role": "assistant",
                    "content": f"Busqué esto: {resultado_web}",
                })
        
        # Extraer opción si está habilitado
        option = None
        if enable_option_detection:
            option = MessageProcessor.extract_option(full_response)
        
        return full_response, option
    
    @staticmethod
    def chat_base(config: ChatConfig, **kwargs) -> None:
        """Método base para manejar chats con diferentes configuraciones"""
        try:
            historial = [{
                "role": "system",
                "content": config.system_message
            }]
            
            # Mostrar saludo inicial si está configurado
            if config.show_greeting:
                historial.append({"role": "user", "content": "Hola!"})
                response, _ = Chat._process_chat_response(historial)
                MessageProcessor.format_and_display(response)
                historial.append({"role": "assistant", "content": response})
            
            # Bucle principal de chat
            while True:
                # Obtener entrada del usuario
                if config.enable_option_detection:
                    user_input = input(f"{Fore.GREEN}{Style.BRIGHT}¿Qué opción eliges?\n").strip()
                    Style.RESET_ALL
                else:
                    nombre_usuario = kwargs.get('nombre_usuario', 'Usuario')
                    user_input = input(f"🔹 {Fore.BLUE}{Style.BRIGHT}{nombre_usuario}{Style.RESET_ALL}: ").strip()
                
                # Verificar condiciones de salida
                if user_input.lower() in ["salir", "exit", "quit", "adiós"]:
                    if config.enable_option_detection:
                        print(f"{Fore.YELLOW}{Style.BRIGHT}🚪 Saliendo de la aplicación...{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}{Style.BRIGHT}🔚 Sesión de chat finalizada.{Style.RESET_ALL}\n")
                    break
                
                historial.append({"role": "user", "content": user_input})
                
                # Procesar respuesta
                bot_response, detected_option = Chat._process_chat_response(
                    historial, config.enable_web_search, config.enable_option_detection
                )
                
                # Mostrar respuesta
                MessageProcessor.format_and_display(bot_response)
                historial.append({"role": "assistant", "content": bot_response})
                
                # Manejar opciones si están habilitadas
                if config.enable_option_detection and detected_option:
                    print(f"{Fore.MAGENTA}{Style.BRIGHT}🎯 Opción detectada: {detected_option}{Style.RESET_ALL}")
                    should_continue = OptionHandler.execute_option(detected_option)
                    if not should_continue:
                        break
                elif config.enable_option_detection and not detected_option:
                    print(f"{Fore.YELLOW}{Style.BRIGHT}💬 No se detectó una opción específica, continuando conversación...{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}❌ Error en chat: {e}{Style.RESET_ALL}")
    
    @staticmethod
    def asistente_bienvenida() -> None:
        """Inicia el asistente de bienvenida"""
        config = ChatConfig(
            system_message=Chat._create_system_message("bienvenida"),
            show_greeting=True,
            enable_option_detection=True
        )
        Chat.chat_base(config)
    
    @staticmethod  
    def chat_interactivo(nombre_usuario: str, catalogo: list, ciudad: str, pais: str) -> None:
        """Inicia el chat interactivo con búsqueda web"""
        print(f"{Fore.CYAN}{Style.BRIGHT}💬 Pregunta lo que quieras...{Style.RESET_ALL}")
        
        config = ChatConfig(
            system_message=Chat._create_system_message(
                "interactivo", 
                nombre_usuario=nombre_usuario, 
                catalogo=catalogo, 
                ciudad=ciudad, 
                pais=pais
            ),
            enable_web_search=True
        )
        Chat.chat_base(config, nombre_usuario=nombre_usuario)
    
    # Mantener compatibilidad con el método anterior
    @staticmethod
    def iniciar(nombre_usuario: str, catalogo: list, ciudad: str, pais: str) -> None:
        """Método de compatibilidad - usa chat_interactivo"""
        print(f"{Fore.BLUE}{Style.BRIGHT}🔄 Iniciando chat con compatibilidad...{Style.RESET_ALL}")
        Chat.chat_interactivo(nombre_usuario, catalogo, ciudad, pais)