from colorama import init, Fore, Style
import cohere
from styles.Menu import Menu
import re

init()

class Chat:
    @staticmethod
    def init(username):
        Menu.asistente(username)
        client = cohere.ClientV2("api_key_tuia_perro")

        history = [
            {"role": "system", "content": f'''
                Tu nombre es Kai. Eres un asistente amigable, confiable y profesional.
                Hablas de forma clara y respetuosa. Tu objetivo es ayudar a los usuarios para la tienda de negocios ContruRent,
                que es una aplicación de alquiler de herramientas. El nombre del usuario es {username}, dirígite a él por su nombre.
            '''}
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
                frequency_penalty=0.3
            )

            full_response = "".join([chunk.text for chunk in response.message.content if chunk])

            # Dividir la respuesta en bloques de código y texto normal
            blocks = re.split(r"(```[^`]+```)", full_response)

            print(f"\n{Fore.BLUE}👩 Kai: {Style.RESET_ALL}", end="")
            for block in blocks:
                if block.startswith("```") and block.endswith("```"):
                    # Bloque de código
                    block.strip("```")
                    for char in block:
                        Menu.maquina_de_escribir(text=f"{Fore.GREEN}{char}{Style.RESET_ALL}", delay=0.002)
                else:
                    # Texto normal
                    for char in block:
                        Menu.maquina_de_escribir(char)
            print("\n")

            # Guardamos la respuesta en historial para mantener el contexto
            history.append({"role": "assistant", "content": full_response})
