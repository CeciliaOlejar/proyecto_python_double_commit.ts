from colorama import Style, Fore
from utils.efecto import consola


def codigo(bloques: list):
    for bloque in bloques:
        if bloque.startswith("```") and bloque.endswith("```"):
            bloque.strip("```")
            for char in bloque:
                consola(
                    text=f"{Fore.GREEN}{char}{Style.RESET_ALL}", delay=0.002
                )
        else:
            for char in bloque:
                consola(char)
