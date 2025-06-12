from db.conexion import Conexion
from styles.Menu import Menu
from controller.asistente import Chat

if __name__ == "__main__":
    try:
        Menu.principal()
        Chat.asistente_bienvenida()
        while True:
            try:
                opcion = int(input("Elige una opción del menú: "))
                if opcion == 1:
                    Menu.login()
                elif opcion == 4:
                    pregunta = input("Pregunta lo que quieras (escribe 'salir' para terminar): ")
                    if pregunta.lower() == "salir":
                        print("Saliendo del chat")
                        break
                    Chat.iniciar(pregunta)
                elif opcion == 5:
                    print("Saliendo de la aplicación...")
                    break
                else:
                    print("Opción no válida. Intenta de nuevo.")
            except Exception as e:
                print(f"Error a ingresar la opción: {opcion}")
            
    except Exception as e:
        print(f"Ocurrió un error: {e}")
