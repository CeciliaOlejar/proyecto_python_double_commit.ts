from models.Ticket import Ticket
from controller.usuario import Usuario_DAO
from controller.herramienta import Herramienta_DAO
from db.conexion import Conexion

class Ticket_DAO:
    _INSERTAR_TICKET = """
                    INSERT INTO ticket (id_usuario, id_herramienta, estado_ticket, cliente, nombre, tipo, modelo, marca, descripcion,
                        fecha_adquisicion, precio_por_dia, ubicacion, fecha_fin, fecha_inicio
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
    @classmethod
    def crear_ticket(cls, ticket: Ticket):
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()

                cursor.execute(
                    cls._INSERTAR_TICKET,
                    (
                        ticket.usuario_actual.id_usuario,  # id_usuario
                        ticket.id_herramienta,  # id_herramienta
                        ticket.estado_ticket,  # estado_ticket
                        ticket.usuario_actual.nombre,  # cliente
                        ticket.nombre,  # nombre
                        ticket.tipo,  # tipo
                        ticket.modelo,  # modelo
                        ticket.marca,  # marca
                        ticket.descripcion,  # descripcion
                        ticket.fecha_adquisicion,  # fecha_adquisicion
                        ticket.precio_por_dia,  # precio_por_dia
                        ticket.ubicacion,  # ubicacion
                        ticket.fecha_fin,  # fecha_fin
                        ticket.fecha_inicio,  # fecha_inicio
                    ),
                )
                conexion.commit()
                print(f"Ticket registrado correctamente: {ticket}")
        except Exception as e:
            print(f"Error al registrar ticket: {e}")

    @classmethod
    def listar_tickets(cls):
        try:
            with Conexion.obtener_conexion() as conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM ticket")
                resultados = cursor.fetchall()
                tickets = []
                for fila in resultados:
                    tickets.append(Ticket(*fila))
                return tickets
        except Exception as e:
            print(f"Error al listar tickets: {e}")
            return []
