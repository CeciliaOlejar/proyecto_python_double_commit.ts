from styles.Menu import Menu
from controller.asistente import Chat
from controller.usuarios import Usuario_DAO
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
                    id_herramienta = input("Ingrese el ID de la herramienta a eliminar: ")
                    id, nombre = Herramienta.eliminar(id_herramienta)
                    print(f"Se ha eliminado la herramienta: {nombre}, ID: {id}")
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
                    print(f"Opción: {opcion} no válida. Intenta de nuevo.")
            except Exception as e:
                print(f"Ocurrió un error: {e}")
            
    except Exception as e:
        print(f"Ocurrió un error: {e}")
