import textwrap
from utils.deteccion import detectar_rol

class Usuario:
    def __init__(self, nombre, apellido, email, contrasenia, rol=None, id_usuario=None):
        self.id_usuario = id_usuario
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        self._contrasenia = contrasenia
        self._rol = rol

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        self._apellido = apellido

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def contrasenia(self):
        return self._contrasenia

    @contrasenia.setter
    def contrasenia(self, contrasenia):
        self._contrasenia = contrasenia

    @property
    def rol(self):
        return self._rol
    
    @rol.setter
    def rol(self, rol):
        self._rol = rol 
        
    def __str__(self):
        return textwrap.dedent(f"""
        ID: {self.id_usuario}
        Usuario: {self._nombre}
        Apellido: {self._apellido}
        Email: {self._email}
        Rol: {detectar_rol(self._rol)}
        """)
