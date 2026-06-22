class Empleado:
    def __init__(self, id, nombre, apellido, usuario, contrasena, rol="empleado"):
        self.__id = id
        self.__nombre = nombre
        self.__apellido = apellido
        self.__usuario = usuario
        self.__contrasena = contrasena
        self.__rol = rol  # "empleado" o "admin"

    def get_id(self): return self.__id
    def get_nombre(self): return self.__nombre
    def get_apellido(self): return self.__apellido
    def get_usuario(self): return self.__usuario
    def get_rol(self): return self.__rol

    # Setters
    def set_nombre(self, nombre): self.__nombre = nombre
    def set_apellido(self, apellido): self.__apellido = apellido
    def set_contrasena(self, contrasena): self.__contrasena = contrasena
    def set_rol(self, rol): self.__rol = rol

    def verificar_contrasena(self, contrasena):
        return self.__contrasena == contrasena

    def __str__(self):
        return f"{self.__nombre} {self.__apellido} ({self.__rol})"
