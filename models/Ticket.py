from models.Herramienta import Herramienta
import textwrap
from colorama import Fore, Style

class Ticket(Herramienta):
    contador_ticket = 1

    def __init__(
        self,
        id_herramienta,
        nombre,
        tipo,
        descripcion,
        marca,
        modelo,
        fecha_adquisicion,
        ubicacion,
        precio_por_dia,
        estado,
        cliente=None,
        fecha_inicio=None,
        fecha_fin=None,
    ):
        super().__init__(
            id_herramienta,
            nombre,
            tipo,
            descripcion,
            marca,
            modelo,
            fecha_adquisicion,
            ubicacion,
            precio_por_dia,
            estado,
        )

        self._id_ticket = Ticket.contador_ticket
        Ticket.contador_ticket += 1

        self._cliente = (
            cliente  # A este cliente le vamos a instanciar la clase Usuario para su uso
        )
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado_ticket = "Activo"  # Puede ser: 'Activo', 'Finalizado', 'Cancelado'

    @property
    def obtener_ticket(self):
        return self._id_ticket

    def calcular_total(self):
        if self._fecha_inicio and self._fecha_fin:
            dias = (self._fecha_fin - self._fecha_inicio).days + 1
            return dias * self.precio_por_dia
        return 0

    def validar_fechas(self):
        if self.fecha_inicio and self.fecha_fin:
            return self._fecha_inicio <= self._fecha_fin
        return True  # Si falta alguna fecha, no validamos

    def finalizar_ticket(self):
        self._estado_ticket = "Finalizado"

    def cancelar_ticket(self):
        self._estado_ticket = "Cancelado"

    def __str__(self):
        total = self.calcular_total()
        return textwrap.dedent(f"""\{Fore.BLUE}
        ───── TICKET N° {self._id_ticket} ─────
        Cliente: {self._cliente if self._cliente else 'No especificado'}
        Estado del ticket: {self._estado_ticket}
        Fecha de inicio: {self._fecha_inicio or 'No definida'}
        Fecha de fin: {self._fecha_fin or 'No definida'}
        Costo total estimado: ${total}
        Herramienta asociada:
        {super().__str__()}{Style.RESET_ALL}
        """)
