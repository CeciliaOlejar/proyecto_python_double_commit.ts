from models.Ticket import Ticket
from controller.usuario import Usuario_DAO
from controller.herramienta import Herramienta_DAO
from db.conexion import Conexion

class Ticket_DAO:
    @classmethod
    def crear_ticket(cls, ticket: Ticket):
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                consulta = """
                    INSERT INTO ticket (id_usuario, id_herramienta, estado_ticket, cliente, nombre, tipo, modelo, marca, descripcion,
                        fecha_adquisicion, precio_por_dia,  ubicacion, fecha_fin, fecha_inicio
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    consulta,
                    (
                        ticket.Usuario.id_usuario,      # id_usuario
                        ticket.id_herramienta,           # id_herramienta
                        ticket._estado_ticket,           # estado_ticket
                        ticket.Usuario.nombre,          # cliente
                        ticket.nombre,                   # nombre
                        ticket.tipo,                     # tipo
                        ticket.modelo,                   # modelo
                        ticket.marca,                    # marca
                        ticket.descripcion,              # descripcion
                        ticket.fecha_adquisicion,        # fecha_adquisicion
                        ticket.precio_por_dia,           # precio_por_dia
                        ticket.ubicacion,                # ubicacion
                        ticket._fecha_fin,               # fecha_fin
                        ticket._fecha_inicio,            # fecha_inicio
                    ),
                )
                conexion.commit()
                print("Ticket registrado correctamente.")
        except Exception as e:
            print(f"Error al registrar ticket: {e}")
