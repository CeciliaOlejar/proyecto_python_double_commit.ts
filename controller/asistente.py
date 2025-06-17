from colorama import init, Fore, Style
import cohere
from styles.Menu import Menu
import re
from utils.resaltar import color_codigo
from dotenv import load_dotenv
import os

load_dotenv()
init()
API_KEY = os.getenv("COHERE_API_KEY")

class Chat:
    @staticmethod
    def iniciar(username):
        try:
            client = cohere.ClientV2(API_KEY)

            history = [
                {
                    "role": "system",
                    "content": f"""
                    Eres un asistente amigable, te llamas  confiable y profesional.
                    Hablas de forma clara y respetuosa. Tu objetivo es ayudar a los usuarios para la tienda de negocios ContruRent,
                    que es una aplicación de alquiler de herramientas. El nombre del usuario es {username}, dirígite a él por su nombre.
                    Puede que el usuario no te diga su nombre y te pregunte algo solamente. Responde cordialmente.
                    """,
                }
            ]

            while True:
                query = input(f"👨 {Fore.MAGENTA}{username}{Style.RESET_ALL}: ").strip()
                if query.lower() in ["salir", "exit", "quit"]:
                    print("🔚 Sesión de chat finalizada.\n")
                    break

                history.append({"role": "user", "content": query})

                response = client.chat(
                    model="command-a-03-2025",
                    messages=history,
                    temperature=0.3,
                    stop_sequences=["User:", "RentaBot:"],
                    frequency_penalty=0.3,
                )

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
            client = cohere.ClientV2(API_KEY)
            history = [{
            "role": "system",
            "content": """Tu nombre es Kai, un asistente virtual de la aplicación ConstruRent, especializada en el alquiler de herramientas.
            Tus objetivos al iniciar la aplicación son:
            1. Dar una cálida bienvenida al usuario.
            2. Explicar claramente las opciones disponibles en el menú principal:
            - Iniciar sesión si ya tiene una cuenta.
            - Crear una nueva cuenta.
            - Explorar las herramientas disponibles para alquiler.
            - Salir de la aplicación.
            3. Responder de manera eficiente y amigable cualquier consulta que el usuario tenga.
            Recuerda ser profesional, accesible y mantener un tono amigable en todo momento."""
            }]
        
            history.append({"role": "user", "content": "Hola!"})

            response = client.chat(
                model="command-a-03-2025",
                messages=history,
                temperature=0.3,
                stop_sequences=["User:", "Kai"],
                frequency_penalty=0.3,
            )


            full_response = "".join(
                [chunk.text for chunk in response.message.content if chunk]
            )
            bloques = re.split(r"(```[^`]+```)", full_response)

            print(f"\n{Fore.BLUE}👩 Kai: {Style.RESET_ALL}", end="")
            color_codigo(bloques)
            print("\n")
            history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(e)
    
