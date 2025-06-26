from models.Usuario import Usuario
from models.Herramienta import Herramienta

class GestionAlquiler(Usuario, Herramienta):
    def __init__(self, nombre, apellido, email, fecha_alquiler):
        super().__init__(nombre, apellido, email)
        self._fecha_alquiler = fecha_alquiler
        
    @property
    def fecha_alquiler(self):
        return self._fecha_alquiler
    
    @fecha_alquiler.setter
    def fecha_alquiler(self, fecha_alquiler):
        self._fecha_alquiler = fecha_alquiler
    
    def calcular_precio_alquiler(self, dias: int, precio_por_dia: int):
        return dias * precio_por_dia
    
    def __str__(self):
        return f"Alquiler: {self.nombre} {self.apellido}, Email: {self.email}, Fecha de Alquiler: {self.fecha_alquiler}"