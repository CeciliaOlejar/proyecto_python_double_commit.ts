from colorama import init, Fore, Style
from utils.config import response_config
from utils.resaltar import color_codigo
import re

init()

class Chat:
    @staticmethod
    def iniciar(username: str, catalogo: list):
        try:
            history = [
                {
                    "role": "system",
                    "content": f"""
                    Eres un asistente amigable, te llamas  confiable y profesional.
                    Hablas de forma clara y respetuosa. Tu objetivo es ayudar a los usuarios para la tienda de negocios ConstruRent,
                    que es una aplicación de alquiler de herramientas. El nombre del usuario es {username}, dirígite a él por su nombre.
                    Puede que el usuario no te diga su nombre y te pregunte algo solamente. Responde cordialmente.
                    En caso de que te pregunten que herramientas hay te dejo el catálgo actual: {catalogo} ten en cuenta si el estado esta en uso,
                    debes de avisarle que no está diposnible si te pregunta por esa herramienta.
                    """,
                }
            ]
            print(f"{Fore.CYAN}{Style.BRIGHT}Pregunta lo que quieras...{Style.RESET_ALL}")
            while True:
                query = input(f"🔹 {Fore.BLUE}{Style.BRIGHT}{username}{Style.RESET_ALL}: ").strip()
                if query.lower() in ["salir", "exit", "quit"]:
                    print("🔚 Sesión de chat finalizada.\n")
                    break

                history.append({"role": "user", "content": query})
                response = response_config(history)
                full_response = "".join(
                    [chunk.text for chunk in response.message.content if chunk]
                )

                # Dividir la respuesta en bloques de código y texto normal
                bloques = re.split(r"(```[^`]+```)", full_response)
                color_codigo(bloques)
                print(f"\n{Fore.BLUE}🤖 RentaBot: {Style.RESET_ALL}", end="")

                print("\n")

                history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(e)

    @staticmethod
    def asistente_bienvenida():
        try:
            history = [{
                "role": "system",
                "content": """Tu nombre es RentaBot, un asistente virtual de la aplicación ConstruRent, especializada en el alquiler de herramientas.
                Tus objetivos al iniciar la aplicación son:
                1. Dar una cálida bienvenida al usuario.
                2. Explicar claramente las opciones disponibles en el menú principal:
                - Iniciar sesión si ya tiene una cuenta.
                - Crear una nueva cuenta.
                - Explorar las herramientas disponibles para alquiler.
                - Preguntar a RentaBot asistente IA.
                - Salir de la aplicación.
                3. Responder de manera eficiente y amigable cualquier consulta que el usuario tenga.
                Recuerda ser profesional, accesible y mantener un tono amigable en todo momento."""
            }]
        
            history.append({"role": "user", "content": "Hola!"})
            response = response_config(history)
            full_response = "".join(
                [chunk.text for chunk in response.message.content if chunk]
            )
            bloques = re.split(r"(```[^`]+```)", full_response)            
            color_codigo(bloques)
            print("\n")
            history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(e)
    
