class Sucursal:

    def __init__(self, id, nombre, direccion):
        self.__id = id
        self.__nombre = nombre
        self.__direccion = direccion

    def get_nombre(self):
        return self.__nombre

    def get_direccion(self):
        return self.__direccion