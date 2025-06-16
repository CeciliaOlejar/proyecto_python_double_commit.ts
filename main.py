from styles.Menu import Menu
from controller.asistente import Chat
from controller.usuario import Usuario_DAO
from models.Herramienta import Herramienta

if __name__ == "__main__":
    try:
        Menu.principal()
        Chat.asistente_bienvenida()
        while True:
            try:
                opcion = Menu.opcion()
                if opcion == 1:
                    Menu.login()
                elif opcion == 2:
                    id = int(input("Ingrese el id del usuario para eliminar: "))
                    Usuario_DAO.eliminar_usuario(id)
                elif opcion == 3:
                    print("Explorando herramientas disponibles...")
                    Herramienta.listar_herramientas()
                elif opcion == 4:
                    pregunta = input(
                        "Pregunta lo que quieras (escribe 'salir' para terminar): "
                    )
                    if pregunta.lower() == "salir":
                        print("Saliendo del chat")
                    Chat.iniciar(pregunta)
                elif opcion == 5:
                    print("Saliendo de la aplicación...")
                    break
                else:
                    print(f"Opción: {opcion} no válida. Intenta de nuevo.")
            except Exception as e:
                print(f"Error a ingresar la opción: {opcion}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
