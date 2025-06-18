import textwrap
from colorama import Fore, Style

class Herramienta:
    def __init__(self, id_herramienta, nombre, tipo, descripcion, marca, modelo, fecha_adquisicion, ubicacion, precio_por_dia, estado="Disponible"):
        self._id_herramienta = id_herramienta
        self._nombre = nombre
        self._tipo = tipo
        self._descripcion = descripcion
        self._marca = marca
        self._modelo = modelo
        self._fecha_adquisicion = fecha_adquisicion
        self._ubicacion = ubicacion
        self._precio_por_dia = precio_por_dia
        self._estado = estado
        
    @property
    def id_herramienta(self):
        return self._id_herramienta
    
    @id_herramienta.setter
    def id_herramienta(self, id_herramienta):
        self._id_herramienta = id_herramienta
    
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        self._tipo = tipo

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        self._descripcion = descripcion

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, marca):
        self._marca = marca

    @property
    def modelo(self):
        return self._modelo

    @modelo.setter
    def modelo(self, modelo):
        self._modelo = modelo

    @property
    def fecha_adquisicion(self):
        return self._fecha_adquisicion

    @fecha_adquisicion.setter
    def fecha_adquisicion(self, fecha_adquisicion):
        self._fecha_adquisicion = fecha_adquisicion

    @property
    def ubicacion(self):
        return self._ubicacion

    @ubicacion.setter
    def ubicacion(self, ubicacion):
        self._ubicacion = ubicacion

    @property
    def precio_por_dia(self):
        return self._precio_por_dia

    @precio_por_dia.setter
    def precio_por_dia(self, precio_por_dia):
        self._precio_por_dia = precio_por_dia

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    def __str__(self):
        return textwrap.dedent(f"""{Fore.BLUE}{Style.BRIGHT}
        ID herramienta: {self._id_herramienta}
        Herramienta: {self._nombre} {self._tipo} - ${self._precio_por_dia}/día
        Descripción: {self._descripcion}
        Marca: {self._marca}
        Modelo: {self._modelo}
        Fecha Adquisición: {self._fecha_adquisicion}
        Ubicación: {self._ubicacion}
        Estado: {self._estado}
        {Style.RESET_ALL}""")