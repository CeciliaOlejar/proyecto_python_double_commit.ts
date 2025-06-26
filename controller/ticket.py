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
                    INSERT INTO ticket (
                        id_herramienta, nombre, tipo, descripcion, marca, modelo,
                        fecha_adquisicion, ubicacion, precio_por_dia, estado,
                        id_usuario, fecha_inicio, fecha_fin, estado_ticket
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    consulta,
                    (
                        ticket.id_herramienta,
                        ticket.nombre,
                        ticket.tipo,
                        ticket.descripcion,
                        ticket.marca,
                        ticket.modelo,
                        ticket.fecha_adquisicion,
                        ticket.ubicacion,
                        ticket.precio_por_dia,
                        ticket.estado,
                        ticket._cliente.id_usuario,
                        ticket._fecha_inicio,
                        ticket._fecha_fin,
                        ticket._estado_ticket,
                    ),
                )
                conexion.commit()
                print("Ticket registrado correctamente.")
        except Exception as e:
            print(f"Error al registrar ticket: {e}")
