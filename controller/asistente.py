from colorama import init, Fore, Style
import cohere
from styles.Menu import Menu
import re

init()
API_KEY = "tu_api_key_perro"

class Chat:
    @staticmethod
    def iniciar(username):
        try:
            Menu.asistente(username)
            client = cohere.ClientV2(API_KEY)

            history = [
                {
                    "role": "system",
                    "content": f"""
                    Tu nombre es Kai. Eres un asistente amigable, confiable y profesional.
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
                    stop_sequences=["User:", "Kai"],
                    frequency_penalty=0.3,
                )

                full_response = "".join(
                    [chunk.text for chunk in response.message.content if chunk]
                )

                # Dividir la respuesta en bloques de código y texto normal
                blocks = re.split(r"(```[^`]+```)", full_response)

                print(f"\n{Fore.BLUE}👩 Kai: {Style.RESET_ALL}", end="")
                for block in blocks:
                    if block.startswith("```") and block.endswith("```"):
                        # Bloque de código
                        block.strip("```")
                        for char in block:
                            Menu.maquina_de_escribir(
                                text=f"{Fore.GREEN}{char}{Style.RESET_ALL}", delay=0.002
                            )
                    else:
                        # Texto normal
                        for char in block:
                            Menu.maquina_de_escribir(char)
                print("\n")

                # Guardamos la respuesta en historial para mantener el contexto
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
            blocks = re.split(r"(```[^`]+```)", full_response)

            print(f"\n{Fore.BLUE}👩 Kai: {Style.RESET_ALL}", end="")
            for block in blocks:
                if block.startswith("```") and block.endswith("```"):
                    block.strip("```")
                    for char in block:
                        Menu.maquina_de_escribir(
                            text=f"{Fore.GREEN}{char}{Style.RESET_ALL}", delay=0.002
                        )
                else:
                    for char in block:
                        Menu.maquina_de_escribir(char)
            print("\n")
            history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(e)
    
